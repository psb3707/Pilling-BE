from rest_framework import serializers
from medicines.serializers import MedicineSerializer

from tags.serializer import TagSerializer
from .models import Schedule

class SchedulePostSerializer(serializers.Serializer):
    medicine_seq = serializers.IntegerField()
    datetime = serializers.DateField()

class ScheduleSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer()
    user_id = serializers.IntegerField(source='user.id')
    class Meta:
        model = Schedule
        fields = [
            'id','user_id','medicine','datetime','completed'
        ]