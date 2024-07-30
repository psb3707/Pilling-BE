from django.db import models

from accounts.models import PillingUser
from medicines.models import Medicine

class Schedule(models.Model):
    user = models.ForeignKey(PillingUser, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    completed = models.BooleanField(default=False)