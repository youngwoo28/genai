from openai import OpenAI
from dotenv import load_dotenv
from week6_03_gpt_functions_pytz import get_current_time, tools
import os
###추가
import json

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=api_key)

# AI 응답 생성 함수
def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    return response

# 초기 시스템 메시지 설정
messages = [
    {"role": "system", "content": "너는 사용자를 도와주는 상담사야."},
]

# 사용자와의 대화 루프
while True:
    user_input = input("사용자\t: ")  # 사용자 입력
    if user_input == "exit":
        break  # 'exit' 입력 시 종료

    messages.append({"role": "user", "content": user_input})  # 대화 기록에 추가

    ai_response = get_ai_response(messages, tools=tools)  # AI 응답 생성
    ai_message = ai_response.choices[0].message
    print(ai_message)  # 응답 객체 전체 출력(디버깅용)

    tool_calls = ai_message.tool_calls  # 툴 호출 여부 확인
    if tool_calls:
        tool_name = tool_calls[0].function.name  # 호출된 함수 이름
        tool_call_id = tool_calls[0].id  # 호출 ID

        ###추가
        arguments = json.loads(tool_calls[0].function.arguments)

        # 시간 함수 호출 시 처리
        if tool_name == "get_current_time":
            messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": get_current_time(timezone = arguments['timezone']),  ###파라미터 추가
            })

        ai_response = get_ai_response(messages, tools=tools)  # 도구 결과 반영 후 재응답
        ai_message = ai_response.choices[0].message

    messages.append(ai_message)  # 최종 응답 대화에 추가
    print("AI\t:", ai_message.content)  # AI의 메시지 출력
