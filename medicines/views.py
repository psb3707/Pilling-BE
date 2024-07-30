from django.shortcuts import render

import os
import base64
import json

import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Medicine
from .serializers import MedicineSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def medicine_access(request):
    if request.method == 'POST':
        medicine_name = request.data.get('name')
        if not medicine_name:
            return Response({'error': 'Medicine name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        medicine, created = Medicine.objects.get_or_create(name=medicine_name)
        
        if created:
            serializer = MedicineSerializer(medicine)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Medicine already exists.', 'medicine_id': medicine.id}, status=status.HTTP_200_OK)