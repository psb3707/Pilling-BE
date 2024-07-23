from rest_framework import serializers

from .models import PillingUser

class PillingUserResponseSerializer(serializers.ModelSerializer):
    pilling_user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = PillingUser
        fields = ['pilling_user_id', 'nickname', 'kakao_sub']
        extra_kwargs = {
            field: {'read_only': True} for field in fields
        }

class KakaoLoginRequestSerializer(serializers.Serializer):
    access_code = serializers.CharField()
    
class UserPatchSerializer(serializers.Serializer):
    nickname = serializers.CharField()