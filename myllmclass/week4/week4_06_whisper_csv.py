from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=api_key)

model_id = "whisper-1"
sample = "./example.mp3"  # 오디오 입력 sample(경로)

# OpenAI Whisper API 호출 결과를 result 변수에 저장
with open(sample, "rb") as audio_file:
    result = client.audio.transcriptions.create(
        model=model_id,
        file=audio_file,
        response_format="verbose_json",             # segment/word-level timestamp 포함
        timestamp_granularities=["word", "segment"]  # word/segment-level timestamps 모두 반환
    )

print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))

import pandas as pd

# segments에서 start, end를 반올림, 텍스트는 제대로 추출
start_end_text = []
for seg in result.segments:
    start = round(seg.start, 1)
    end = round(seg.end, 1)
    text = seg.text.strip()  # 앞뒤 공백 제거(불필요시 생략)
    start_end_text.append([start, end, text])

df = pd.DataFrame(start_end_text, columns=["start", "end", "text"])
# encoding='utf-8-sig' 옵션 추가(Excel, 한글 깨짐 방지)
df.to_csv("audio_example.csv", index=False, sep="|", encoding="utf-8-sig")
print(df)

# 이어붙인 텍스트: (글자가 깨지면 encoding 문제, print 만약 콘솔에서 깨지면 파일로 저장해서 확인)
full_text = "".join(df["text"].tolist())
print(full_text)
