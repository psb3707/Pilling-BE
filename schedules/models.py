from django.db import models

from accounts.models import PillingUser
from medicines.models import Medicine
from tags.models import Tag

class Schedule(models.Model):
    user = models.ForeignKey(PillingUser, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, through='ScheduleTag', blank=True)
    
class ScheduleTag(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)