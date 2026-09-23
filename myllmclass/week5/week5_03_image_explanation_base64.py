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

image_path = "./example01.jpg"

base64_image = encode_image(image_path)

print("base64 형식의 이미지: "+base64_image)

messages = [
    {
        "role": "user",
        "content":[
            {"type": "text", "text": "이 이미지에 대해 구체적으로 설명해."},
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{base64_image}",
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
