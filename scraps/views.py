from django.shortcuts import render,get_object_or_404
from medicines.models import Medicine

from medicines.serializers import MedicineSerializer

from .models import Scrap
from .serializers import ScrapSerializer
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsOwner

class ScrapCreateView(CreateAPIView):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]


class ScrapListView(ListAPIView):
    serializer_class = ScrapSerializer
    permission_classes = [IsOwner]
    def get_queryset(self):
        queryset = Scrap.objects.all().defer("user")
        category = self.request.query_params.get('category',None)
        if category is not None:
            queryset = queryset.filter(category=category)
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
