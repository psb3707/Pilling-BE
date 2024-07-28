import requests
from PIL import Image
import base64
from io import BytesIO
import io

def get_thumbnail(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        thumbnail_size = (100,100)
        image.thumbnail(thumbnail_size)

        buffuered = BytesIO()
        image.save(buffuered,format="WEBP")
        buffuered.seek(0)
        encoded_string = base64.b64encode(buffuered.read()).decode('utf-8')

        return encoded_string
    else:
        return None
    
def validate_base64_image(base64_string):
    try:
        # base64 디코딩
        image_data = base64.b64decode(base64_string)
        
        # 이미지로 열기 시도
        image = Image.open(io.BytesIO(image_data))
        image.show()
        # 포맷 확인
        if image.format != 'WEBP':
            return False
        
        return True
    except:
        return False