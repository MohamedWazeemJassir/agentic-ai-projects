import asyncio
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import speech_recognition as sr
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Speak Something...")
        audio = r.listen(source)

        print("Processing Audio... (STT)")
        stt = r.recognize_google(audio)

        print("You Said:", stt)

        SYSTEM_PROMPT = f"""
            You're an expert voice agent. You are given the transcript of what user has said using voice.
            You need to output as if you are an voice agent and whatever you speak will be converted back
            to audio using AI anad played back to user.
        """

        response = client.chat.completions.create(
            model="gemini-3.5-flash",
            messages=[
                { "role": "system", "content": SYSTEM_PROMPT },
                { "role": "user", "content": stt }
            ]
        )

        print("AI Response:", response.choices[0].message.content)
        audio = elevenlabs.text_to_speech.convert(
            text=response.choices[0].message.content,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_v3",
            output_format="mp3_44100_128",
        )

        play(audio)
main()