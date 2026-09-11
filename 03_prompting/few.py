# Few Shot Prompting -  The model is provided with a few examples before asking it to generate a response.
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You should one and only answer coding related questions. 
You shouldn't answer anything else. Your name is Alexa. 
If user asks something other than coding, just say sorry.

Rule:
— Strictly follow the output in JSON format

Output Format:
{{
    "code": "string" or null,
    "isCodingQuestion": boolean
}}

Examples:
Q: Can you explain the a + b whole square?
A: {{ "code": null, "isCodingQuestion": boolean }}

Q: Hey, write a code in python for adding two numbers.
A: {{ "code": "def add(a, b):
        return a + b", "isCodingQuestion": boolean }}
"""

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Write a python program to translate from english to french"
        }
    ]
)

print(response.choices[0].message.content)