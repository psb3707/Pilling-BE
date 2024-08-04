from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import MedicineSerializer, MedicineDetailSerializer,MedicineNameSerializer
from config.utils import get_efcy_using_openai, get_efcy_using_openai_custom
import requests
from rest_framework.permissions import AllowAny


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

        if data['body']['totalCount'] == 0:
            return Response("해당하는 약 이름에 대한 약 정보가 없습니다.",status=status.HTTP_404_NOT_FOUND)
        
        items = data['body']['items']
        
        # filtered_items = [item for item in items if item['itemName'].startswith(itemName)]
        # sorted_items = sorted(filtered_items, key=lambda x: x['itemName'])

        medicines = []


        if type == "detail":
            
            for item in items:
                    # if item['itemImage']:
                    #     itemImage = get_thumbnail(item['itemImage'])
                    # else:
                    #     itemImage = "사진은 공개되지 않았습니다. 죄송합니다."

                data = {"itemName":item['itemName'],"efcy":item['efcyQesitm'],"image":item['itemImage'], "atpn":item['atpnQesitm'], "intrc":item['intrcQesitm'],
                        "usemethod":item['useMethodQesitm'],"seQ":item['seQesitm']}
                medicines.append(data)

            serializer = MedicineDetailSerializer(medicines,many=True)
            return Response(serializer.data)
           
            
        
        for item in items:
                # if item['itemImage']:
                #     itemImage = get_thumbnail(item['itemImage'])
                    
                # else:
                #     itemImage = "사진은 공개되지 않았습니다. 죄송합니다."

            efcy_data = get_efcy_using_openai(item['efcyQesitm'])
            medicine = {"itemName":item['itemName'],"efcy":efcy_data,"image":item['itemImage']}
            medicines.append(medicine)
        
        serializer = MedicineSerializer(medicines,many=True)
        return Response(serializer.data)
        
        
        
    elif efcy is not None:

        params = {"efcyQesitm":efcy, "type":"json","numOfRows":10}
        response = requests.get(url, params=params)
        data = response.json()

        if data['body']['totalCount'] == 0:
            return Response("해당하는 증상에 대한 약 정보가 없습니다.",status=status.HTTP_404_NOT_FOUND)
        
        items = data['body']['items']

        medicines = []

        if type == "detail":
            
            for item in items:
                    # if item['itemImage']:
                    #     itemImage = get_thumbnail(item['itemImage'])
                    # else:
                    #     itemImage = "사진은 공개되지 않았습니다. 죄송합니다."
                data = {"itemName":item['itemName'],"efcy":item['efcyQesitm'],"image":item['itemImage'], "atpn":item['atpnQesitm'], "intrc":item['intrcQesitm'],
                        "usemethod":item['useMethodQesitm'],"seQ":item['seQesitm']}
                medicines.append(data)
            serializer = MedicineDetailSerializer(medicines,many=True)
            return Response(serializer.data)
            
           
        
        for item in items:
                # if item['itemImage']:
                #     itemImage = get_thumbnail(item['itemImage'])
                    
                # else:
                #     itemImage = "사진은 공개되지 않았습니다. 죄송합니다."
                    
            efcy_data = get_efcy_using_openai_custom(item['efcyQesitm'],efcy)
            medicine = {"itemName":item['itemName'],"efcy":efcy_data,"image":item['itemImage']}
            medicines.append(medicine)
                
        serializer = MedicineSerializer(medicines,many=True)
        return Response(serializer.data)
        
        
@api_view(['GET'])
@permission_classes([AllowAny])
def search_for_register(request):
    query = request.GET.get('itemName',None)
    if query is None:
        return Response("약 이름이 필요합니다.",status=status.HTTP_400_BAD_REQUEST)
    url = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList?serviceKey=C0OCzqNhw6sohn5jE2c1L52H4YKftzf9U8nxGSsC5GqH1YzH4Uu9VJ18zMHmpBrOEPgm3jqSOUpHh3j1oLcwLw%3D%3D"
    params = {"itemName":query,"type":"json","numOfRows":10}
    response = requests.get(url, params=params)
        
    data = response.json()

    if data['body']['totalCount'] == 0:
        return Response("해당하는 약 이름에 대한 약 정보가 없습니다.",status=status.HTTP_404_NOT_FOUND)
        
    items = data['body']['items']

    medicines = []

    for item in items:
        name_data = {"itemName":item['itemName']}
        medicines.append(name_data)
    serializer = MedicineNameSerializer(medicines,many=True)

    return Response(serializer.data)
    



