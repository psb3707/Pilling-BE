from rest_framework import serializers

from tags.serializer import TagSerializer
from .models import Medicine,MedicineTag

class MedicineTagSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    tag = TagSerializer()
    class Meta:
        model = MedicineTag
        fields = [
            'id','tag'
        ]

class MedicineSerializer(serializers.ModelSerializer):
    tags = MedicineTagSerializer(source='medicinetag_set', many=True, read_only=True)
    class Meta:
        model = Medicine
        fields = [
            'id','name','efcy','image', 'tags' 
        ]
