from google.adk.agents.llm_agent import Agent

def get_current_time(greeting: str) -> dict:
    return {"status": "success", "greeting": greeting}

root_agent = Agent(
    model='gemini-3.5-flash',
    name='hello_world',
    description='Hello World Agent',
    instruction="You're an agent which greets the user and helps them ans using emoijis and in funny way",
)

# result = 