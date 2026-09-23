from glob import glob
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key = api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def image_quiz(image_path):
    base64_image = encode_image(image_path)
    quiz_prompt = """
    제공한 이미지를 바탕으로, 다음과 같은 양식으로 퀴즈를 만들어줘.
    정답은 (1)~(4) 중 하나만 해당하도록 출제해.
    아래는 예시야.
    -----예시-----

    Q: 다음 이미지에 대한 설명 중 옳지 않은 것은 무엇인가요?
    - (1) 베이커리에서 사람들이 빵을 사는 모습이 담겨 있습니다.
    - (2) 맨 앞에 서 있는 사람은 빨간색 셔츠를 입었습니다.
    - (3) 기차를 타기 위해 줄을 서 있는 사람들이 있습니다.
    - (4) 점원은 노란색 티셔츠를 입었습니다.

    정답: (4) 점원은 노란색 티셔츠가 아닌 파란색 티셔츠를 입었습니다.
    (주의: 정답은 (1)~(4) 중 하나만 선택하도록 출제하세요.)
    =====
    """

    messages = [
        {
            "role":"user",
            "content":[
                {"type":"text", "text": quiz_prompt},
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
        model = "gpt-4o",
        messages=messages
    )

    return response.choices[0].message.content

q = image_quiz("./cafe02.jpg")
print("테스트용 한 문제 출력:")
print(q)

# 여러 이미지와 관련된 문제를 생성하고, 그 결과를 문제집으로 만드는 코드
txt = ''
no = 1
for g in glob('./images/*.jpg'): #하위 폴더 images폴더를 만들어서, 내부에 jpg 파일들 준비하기
    try:
        q = image_quiz(g)
    except Exception as e:
        print(e)
        continue

    divider = f'## 문제 {no}\n\n'
    print(divider)

    txt += divider
    filename = os.path.basename(g)
    txt += f'![image]({filename})\n\n'

    #문제 추가
    print(q)
    txt += q + '\n\n-------------------\n\n'

    with open('./images/image_quiz.md', 'w', encoding = 'utf-8') as f:
        f.write(txt)

    no += 1 #문제 번호 증가
