from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from os import getenv
load_dotenv()

client = OpenAI(
    api_key=getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("\n\nChatbot Node", state)
    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            { "role": "user", "content": state.get("user_query") }
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("\n\nEvaluate Node", state)
    # TODO: Evaluate whether this response is true or not using API call
    if False:
        return "endnode"

    return "chatbot_gemini"

def chatbot_gemini(state: State):
    print("\n\nChatbot Gemini Node", state)
    response = client.chat.completions.create(
        model="gemini-3.5-flash",
        messages=[
            { "role": "user", "content": state.get("user_query") }
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def endnode(state: State):
    print("\n\nEndnode Node", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, what is 2 + 2"}))
print(updated_state)