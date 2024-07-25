from datetime import datetime,timedelta
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView
from .serializers import SchedulePostSerializer,ScheduleSerializer
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsOwner
from .models import Schedule
from medicines.models import Medicine
from django.utils import timezone

class ScheduleCreateView(CreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = SchedulePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        medicine = Medicine(medicine_seq=data['medicine_seq'])
        schedule = Schedule(user=request.user,medicine=medicine,datetime=data['datetime'])
        schedule.save()
        serializer = ScheduleSerializer(instance=schedule)
        return Response(serializer.data)

class ScheduleListView(ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        today = timezone.now().date()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        queryset = Schedule.objects.filter(datetime_gte=first_day, datetime_lte=last_day)
        return queryset

class ScheduleRetreiveView(RetrieveAPIView):
     queryset = Schedule.objects.all()
     serializer_class = ScheduleSerializer
     permission_classes = [IsOwner]
     
class ScheduleUpdateView(UpdateAPIView):
     queryset = Schedule.objects.all()
     serializer_class = ScheduleSerializer
     permission_classes = [IsOwner]

class ScheduleDestroyView(DestroyAPIView):
        queryset = Schedule.objects.all()
        permission_classes = [IsOwner]


        
