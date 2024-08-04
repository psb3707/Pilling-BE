from rest_framework import serializers
from tags.serializers import TagSerializer
from .models import Schedule
from tags.models import Tag
from medicines.models import MedicineTag, Medicine
from datetime import datetime, date
from rest_framework.exceptions import ValidationError


class ScheduleSerializer(serializers.ModelSerializer):    
    schedule_id = serializers.IntegerField(source='id', read_only=True)
    pilling_user_id = serializers.IntegerField(source='user.id', required=False)
    medicine_name = serializers.CharField(source='medicine.name')
    date = serializers.DateField()
    tags = serializers.SerializerMethodField()
    completed = serializers.BooleanField(required=False)
    
    class Meta:
        model = Schedule
        fields = ['schedule_id', 'pilling_user_id', 'medicine_name', 'date', 'tags', 'completed']

    def get_tags(self, obj):
        user = self.context['request'].user
        medicine_tags = MedicineTag.objects.filter(medicine=obj.medicine, user=user)
        return TagSerializer([mt.tag for mt in medicine_tags], many=True).data
    
    def create(self, validated_data):
        tags_data = self.initial_data.get('tags', [])
        user = self.context['request'].user
        
        medicine_name = self.initial_data.get('medicine_name')
        
        medicine = None
        try: 
            medicine = Medicine.objects.get(name=medicine_name)
        except Medicine.DoesNotExist:
            medicine = Medicine.objects.create(name=medicine_name)
        
        schedule = Schedule.objects.create(user=user, medicine=medicine, date=self.initial_data.get('date'), completed=False)
        
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(content=tag_data['content'])
            MedicineTag.objects.get_or_create(user=user, medicine=medicine, tag=tag)
        
        return schedule