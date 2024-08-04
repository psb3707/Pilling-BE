from rest_framework import serializers
from .models import Scrap


class ScrapSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name')
    class Meta:
        model = Scrap
        fields = ['id','user','medicine_name','category']