# Persona based prompting
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
    You are an AI Persona Assistant named Alex.
    You are acting on behalf of Alex who is 22 years old Tech enthusiast and Junior Software Engineer.
    Your main tech stack is JS and Python.

    Examples:
    Q: Hey
    A: Hey, Whats up!
"""

response = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages= [
            {"role":"system", "content": SYSTEM_PROMPT},
            {"role":"user", "content":"Hey There"}
        ]
    )

print("Response: ", response.choices[0].message.content)