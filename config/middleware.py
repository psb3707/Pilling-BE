import time
import logging
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

logger = logging.getLogger(__name__)

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """API 성능 모니터링 미들웨어"""
    
    def process_request(self, request):
        # 요청 시작 시간 기록
        request._start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if not hasattr(request, '_start_time'):
            return response
            
        # 응답 시간 계산
        duration = time.time() - request._start_time
        
        # 느린 API 로깅
        if getattr(settings, 'PERFORMANCE_MONITORING', {}).get('LOG_SLOW_QUERIES', False):
            threshold = getattr(settings, 'PERFORMANCE_MONITORING', {}).get('SLOW_QUERY_THRESHOLD', 1.0)
            if duration > threshold:
                logger.warning(
                    f"Slow API: {request.method} {request.path} took {duration:.2f}s"
                )
        
        # 응답 헤더에 처리 시간 추가
        response['X-Response-Time'] = f"{duration:.3f}s"
        
        # API 사용량 추적
        if getattr(settings, 'API_USAGE_TRACKING', {}).get('ENABLED', False):
            self._track_api_usage(request, response, duration)
        
        return response
    
    def _track_api_usage(self, request, response, duration):
        """API 사용량 통계 수집"""
        try:
            # 일일 통계 키
            today = time.strftime('%Y-%m-%d')
            stats_key = f"api_stats_{today}"
            
            # 기존 통계 가져오기
            stats = cache.get(stats_key, {
                'total_requests': 0,
                'total_time': 0.0,
                'status_codes': {},
                'endpoints': {}
            })
            
            # 통계 업데이트
            stats['total_requests'] += 1
            stats['total_time'] += duration
            
            status_code = str(response.status_code)
            stats['status_codes'][status_code] = stats['status_codes'].get(status_code, 0) + 1
            
            endpoint = request.path
            if endpoint not in stats['endpoints']:
                stats['endpoints'][endpoint] = {'count': 0, 'total_time': 0.0}
            stats['endpoints'][endpoint]['count'] += 1
            stats['endpoints'][endpoint]['total_time'] += duration
            
            # 캐시에 저장 (24시간)
            cache.set(stats_key, stats, 86400)
            
        except Exception as e:
            logger.error(f"API 사용량 추적 실패: {str(e)}")

class APIRateLimitMiddleware(MiddlewareMixin):
    """간단한 API 호출 제한 미들웨어"""
    
    def process_request(self, request):
        if not getattr(settings, 'RATELIMIT_ENABLE', False):
            return None
            
        # 사용자별 요청 제한 (1분당 60회)
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_key = f"ratelimit_user_{request.user.id}"
            current_requests = cache.get(user_key, 0)
            
            if current_requests >= 60:  # 1분당 60회 제한
                from django.http import JsonResponse
                return JsonResponse(
                    {"error": "API 호출 제한을 초과했습니다. 잠시 후 다시 시도해주세요."}, 
                    status=429
                )
            
            # 카운터 증가
            cache.set(user_key, current_requests + 1, 60)  # 1분
        
        return None

class CacheHeaderMiddleware(MiddlewareMixin):
    """캐시 관련 헤더 추가 미들웨어"""
    
    def process_response(self, request, response):
        # 검색 API의 경우 캐시 헤더 추가
        if request.path.startswith('/search/'):
            # 1분간 캐시 허용
            response['Cache-Control'] = 'public, max-age=60'
            response['X-Cache-Strategy'] = 'database-first'
        
        return response