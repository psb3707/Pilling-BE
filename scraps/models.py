from django.db import models

from accounts.models import PillingUser
from medicines.models import Medicine

class Scrap(models.Model):
    CATEGORY_CHOICES = [
        ('F','FAVORITE'),
        ('G','GOOD'),
        ('B','BAD')
    ]
    user = models.ForeignKey(PillingUser, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    category = models.CharField(max_length=8,choices=CATEGORY_CHOICES)
