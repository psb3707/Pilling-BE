from django.db import models
from accounts.models import PillingUser

class Tag(models.Model):
    content = models.CharField(max_length=10, unique=True)
    
class UserTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(PillingUser, on_delete=models.CASCADE)