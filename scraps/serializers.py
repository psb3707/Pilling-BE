from rest_framework import serializers
from medicines.models import Medicine
from django.shortcuts import get_object_or_404
from medicines.serializers import MedicineSerializer
from .models import Scrap

class ScrapSerializer(serializers.ModelSerializer):
    medicine_id = serializers.IntegerField()
    class Meta:
        model = Scrap
        fields = ['medicine_id','category']
    
    def create(self,validated_data):
        user = self.context['request'].user
        medicine_id = validated_data.pop('medicine_id')
        medicine = get_object_or_404(Medicine,pk=medicine_id)
        scrap = Scrap.objects.create(user=user,medicine=medicine,**validated_data)
        return scrap

   