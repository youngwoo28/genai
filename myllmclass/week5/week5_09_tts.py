from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key = api_key)

#TTS 함수 사용

response = client.audio.speech.create(
    model = "tts-1-hd",
    voice = "shimmer",
    input = "Hello world! This is TTS test.",
)

response.write_to_file("hello_world.mp3")


#ipynb 사용시 창에 다음 코드로 바로 음성 띄우기 가능
'''
import IPython.display as ipd

ipd.Audio("hello_world.mp3")
'''

import json

#json 파일 열기
with open("./images/image_quiz_eng.json", "r", encoding = 'utf-8') as f:
    eng_dict = json.load(f)

print("eng_dict 내용 출력: ")
print(eng_dict)


voices = ['alloy', 'ash', 'coral', 'echo', 'fable', 'onyx', 'nova', 'sage', 'shimmer']

for q in eng_dict:
    no = q['no']
    quiz = q['eng']
    quiz = quiz.replace("- (1)", "- One.\t")#음성으로 읽기 위해 해당 기호를 대체함
    quiz = quiz.replace("- (2)", "- Two.\t")
    quiz = quiz.replace("- (3)", "- Three.\t")
    quiz = quiz.replace("- (4)", "- Four.\t")

    print("수정된 문제 출력: ")
    print(no, quiz)

    voice = voices[no%len(voices)] #문제 번호마다 목소리가 달라지게 지정

    response = client.audio.speech.create(
        model = "tts-1-hd" ,
        voice = voice,
        input = f"#{no}. {quiz}",
    )

    response.write_to_file(f"./audio/{no}.mp3")
