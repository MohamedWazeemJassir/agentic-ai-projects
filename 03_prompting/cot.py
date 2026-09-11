# Chain Of Thought Prompting - Making the model think before producing output
from dotenv import load_dotenv
from openai import OpenAI
import json, os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can
    be multiple times) and finally OUTPUT (which is going to be displayed to 
    the user).

    Output JSON format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

    Example:
    START: Hey, can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is the correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10 = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    PLAN: { "step": "OUTPUT": "content": "3.5" }
"""

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    response_format= {"type": "json_object"},
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        # Manually keep adding messages to History
        { "role": "assistant", "content": json.dumps({
            "step": "PLAN",
            "content": "The user wants a JavaScript function to add 'n' numbers. I need to consider modern JavaScript syntax like rest parameters (...numbers) and array helper methods like reduce."
            })
        },
        { "role": "assistant", "content": json.dumps({
            "step": "PLAN",
            "content": "I will create a flexible JavaScript function using rest parameters (`...numbers`) so it can accept any number of arguments, and use the `reduce` method to calculate the sum."
            })
        },
        { "role": "user", "content": "Hey, write a code to add n numbers in js"},
    ]
)

print(response.choices[0].message.content)