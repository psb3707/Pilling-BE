from django.db import models

class Pharm(models.Model):
    addr = models.TextField()
    name = models.CharField(max_length=255)
    timeMon = models.TextField()
    timeTue = models.TextField()
    timeWed = models.TextField()
    timeThu = models.TextField()
    timeFri = models.TextField()
    timeSat = models.TextField(default='Closed')
    timeSun = models.TextField(default='Closed')
    lat = models.FloatField()
    lon = models.FloatField()