from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os, json
from neo4j import GraphDatabase
 
driver = GraphDatabase.driver(
    os.getenv("NEO_CONNECT_URI"),
    auth=(os.getenv("NEO_USERNAME"), os.getenv("NEO_PASSWORD"))
)
 
def save_graph(user, message):
    with driver.session() as session:
        session.run(
            """
            MERGE (u:User {id:$user})
            MERGE (m:Message {text:$message})
            MERGE (u)-[:SAID]->(m)
            """,
            user=user,
            message=message
        )

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": { "api_key": GEMINI_API_KEY, "model": "gemini-embedding-001", "embedding_dims": 1536 }
    },
    "llm": {
        "provider": "gemini",
        "config": { "api_key": GEMINI_API_KEY, "model": "gemini-3.5-flash" }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("> ")

    search_memory = mem_client.search(query=user_query, filters={'user_id':"waz"})
    save_graph("waz", user_query)

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]

    print("Found Memories", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content
    print("AI:", ai_response)

    mem_client.add(
        user_id='waz',
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )
    print("Memory has been saved...")