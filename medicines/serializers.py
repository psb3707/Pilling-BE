from rest_framework import serializers

from tags.serializer import TagSerializer
from .models import Medicine,MedicineTag

class MedicineTagSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    tags = TagSerializer(source='tag_set',many=True)
    class Meta:
        model = MedicineTag
        fields = [
            'user','tags'
        ]

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = [
            'id','item_seq','tags'
        ]
