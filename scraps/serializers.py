from rest_framework import serializers
from medicines.models import Medicine
from django.shortcuts import get_object_or_404
from medicines.serializers import MedicineSerializer
from .models import Scrap


class ScrapSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name')
    medicine_image = serializers.CharField(source='medicine.image')
    class Meta:
        model = Scrap
        fields = ['user','medicine_name','medicine_image','category']

class ScrapMedicineSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['name', 'efcy', 'image', 'usemethod', 'atpn', 'intrc', 'seQ']    
    

   