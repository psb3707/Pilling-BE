from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Medicine
from .serializers import MedicineSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def medicine_access(request):
    if request.method == 'POST':
        medicine_name = request.data.get('name')
        if not medicine_name:
            return Response({'detail': '약 이름을 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        medicine, created = Medicine.objects.get_or_create(name=medicine_name)
        
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data, status=status.HTTP_201_CREATED)