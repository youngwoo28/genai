from openai import OpenAI
from dotenv import load_dotenv
#정의한 함수들 모두 포함해주기
from week6_10_gpt_functions_more import get_current_time, tools, get_yf_stock_info
from week6_10_gpt_functions_more import get_yf_stock_history, get_yf_stock_recommendations
import os
import json
import streamlit as st

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

st.title("주식도 잘 알려주는 챗봇")

#초기 시스템 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"system",
         "content":"너는 사용자를 도와주는 상담사야."
        },
    ]

for msg in st.session_state.messages:
    #불필요한 출력을 없애기 위해 assistant, user만 출력
    #if msg["role"] == "assistant" or msg["role"] == "user":
    #어떤 함수를 호출했는지 확인하기 위해 전체 내용을 띄움
    st.chat_message(msg["role"]).write(msg["content"])


if user_input := st.chat_input():
    st.session_state.messages.append({"role":"user", "content":user_input})
    st.chat_message("user").write(user_input)

    ai_response = get_ai_response(st.session_state.messages, tools=tools)  # AI 응답 생성
    ai_message = ai_response.choices[0].message
    print(ai_message)  # 응답 객체 전체 출력(디버깅용)

    tool_calls = ai_message.tool_calls  # 툴 호출 여부 확인
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name  # 호출된 함수 이름
            tool_call_id = tool_call.id  # 호출 ID

            arguments = json.loads(tool_call.function.arguments)

            # 시간 함수 호출 시 처리
            if tool_name == "get_current_time":
                func_result = get_current_time(timezone=arguments['timezone'])

            elif tool_name == "get_yf_stock_info":
                func_result = get_yf_stock_info(ticker=arguments['ticker'])

            elif tool_name == "get_yf_stock_history":
                func_result = get_yf_stock_history(
                    ticker=arguments['ticker'],
                    period=arguments['period']
                )

            elif tool_name == "get_yf_stock_recommendations":
                func_result = get_yf_stock_recommendations(
                    ticker=arguments['ticker']
                )

            st.session_state.messages.append({
                "role":"function",
                "tool_call_id":tool_call_id,
                "name":tool_name,
                "content":func_result,
            })

        st.session_state.messages.append({"role":"system", "content":"이제 주어진 결과를 바탕으로 답변할 차례다."})

        ai_response = get_ai_response(st.session_state.messages)  # 도구 결과 반영 후 재응답
        ai_message = ai_response.choices[0].message

    st.session_state.messages.append({
        "role":"assistant",
        "content":ai_message.content

    })

    print("AI\t:", ai_message.content)  # AI의 메시지 출력
    st.chat_message("assistant").write(ai_message.content)
