from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key = api_key)

audio_file_path = "../week4/example.mp3"

with open(audio_file_path, 'rb') as audio_file:
    transcription = client.audio.translations.create(
        model = "whisper-1",
        file = audio_file
    )

print(transcription)
