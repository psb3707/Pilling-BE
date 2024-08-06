from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .models import Schedule
from .serializers import ScheduleSerializer

# Create your views here.

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def schedule_access(request):
    if request.method == 'GET':
        schedules = Schedule.objects.filter(user=request.user)
        serializer = ScheduleSerializer(schedules, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ScheduleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def schedule_single(request, id):
    try: 
        schedule = Schedule.objects.get(id=id)
    except Schedule.DoesNotExist:
        return Response({"detail": "스케줄을 찾을 수 없음."}, status=status.HTTP_404_NOT_FOUND)
    if schedule.user != request.user:
        return Response({"detail": "당신 스케줄이 아님."}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = ScheduleSerializer(schedule, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'DELETE':
        schedule.delete()
        return Response({"detail": "스케줄 삭제 완료"}, status=status.HTTP_200_OK)
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def schedule_complete(request, id):
    if request.method == 'PATCH':
        schedule = Schedule.objects.get(id=id)
        
        if schedule.user != request.user:
            return Response({"detail": "당신 스케줄이 아님."}, status=status.HTTP_403_FORBIDDEN)
        else:
            if schedule.completed == False:
                schedule.completed = True
            else:
                schedule.completed = False
            schedule.save()
            
            serializer = ScheduleSerializer(schedule, context={'request': request})
            return Response(serializer.data)