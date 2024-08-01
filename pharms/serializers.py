from pharms.models import Pharm
from rest_framework import serializers

class PharmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharm
        fields = '__all__'