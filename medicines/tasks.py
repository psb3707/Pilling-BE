from celery import shared_task
from django.utils import timezone
from medicines.models import MedicineCache, CustomSummaryCache
from config.utils import get_efcy_using_openai, get_efcy_using_openai_custom
import requests
import logging
import time

logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def update_medicine_cache_batch(self, batch_size=50, start_page=1):
    """
    약물 정보를 배치로 업데이트하는 비동기 태스크
    프로덕션 환경에서 주기적으로 실행
    """
    try:
        base_url = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
        service_key = "C0OCzqNhw6sohn5jE2c1L52H4YKftzf9U8nxGSsC5GqH1YzH4Uu9VJ18zMHmpBrOEPgm3jqSOUpHh3j1oLcwLw%3D%3D"
        
        processed_count = 0
        success_count = 0
        error_count = 0
        
        for page_no in range(start_page, start_page + 10):  # 한 번에 10페이지씩 처리
            try:
                params = {
                    "serviceKey": service_key,
                    "type": "json",
                    "numOfRows": batch_size,
                    "pageNo": page_no
                }
                
                response = requests.get(base_url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data['body']['totalCount'] == 0 or not data['body'].get('items'):
                    break
                
                items = data['body']['items']
                
                for item in items:
                    try:
                        # 이미 처리된 약물 건너뛰기
                        if MedicineCache.objects.filter(item_name=item['itemName']).exists():
                            continue
                        
                        # OpenAI API 호출 (레이트 리미트 고려)
                        efcy_summary = None
                        if item.get('efcyQesitm'):
                            efcy_summary = get_efcy_using_openai(item['efcyQesitm'])
                            time.sleep(0.5)  # API 부하 방지
                        
                        # DB 저장
                        MedicineCache.objects.create(
                            item_name=item['itemName'],
                            efcy_original=item.get('efcyQesitm', ''),
                            efcy_summary=efcy_summary or '효능 정보 없음',
                            item_image=item.get('itemImage', ''),
                            atpn_qesitm=item.get('atpnQesitm', ''),
                            intrc_qesitm=item.get('intrcQesitm', ''),
                            use_method_qesitm=item.get('useMethodQesitm', ''),
                            se_qesitm=item.get('seQesitm', ''),
                            created_from_api=True,
                            last_updated=timezone.now()
                        )
                        
                        success_count += 1
                        processed_count += 1
                        
                        # 진행 상황 업데이트
                        if processed_count % 10 == 0:
                            self.update_state(
                                state='PROGRESS',
                                meta={
                                    'current': processed_count,
                                    'total': batch_size * 10,
                                    'status': f'{processed_count}개 처리 완료'
                                }
                            )
                        
                    except Exception as e:
                        error_count += 1
                        logger.error(f"약물 처리 실패 {item.get('itemName', 'Unknown')}: {str(e)}")
                        continue
                
            except Exception as e:
                logger.error(f"페이지 {page_no} 처리 실패: {str(e)}")
                continue
        
        result = {
            'processed': processed_count,
            'success': success_count,
            'errors': error_count,
            'status': 'completed'
        }
        
        logger.info(f"배치 처리 완료: {result}")
        return result
        
    except Exception as e:
        logger.error(f"배치 처리 실패: {str(e)}")
        raise self.retry(exc=e)

@shared_task
def cleanup_old_custom_summaries(days_old=30):
    """
    오래된 사용자 맞춤 요약 캐시 정리 (30일 이상)
    """
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
        deleted_count = CustomSummaryCache.objects.filter(
            created_at__lt=cutoff_date
        ).delete()[0]
        
        logger.info(f"오래된 캐시 {deleted_count}개 삭제 완료")
        return {'deleted_count': deleted_count}
        
    except Exception as e:
        logger.error(f"캐시 정리 실패: {str(e)}")
        raise

@shared_task
def refresh_medicine_summaries(medicine_names=None):
    """
    특정 약물들의 요약 정보 갱신
    """
    try:
        query = MedicineCache.objects.all()
        if medicine_names:
            query = query.filter(item_name__in=medicine_names)
        
        updated_count = 0
        for medicine in query:
            try:
                if medicine.efcy_original:
                    new_summary = get_efcy_using_openai(medicine.efcy_original)
                    medicine.efcy_summary = new_summary
                    medicine.last_updated = timezone.now()
                    medicine.save()
                    updated_count += 1
                    time.sleep(0.5)  # API 레이트 리미트
                    
            except Exception as e:
                logger.error(f"약물 요약 갱신 실패 {medicine.item_name}: {str(e)}")
                continue
        
        return {'updated_count': updated_count}
        
    except Exception as e:
        logger.error(f"요약 갱신 실패: {str(e)}")
        raise

@shared_task
def generate_popular_medicine_summaries():
    """
    인기 있는 약물들의 다양한 키워드 요약 미리 생성
    """
    try:
        # 인기 약물 목록 (실제로는 사용자 검색 로그에서 추출)
        popular_keywords = [
            '두통', '감기', '소화불량', '변비', '설사', 
            '알레르기', '염증', '통증', '발열', '기침'
        ]
        
        # 캐시된 약물 중 상위 100개
        popular_medicines = MedicineCache.objects.order_by('-last_updated')[:100]
        
        generated_count = 0
        for medicine in popular_medicines:
            for keyword in popular_keywords:
                # 이미 존재하는 요약은 건너뛰기
                if CustomSummaryCache.objects.filter(
                    medicine_name=medicine.item_name,
                    search_keyword=keyword
                ).exists():
                    continue
                
                try:
                    if medicine.efcy_original:
                        custom_summary = get_efcy_using_openai_custom(
                            medicine.efcy_original, keyword
                        )
                        
                        CustomSummaryCache.objects.create(
                            medicine_name=medicine.item_name,
                            search_keyword=keyword,
                            custom_summary=custom_summary
                        )
                        
                        generated_count += 1
                        time.sleep(0.3)  # API 레이트 리미트
                        
                except Exception as e:
                    logger.error(f"맞춤 요약 생성 실패 {medicine.item_name}-{keyword}: {str(e)}")
                    continue
        
        return {'generated_count': generated_count}
        
    except Exception as e:
        logger.error(f"인기 약물 요약 생성 실패: {str(e)}")
        raise