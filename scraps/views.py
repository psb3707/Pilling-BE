from medicines.models import Medicine

from .models import Scrap
from .serializers import ScrapSerializer
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from config.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class ScrapCreateView(CreateAPIView):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        medicine_name = request.data.get('medicine_name')
        if medicine_name is None:
            raise ValidationError({'details': '아직 없는 약입니다.'})
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
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Scrap.objects.filter(self.request.user).defer("user")
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
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Scrap.objects.filter(user=self.request.user).defer("user")

class ScrapUpdateView(UpdateAPIView):
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Scrap.objects.filter(user=self.request.user).defer("user")

class ScrapDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Scrap.objects.filter(user=self.request.user).defer("user")
