from django.urls import path
from . import views_optimized

urlpatterns = [
    # 최적화된 검색 엔드포인트
    path('optimized/', views_optimized.search_medicine_optimized, name='search_medicine_optimized'),
    
    # 캐시 통계 (관리자용)
    path('cache-stats/', views_optimized.cache_stats, name='cache_stats'),
]