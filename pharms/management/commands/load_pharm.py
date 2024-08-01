import json
from typing import Any

from django.core.management import BaseCommand
import requests
from config.utils import opening_hours
from pharms.models import Pharm

import xmltodict

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
    
        url = 'http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyFullDown'
        
        params = {'serviceKey':'C0OCzqNhw6sohn5jE2c1L52H4YKftzf9U8nxGSsC5GqH1YzH4Uu9VJ18zMHmpBrOEPgm3jqSOUpHh3j1oLcwLw==','pageNo':1,'numOfRows':24498}
        response = requests.get(url,params=params)
            
        jsonString = json.dumps(xmltodict.parse(response.content), indent=4)
    
        dict_data = json.loads(jsonString)
                    
        items = dict_data.get('response').get('body').get('items').get('item')
        print(len(items))
        
        data_list = []

        if items:
            for item in items:
                data = {"addr":item['dutyAddr'],"name":item['dutyName'],"timeMon":opening_hours(item.get('dutyTime1s'),item.get('dutyTime1c')),"timeTue":opening_hours(item.get('dutyTime2s'),item.get('dutyTime2c')),
                        "timeWed":opening_hours(item.get('dutyTime3s'),item.get('dutyTime3c')),"timeThu":opening_hours(item.get('dutyTime4s'),item.get('dutyTime4c')),"timeFri":opening_hours(item.get('dutyTime5s'),item.get('dutyTime5c')),
                        "timeSat":opening_hours(item.get('dutyTime6s'),item.get('dutyTime6c')),"timeSun":opening_hours(item.get('dutyTime7s'),item.get('dutyTime7c')),"lat":item.get('wgs84Lat'),"lon":item.get('wgs84Lon')}
                pharm = Pharm(**data)
                data_list.append(pharm)
            Pharm.objects.bulk_create(data_list,batch_size=24498,ignore_conflicts=True)
            