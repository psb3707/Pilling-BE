from rest_framework import serializers
from medicines.models import Medicine
from django.shortcuts import get_object_or_404
from medicines.serializers import MedicineSerializer
from .models import Scrap


class ScrapSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name')
    class Meta:
        model = Scrap
        fields = ['user','medicine_name','category']