from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key = api_key)

messages = [
    {
        "role": "user",
        "content":[
            {"type": "text", "text": "이 이미지에 대해 구체적으로 설명해."},
            {
                "type":"image_url",
                "image_url":{
                    "url": "https://www.dongyang.ac.kr/sites/dmu/images/sub/char2-1.png",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = messages
)

print("응답: "+response.choices[0].message.content)
