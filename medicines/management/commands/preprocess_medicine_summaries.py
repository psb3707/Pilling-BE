import requests
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from medicines.models import MedicineCache
from config.utils import get_efcy_using_openai
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '모든 약물 정보를 사전 처리하여 OpenAI 요약과 함께 DB에 저장'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='배치 처리 크기 (기본: 100)'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='API 호출 간 딜레이 (초, 기본: 1.0)'
        )
        parser.add_argument(
            '--max-items',
            type=int,
            default=None,
            help='처리할 최대 아이템 수 (테스트용)'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        delay = options['delay']
        max_items = options['max_items']
        
        self.stdout.write("약물 정보 사전 처리를 시작합니다...")
        
        # 공공데이터 API에서 전체 약물 목록 가져오기
        base_url = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
        service_key = "C0OCzqNhw6sohn5jE2c1L52H4YKftzf9U8nxGSsC5GqH1YzH4Uu9VJ18zMHmpBrOEPgm3jqSOUpHh3j1oLcwLw%3D%3D"
        
        processed_count = 0
        success_count = 0
        error_count = 0
        page_no = 1
        
        while True:
            try:
                # 페이지별로 약물 정보 가져오기
                params = {
                    "serviceKey": service_key,
                    "type": "json",
                    "numOfRows": batch_size,
                    "pageNo": page_no
                }
                
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data['body']['totalCount'] == 0 or not data['body'].get('items'):
                    break
                
                items = data['body']['items']
                
                for item in items:
                    if max_items and processed_count >= max_items:
                        break
                        
                    try:
                        # 이미 처리된 약물인지 확인
                        if MedicineCache.objects.filter(item_name=item['itemName']).exists():
                            self.stdout.write(f"이미 처리됨: {item['itemName']}")
                            continue
                        
                        # OpenAI API로 효능 요약
                        self.stdout.write(f"처리 중: {item['itemName']}")
                        
                        efcy_summary = None
                        if item.get('efcyQesitm'):
                            efcy_summary = get_efcy_using_openai(item['efcyQesitm'])
                            time.sleep(delay)  # API 레이트 리미트 방지
                        
                        # DB에 저장
                        MedicineCache.objects.create(
                            item_name=item['itemName'],
                            efcy_original=item.get('efcyQesitm', ''),
                            efcy_summary=efcy_summary or '효능 정보 없음',
                            item_image=item.get('itemImage', ''),
                            atpn_qesitm=item.get('atpnQesitm', ''),
                            intrc_qesitm=item.get('intrcQesitm', ''),
                            use_method_qesitm=item.get('useMethodQesitm', ''),
                            se_qesitm=item.get('seQesitm', ''),
                            # 메타 정보
                            created_from_api=True,
                            last_updated=timezone.now()
                        )
                        
                        success_count += 1
                        processed_count += 1
                        
                        if processed_count % 10 == 0:
                            self.stdout.write(f"진행률: {processed_count}개 처리 완료")
                            
                    except Exception as e:
                        error_count += 1
                        logger.error(f"약물 처리 실패 {item['itemName']}: {str(e)}")
                        self.stdout.write(
                            self.style.ERROR(f"오류: {item['itemName']} - {str(e)}")
                        )
                        continue
                
                if max_items and processed_count >= max_items:
                    break
                    
                page_no += 1
                
            except Exception as e:
                logger.error(f"페이지 {page_no} 처리 실패: {str(e)}")
                self.stdout.write(self.style.ERROR(f"페이지 오류: {str(e)}"))
                break
        
        # 결과 출력
        self.stdout.write(
            self.style.SUCCESS(
                f"\n처리 완료!\n"
                f"- 전체 처리: {processed_count}개\n"
                f"- 성공: {success_count}개\n"
                f"- 실패: {error_count}개"
            )
        )