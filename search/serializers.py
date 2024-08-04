from rest_framework import serializers
from medicines.models import Medicine

class MedicineSerializer(serializers.Serializer):
    itemName = serializers.CharField()
    efcy = serializers.CharField()
    image = serializers.CharField()

class MedicineDetailSerializer(serializers.Serializer):
    itemName = serializers.CharField()
    efcy = serializers.CharField()
    image = serializers.CharField()
    usemethod=serializers.CharField()
    atpn = serializers.CharField()
    intrc = serializers.CharField()
    seQ = serializers.CharField()

class MedicineNameSerializer(serializers.Serializer):
    itemName = serializers.CharField()