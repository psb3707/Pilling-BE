from rest_framework.decorators import api_view
from .models import Medicine
import requests

@api_view(['GET'])
def search_medicine(request):
    itemName = request.GET.get('itemName',None)
    url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
    params = {"serviceKey":"C0OCzqNhw6sohn5jE2c1L52H4YKftzf9U8nxGSsC5GqH1YzH4Uu9VJ18zMHmpBrOEPgm3jqSOUpHh3j1oLcwLw%3D%3D", "numOfRows":10, "itemName": itemName, "type":"json"}

    response = requests.get(url, params=params)
    
