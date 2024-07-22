from django.db import models

from medicines.models import Medicine

class Tag(models.Model):
    content = models.CharField(max_length=10)

