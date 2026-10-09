from google.adk.agents import Agent
from google.adk.tools import google_search
import requests

def greet(greeting: str) -> dict:
    return {"status": "success", "greeting": greeting}

def get_weather(city: str, unit: str):
    """
    Retrieves the weather for a city in the specified unit.

    Args:
        city (str): The city name.
        unit (str): The temperature unit, either 'Celsius' or 'Fahrenheit'.
    """
    # ... function logic ...
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code==200:
        return {"status": "success", "report": f"Weather for {city} is {response.text}."}
    return "Someting went wrong..."

root_agent = Agent(
    model='gemini-3.5-flash',
    name='hello_world',
    description='Hello World Agent',
    instruction="You're an agent which greets the user and helps them ans using emoijis and in funny way.",
    tools=[
        greet, 
        # google_search,
        get_weather
        ],
)
