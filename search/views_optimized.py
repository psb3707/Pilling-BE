from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.db.models import Q, Case, When, IntegerField
from medicines.models import MedicineCache, CustomSummaryCache
from .serializers import MedicineSerializer, MedicineDetailSerializer, MedicineNameSerializer
from config.utils import get_efcy_using_openai, get_efcy_using_openai_custom
import requests
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_medicine_optimized(request):
    """최적화된 약물 검색 - 캐시 우선, 필요시 실시간 처리"""
    item_name = request.GET.get("itemName", None)
    efcy = request.GET.get("efcyQesitm", None)
    search_type = request.GET.get("type", 'basic')

    if not item_name and not efcy:
        return Response(
            {"error": "약 이름과 증상 정보 중 하나는 제공해야 합니다."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if item_name:
            return _search_by_name_optimized(item_name, search_type)
        elif efcy:
            return _search_by_symptom_optimized(efcy, search_type)
    except Exception as e:
        logger.error(f"검색 중 오류 발생: {str(e)}", exc_info=True)
        return Response(
            {"error": "검색 중 오류가 발생했습니다."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _search_by_name_optimized(item_name, search_type):
    """약물명으로 최적화된 검색"""
    # 1. 캐시에서 먼저 조회
    cache_key = f"medicine_search_{item_name}_{search_type}"
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"캐시 히트: {item_name}")
        return Response(cached_result)

    # 2. DB 캐시에서 조회
    if '%' in item_name:
        item_name = item_name.split('%', 1)[0]
    
    # 정확한 매치 우선, 부분 매치 보조
    db_medicines = MedicineCache.objects.filter(
        Q(item_name__iexact=item_name) | Q(item_name__icontains=item_name)
    ).order_by(
        # 정확한 매치를 먼저 정렬
        Case(
            When(item_name__iexact=item_name, then=0),
            default=1,
            output_field=IntegerField()
        )
    )[:10]

    if db_medicines.exists():
        logger.info(f"DB 캐시 히트: {item_name} ({db_medicines.count()}개)")
        medicines = _format_cached_medicines(db_medicines, search_type)
        
        # 메모리 캐시에 저장 (1시간)
        cache.set(cache_key, medicines, 3600)
        return Response(medicines)

    # 3. 실시간 API 호출 (fallback)
    logger.info(f"실시간 API 호출: {item_name}")
    return _fallback_api_search(item_name, None, search_type)

def _search_by_symptom_optimized(efcy, search_type):
    """증상으로 최적화된 검색"""
    cache_key = f"symptom_search_{efcy}_{search_type}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return Response(cached_result)

    # DB에서 증상 관련 약물 검색
    db_medicines = MedicineCache.objects.filter(
        Q(efcy_original__icontains=efcy) | Q(efcy_summary__icontains=efcy)
    )[:10]

    if db_medicines.exists():
        logger.info(f"증상 DB 캐시 히트: {efcy} ({db_medicines.count()}개)")
        
        medicines = []
        for medicine in db_medicines:
            # 사용자 맞춤 요약 캐시 확인
            custom_cache = CustomSummaryCache.objects.filter(
                medicine_name=medicine.item_name,
                search_keyword=efcy
            ).first()
            
            if custom_cache:
                efcy_data = custom_cache.custom_summary
            else:
                # 새로운 맞춤 요약 생성 및 캐시
                efcy_data = get_efcy_using_openai_custom(medicine.efcy_original, efcy)
                CustomSummaryCache.objects.create(
                    medicine_name=medicine.item_name,
                    search_keyword=efcy,
                    custom_summary=efcy_data
                )
            
            if search_type == "detail":
                medicine_data = _format_detailed_medicine(medicine)
            else:
                medicine_data = {
                    "itemName": medicine.item_name,
                    "efcy": efcy_data,
                    "image": medicine.item_image
                }
            medicines.append(medicine_data)
        
        # 캐시 저장
        cache.set(cache_key, medicines, 1800)  # 30분
        return Response(medicines)

    # Fallback to API
    return _fallback_api_search(None, efcy, search_type)

def _format_cached_medicines(db_medicines, search_type):
    """캐시된 약물 정보 포맷팅"""
    medicines = []
    
    for medicine in db_medicines:
        if search_type == "detail":
            medicine_data = _format_detailed_medicine(medicine)
        else:
            medicine_data = {
                "itemName": medicine.item_name,
                "efcy": medicine.efcy_summary,
                "image": medicine.item_image
            }
        medicines.append(medicine_data)
    
    return medicines

def _format_detailed_medicine(medicine):
    """상세 약물 정보 포맷팅"""
    return {
        "itemName": medicine.item_name,
        "efcy": medicine.efcy_original or "이 정보가 제공되지 않는 약입니다. :(",
        "image": medicine.item_image,
        "atpn": medicine.atpn_qesitm or "이 정보가 제공되지 않는 약입니다. :(",
        "intrc": medicine.intrc_qesitm or "이 정보가 제공되지 않는 약입니다. :(",
        "usemethod": medicine.use_method_qesitm or "이 정보가 제공되지 않는 약입니다. :(",
        "seQ": medicine.se_qesitm or "이 정보가 제공되지 않는 약입니다. :("
    }

def _fallback_api_search(item_name, efcy, search_type):
    """실시간 API 호출 (기존 방식과 동일하지만 로깅 추가)"""
    url = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
    service_key = "C0OCzqNhw6sohn5jE2c1L52H4YKftzf9U8nxGSsC5GqH1YzH4Uu9VJ18zMHmpBrOEPgm3jqSOUpHh3j1oLcwLw%3D%3D"
    
    params = {"type": "json", "numOfRows": 10}
    if item_name:
        params["itemName"] = item_name
    if efcy:
        params["efcyQesitm"] = efcy
    
    params["serviceKey"] = service_key
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['body']['totalCount'] == 0:
            message = "해당하는 약 이름에 대한 약 정보가 없습니다." if item_name else "해당하는 증상에 대한 약 정보가 없습니다."
            return Response({"error": message}, status=status.HTTP_404_NOT_FOUND)

        items = data['body']['items']
        medicines = []

        # 실시간 처리하면서 DB에도 저장 (백그라운드)
        for item in items:
            try:
                if search_type == "detail":
                    medicine_data = {
                        "itemName": item['itemName'],
                        "efcy": item.get('efcyQesitm', '이 정보가 제공되지 않는 약입니다. :('),
                        "image": item.get('itemImage', ''),
                        "atpn": item.get('atpnQesitm', '이 정보가 제공되지 않는 약입니다. :('),
                        "intrc": item.get('intrcQesitm', '이 정보가 제공되지 않는 약입니다. :('),
                        "usemethod": item.get('useMethodQesitm', '이 정보가 제공되지 않는 약입니다. :('),
                        "seQ": item.get('seQesitm', '이 정보가 제공되지 않는 약입니다. :(')
                    }
                else:
                    # 실시간 OpenAI 호출 (기존 방식)
                    if efcy:
                        efcy_data = get_efcy_using_openai_custom(item['efcyQesitm'], efcy)
                    else:
                        efcy_data = get_efcy_using_openai(item['efcyQesitm'])
                    
                    medicine_data = {
                        "itemName": item['itemName'],
                        "efcy": efcy_data,
                        "image": item.get('itemImage', '')
                    }
                    
                    # 백그라운드에서 DB에 저장 (이미 존재하지 않는 경우)
                    _save_to_cache_async(item, efcy_data)

                medicines.append(medicine_data)
                
            except Exception as e:
                logger.error(f"약물 처리 실패 {item.get('itemName', 'Unknown')}: {str(e)}")
                continue

        return Response(medicines)
        
    except requests.RequestException as e:
        logger.error(f"공공데이터 API 호출 실패: {str(e)}")
        return Response(
            {"error": "외부 서비스 연결에 실패했습니다. 잠시 후 다시 시도해주세요."}, 
            status=status.HTTP_502_BAD_GATEWAY
        )

def _save_to_cache_async(item, efcy_summary):
    """비동기적으로 캐시에 저장 (중복 체크)"""
    try:
        MedicineCache.objects.get_or_create(
            item_name=item['itemName'],
            defaults={
                'efcy_original': item.get('efcyQesitm', ''),
                'efcy_summary': efcy_summary,
                'item_image': item.get('itemImage', ''),
                'atpn_qesitm': item.get('atpnQesitm', ''),
                'intrc_qesitm': item.get('intrcQesitm', ''),
                'use_method_qesitm': item.get('useMethodQesitm', ''),
                'se_qesitm': item.get('seQesitm', ''),
                'created_from_api': True
            }
        )
    except Exception as e:
        logger.error(f"캐시 저장 실패 {item['itemName']}: {str(e)}")

# 통계 및 모니터링 엔드포인트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cache_stats(request):
    """캐시 통계 조회 (관리용)"""
    if not request.user.is_staff:
        return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    stats = {
        "총_캐시된_약물수": MedicineCache.objects.count(),
        "사용자_맞춤_요약수": CustomSummaryCache.objects.count(),
        "최근_업데이트": MedicineCache.objects.order_by('-last_updated').first().last_updated if MedicineCache.objects.exists() else None
    }
    
    return Response(stats)