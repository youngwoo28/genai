from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key = api_key)

audio_file_path = "./example.mp3"

with open(audio_file_path, 'rb') as audio_file:
    transcription = client.audio.transcriptions.create(
        model = "whisper-1",
        file = audio_file
    )

text_file_path = "mp3_to_txt.txt"

with open(text_file_path, "w", encoding="utf-8") as text_file:
    text_file.write(transcription.text)

print(f"저장 완료: {text_file_path}")
