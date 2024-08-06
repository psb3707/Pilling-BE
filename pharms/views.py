from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from math import radians, cos, sin, sqrt, atan2
from .models import Pharm
from  .serializers import PharmSerializer

@api_view(['POST','GET'])
def pharm_info(request):

    def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # 지구 반경 (km)
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            return distance
    
    if request.method == 'POST':
        lat = request.data.get('lat',None)
        lon = request.data.get('lon',None)

        if lat is None or lon is None:
            return Response("No user coordinates provided.",status=status.HTTP_400_BAD_REQUEST)

        radius = 0.1

        pharms = Pharm.objects.all()

        user_pharm = None

        for pharm in pharms:
            distance = haversine(lat,lon,pharm.lat,pharm.lon)
            if distance <= radius:
                user_pharm = pharm
                radius = distance

        if user_pharm is None:
            return Response("데이터베이스 상에 존재하지 않는 약국입니다.",status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PharmSerializer(user_pharm)
        return Response(serializer.data)
    
    if request.method == 'GET':

        lat_data = request.GET.get('lat',None)
        lon_data = request.GET.get('lon',None)

        if lat_data is None or lon_data is None:
            return Response("No user coordinates provided.",status=status.HTTP_400_BAD_REQUEST)

        user_lat = float(lat_data)
        user_lon = float(lon_data)

        near_pharm = []

        for pharm in Pharm.objects.all():
            
            distance = haversine(user_lat,user_lon,pharm.lat,pharm.lon)
        
            if distance <= 1:
                near_pharm.append(pharm)
        
        serializer = PharmSerializer(near_pharm,many=True)
        return Response(serializer.data)