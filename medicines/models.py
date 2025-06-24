from django.db import models
from django.utils import timezone

class Medicine(models.Model):
    name = models.TextField(default='')
    # tags = models.ManyToManyField(Tag,through='MedicineTag',blank=True)

class MedicineCache(models.Model):
    """사전 처리된 약물 정보 캐시"""
    item_name = models.CharField(max_length=255, unique=True, db_index=True)
    efcy_original = models.TextField(blank=True)  # 원본 효능 정보
    efcy_summary = models.TextField(blank=True)   # AI 요약 효능 정보
    item_image = models.URLField(blank=True)      # 약물 이미지
    
    # 상세 정보
    atpn_qesitm = models.TextField(blank=True)       # 주의사항
    intrc_qesitm = models.TextField(blank=True)      # 상호작용
    use_method_qesitm = models.TextField(blank=True) # 사용법
    se_qesitm = models.TextField(blank=True)         # 부작용
    
    # 메타 정보
    created_from_api = models.BooleanField(default=True)
    last_updated = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'medicine_cache'
        indexes = [
            models.Index(fields=['item_name']),
            models.Index(fields=['last_updated']),
        ]
    
    def __str__(self):
        return f"{self.item_name} - {self.efcy_summary[:50]}"

class CustomSummaryCache(models.Model):
    """사용자 맞춤 검색 키워드별 요약 캐시"""
    medicine_name = models.CharField(max_length=255, db_index=True)
    search_keyword = models.CharField(max_length=100, db_index=True)
    custom_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'custom_summary_cache'
        unique_together = ['medicine_name', 'search_keyword']
        indexes = [
            models.Index(fields=['medicine_name', 'search_keyword']),
        ]
    
    def __str__(self):
        return f"{self.medicine_name} - {self.search_keyword}"

# class MedicineTag(models.Model):
#     user = models.ForeignKey(PillingUser,on_delete=models.CASCADE)
#     medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag,on_delete=models.CASCADE)