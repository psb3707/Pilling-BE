from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Tag, UserTag
from medicines.models import Medicine
from .serializers import TagSerializer


@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def tags_access(request):
    if request.method == 'POST':
        newTag, created = Tag.objects.get_or_create(content=request.data.get('content'))
        # medicine = Medicine.objects.get(name=request.data.get('medicine_name'))
        # MedicineTag.objects.create(user=request.user, medicine=medicine, tag=newTag)
        
        UserTag.objects.create(user=request.user, tag=newTag)
        
        serializer = TagSerializer(newTag)
        return Response(serializer.data)
    
    elif request.method == 'GET':
        # medicine_name = request.query_params.get('medicine-name')
        # if not medicine_name:
        #     return Response({"detail": "약 이름이 필요합니다."}, status=400)
        # medicine = Medicine.objects.get(name=medicine_name)
        # medicine_tags = MedicineTag.objects.filter(user=request.user, medicine=medicine)
        
        customTags = []
        for ut in UserTag.objects.filter(user=request.user):
            customTags.append(ut.tag)
        
        tags = set(customTags + list(Tag.objects.filter(id__in=range(1, 18))))
        
        serializer = TagSerializer(sorted(tags, key=lambda x: x.id), many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # medicine = Medicine.objects.get(name=request.query_params.get('medicine-name'))
        tag = Tag.objects.get(content=request.query_params.get('content'))
        
        try:
            UserTag.objects.get(tag=tag, user=request.user).delete()
            return Response({"detail": "삭제 완료."}, status=status.HTTP_200_OK)
        except UserTag.DoesNotExist:
            return Response({"detail": "없는 태그임."}, status=status.HTTP_200_OK)