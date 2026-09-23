from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key = api_key)

import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

image1 = encode_image("./oecd_rnd_2021.png")
image2 = encode_image("./oecd_rnd_2022.png")

messages = [
    {
        "role": "user",
        "content":[
            {"type": "text", "text": "첫 번째 이미지는 2021년도 데이터이고, 두 번째 이미지는 2022년도 데이터야. 이 데이터에 대해 설명해줘. 어떤 변화가 있었어? 한국 데이터를 중심으로 설명해."},
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{image1}",
                },
            },
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{image2}",
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
