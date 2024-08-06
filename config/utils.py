from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    
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