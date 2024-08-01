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
    medicine_id = serializers.IntegerField(source='medicine.id', read_only=True)
    medicine_name = serializers.CharField(write_only=True)
    date = serializers.DateField()
    tags = serializers.SerializerMethodField()
    completed = serializers.BooleanField(required=False)
    
    class Meta:
        model = Schedule
        fields = ['schedule_id', 'pilling_user_id', 'medicine_id', 'medicine_name', 'date', 'tags', 'completed']

    def get_tags(self, obj):
        print('get_tags 들어옴')
        user = self.context['request'].user
        medicine_tags = MedicineTag.objects.filter(medicine=obj.medicine, user=user)
        return TagSerializer([mt.tag for mt in medicine_tags], many=True).data
    
    def create(self, validated_data):
        tags_data = self.initial_data.get('tags', [])
        user = self.context['request'].user
        
        medicine_name = validated_data.pop('medicine_name')
        
        medicine = None
        try: 
            medicine = Medicine.objects.get(name=medicine_name)
        except Medicine.DoesNotExist:
            efcy = self.initial_data.get('efcy')
            image = self.initial_data.get('image')
            if efcy is None or image is None:
                raise ValidationError({'details': '효능과 사진 필드에 문자열 값이 있어야 합니다.'})
            medicine = Medicine.objects.create(name=medicine_name, efcy=efcy, image=image)
        
        schedule = Schedule.objects.create(user=user, medicine=medicine, **validated_data)
        
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(content=tag_data['content'])
            MedicineTag.objects.get_or_create(user=user, medicine=medicine, tag=tag)
        
        return schedule