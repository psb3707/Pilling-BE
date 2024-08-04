from django.db import models
from accounts.models import PillingUser

from tags.models import Tag

class Medicine(models.Model):
    name = models.TextField(default='')
    tags = models.ManyToManyField(Tag,through='MedicineTag',blank=True)

class MedicineTag(models.Model):
    user = models.ForeignKey(PillingUser,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)