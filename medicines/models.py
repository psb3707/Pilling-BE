from django.db import models
from accounts.models import PillingUser

from tags.models import Tag

class Medicine(models.Model):
    name = models.TextField()
    efcy = models.TextField()
    image = models.TextField()
    usemethod=models.CharField()
    atpn = models.CharField()
    intrc = models.CharField()
    seQ = models.CharField()
    tags = models.ManyToManyField(Tag,through='MedicineTag',blank=True)

class MedicineTag(models.Model):
    user = models.ForeignKey(PillingUser,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)