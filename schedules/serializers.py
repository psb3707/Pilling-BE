from rest_framework import serializers
from medicines.models import Medicine, MedicineTag
from medicines.serializers import MedicineSerializer
from tags.models import Tag

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
    
    def create(self, validated_data):
        medicine_data = validated_data.pop('medicine')
        tags_data = validated_data.pop('tags',[])
        medicine = Medicine.objects.create(**medicine_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            MedicineTag.objects.create(user=validated_data[''])