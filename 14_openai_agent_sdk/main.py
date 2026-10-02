from dotenv import load_dotenv
import requests
from agents import Agent, Runner, WebSearchTool, function_tool
import os

load_dotenv()

@function_tool()
def get_weather(city: str):
    """Fetch the weather for a given city name.
    Args:
        city: The city name to fetch the weather for
    """
    
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"


base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
api_key=os.getenv("GEMINI_API_KEY")

# Define an agent
hello_agent = Agent(
    name="Hello World Agent",
    instructions="You're an agent which greets the user and helps them ans using emoijis and in funny way",
    tools=[
        WebSearchTool(),
        get_weather
    ]
)

result = Runner.run_sync(hello_agent, "Hey There, My name is Wazeem")

print(result.final_output)