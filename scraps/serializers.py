from rest_framework import serializers
from .models import Scrap

class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap
        fields = ['id','medicine','category']