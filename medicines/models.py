from django.db import models
from accounts.models import PillingUser

from tags.models import Tag

class Medicine(models.Model):
    name = models.TextField(default='')
    efcy = models.TextField(default='')
    image = models.TextField(default='', null=True)
    usemethod=models.CharField(max_length=1000, default='')
    atpn = models.CharField(max_length=1000, default='')
    intrc = models.CharField(max_length=1000, default='', null=True)
    seQ = models.CharField(max_length=1000, default='')
    tags = models.ManyToManyField(Tag,through='MedicineTag',blank=True)

class MedicineTag(models.Model):
    user = models.ForeignKey(PillingUser,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)