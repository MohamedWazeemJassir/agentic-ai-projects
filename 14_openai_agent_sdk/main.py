from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool
import os

load_dotenv()

base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
api_key=os.getenv("GEMINI_API_KEY")

# Define an agent
hello_agent = Agent(
    name="Hello World Agent",
    instructions="You're an agent which greets the user and helps them ans using emoijis and in funny way",
    tools=[
        WebSearchTool()
    ]
)

result = Runner.run_sync(hello_agent, "Hey There, My name is Wazeem")

print(result.final_output)