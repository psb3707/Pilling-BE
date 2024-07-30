from rest_framework import serializers
from .models import Medicine

class MedicineSerializer(serializers.ModelSerializer):
    medicine_id = serializers.IntegerField(source='id')

    class Meta:
        model = Medicine
        fields = ['medicine_id', 'name']