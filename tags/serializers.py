from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    tag_id = serializers.IntegerField(source='id')

    class Meta:
        model = Tag
        fields = ['tag_id', 'content']
        
class TagRequestSerializer(serializers.Serializer):
    medicine_name = serializers.CharField()