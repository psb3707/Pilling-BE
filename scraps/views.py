from medicines.models import Medicine

from .models import Scrap
from .serializers import ScrapSerializer
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from config.permissions import IsOwner
from rest_framework.exceptions import ValidationError

class ScrapCreateView(CreateAPIView):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        medicine_name = request.data.get('medicine_name')
        category = request.data.get('category')
        
        medicine = None
        try: 
            medicine = Medicine.objects.get(name=medicine_name)
        except Medicine.DoesNotExist:
            medicine = Medicine.objects.create(name=medicine_name)
        
        if Scrap.objects.filter(medicine=medicine, user=request.user):
            raise ValidationError({'details': '이미 스크랩했던 약입니다.'})
        scrap = Scrap.objects.create(user=request.user, medicine=medicine, category=category)
        serializer = ScrapSerializer(instance=scrap)
        return Response(serializer.data)

class ScrapListView(ListAPIView):
    serializer_class = ScrapSerializer
    permission_classes = [IsOwner]
    def get_queryset(self):
        queryset = Scrap.objects.all().defer("user")
        category = self.request.query_params.get('category',None)
        if category is not None:
            try:
                queryset = queryset.filter(category=category)
            except queryset is None:
                return Response("No content",status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Category is None",status=status.HTTP_400_BAD_REQUEST)
        return queryset

class ScrapRetreiveView(RetrieveAPIView):
    queryset = Scrap.objects.all().defer("user")
    serializer_class = ScrapSerializer
    permission_classes = [IsOwner]

class ScrapUpdateView(UpdateAPIView):
    queryset = Scrap.objects.all().defer("user")
    serializer_class = ScrapSerializer
    permission_classes = [IsOwner]

class ScrapDestroyView(DestroyAPIView):
    queryset = Scrap.objects.all()
    permission_classes = [IsOwner]
