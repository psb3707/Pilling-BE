from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MedicineSerializer, MedicineDetailSerializer
from config.utils import get_thumbnail, get_efcy_using_openai, get_efcy_using_openai_custom
import requests


@api_view(['GET'])
def search_medicine(request):
    itemName = request.GET.get("itemName",None)
    efcy = request.GET.get("efcyQesitm",None)
    type = request.GET.get("type",'basic')

    url = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList?serviceKey=C0OCzqNhw6sohn5jE2c1L52H4YKftzf9U8nxGSsC5GqH1YzH4Uu9VJ18zMHmpBrOEPgm3jqSOUpHh3j1oLcwLw%3D%3D"
    if not itemName and not efcy:
        return Response("약 이름과 증상 정보 중 하나는 제공해야 합니다.",status=status.HTTP_400_BAD_REQUEST)
    
    if itemName is not None:
        
        params = {"itemName":itemName,"type":"json","numOfRows":10}
        response = requests.get(url, params=params)
        data = response.json()
        
        items = data['body']['items']
        
        # filtered_items = [item for item in items if item['itemName'].startswith(itemName)]
        # sorted_items = sorted(filtered_items, key=lambda x: x['itemName'])

        medicines = []


        if type == "detail":
            if items:
                for item in items:
                    data = {"name":item['itemName'],"efcy":item['efcyQesitm'],"image":item['itemImage'], "atpn":item['atpnQesitm'], "intrc":item['intrcQesitm'],
                            "usemethod":item['useMethodQesitm'],"seQ":item['seQesitm']}
                    medicines.append(data)

                serializer = MedicineDetailSerializer(medicines,many=True)
                return Response(serializer.data)
            else:
                return Response("검색된 약이 없습니다.", status=status.HTTP_404_NOT_FOUND)
            
        if items:
            for item in items:
                if item['itemImage']:
                    itemImage = get_thumbnail(item['itemImage'])
                    
                else:
                    itemImage = "사진은 공개되지 않았습니다. 죄송합니다."

                efcy_data = get_efcy_using_openai(item['efcyQesitm'])
                medicine = {"name":item['itemName'],"efcy":efcy_data,"image":itemImage}
                medicines.append(medicine)
        
            serializer = MedicineSerializer(medicines,many=True)
            return Response(serializer.data)
        
        else:
            return Response("검색된 약이 없습니다.", status=status.HTTP_404_NOT_FOUND)
        
    elif efcy is not None:

        params = {"efcyQesitm":efcy, "type":"json","numOfRows":10}
        response = requests.get(url, params=params)
        data = response.json()
        items = data['body']['items']

        medicines = []

        if type == "detail":
            if items:
                for item in items:
                    data = {"name":item['itemName'],"efcy":item['efcyQesitm'],"image":item['itemImage'], "atpn":item['atpnQesitm'], "intrc":item['intrcQesitm']}
                    medicines.append(data)
                serializer = MedicineDetailSerializer(medicines,many=True)
                return Response(serializer.data)
            
            else:
                return Response("검색된 약이 없습니다.", status=status.HTTP_404_NOT_FOUND)
            
        if items:
            for item in items:
                if item['itemImage']:
                    itemImage = get_thumbnail(item['itemImage'])
                    
                else:
                    itemImage = "사진은 공개되지 않았습니다. 죄송합니다."
                    
                efcy_data = get_efcy_using_openai_custom(item['efcyQesitm'],efcy)
                medicine = {"name":item['itemName'],"efcy":efcy_data,"image":itemImage}
                medicines.append(medicine)
                
            serializer = MedicineSerializer(medicines,many=True)
            return Response(serializer.data)
        
        else:
            return Response("검색된 약이 없습니다.", status=status.HTTP_404_NOT_FOUND)
