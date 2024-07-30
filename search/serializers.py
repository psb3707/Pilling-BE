from rest_framework import serializers
from .models import Medicine

class MedicineSerializer(serializers.Serializer):
    name = serializers.CharField()
    efcy = serializers.CharField()
    image = serializers.CharField()

class MedicineDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    efcy = serializers.CharField()
    image = serializers.CharField()
    usemethod=serializers.CharField()
    atpn = serializers.CharField()
    intrc = serializers.CharField()
    seQ = serializers.CharField()