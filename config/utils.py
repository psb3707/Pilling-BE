import requests
from PIL import Image
import base64
from io import BytesIO
import io
from openai import OpenAI
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

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
    
def get_efcy_using_openai(efcy_data):
    respone = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role":"system",
                "content":"당신은 약의 효능정보를 요약해주는 사람입니다. 다음 약 효능 정보를 두세 단어로 요약한 뒤 반환해주세요"
            },
            {
                "role":"user",
                "content":efcy_data
            }
        ],
        temperature=0.5,
        max_tokens=100,
        n=1,
    )
    return (respone.choices[0].message.content).strip()

def get_efcy_using_openai_custom(efcy_data,efcy):
    respone = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role":"system",
                "content":"당신은 약의 효능정보를 요약해주는 사람입니다. 입력받은 약 효능 정보를 두세 단어로 요약한 뒤 반환해주세요."
            },
            {
                "role":"user",
                "content":f"효능정보 {efcy_data}를 키워드 {efcy}를 반드시 넣어서 두세 단어로 요약한 뒤 반환해주세요"
            }
        ],
        temperature=0.5,
        max_tokens=100,
        n=1,
    )
    return (respone.choices[0].message.content).strip()

def opening_hours(start,end):
    if start is None or end is None:
        return 'Closed'
    data = start + '~' + end
    return data