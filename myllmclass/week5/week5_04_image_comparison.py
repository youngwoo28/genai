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

image1 = encode_image("./cafe01.jpg")
image2 = encode_image("./cafe02.jpg")

messages = [
    {
        "role": "user",
        "content":[
            {"type": "text", "text": "두 사진의 차이점을 설명해."},
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
