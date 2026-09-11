# Zero Shot Prompting: Directly giving a direct question or task without prior examples.
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "You should one and only answer coding related questions. You shouldn't answer anything else. Your name is Alexa.If user asks something other than coding, just say sorry."

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "How to print something in terminal in dart"
        }
    ]
)

print(response.choices[0].message.content)