from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

def process_query(query:str):
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query)
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])
    SYSTEM_PROMPT = f"""
        You are a helpful AI Assistant who answers user query based in the available context retrieved from a PDF file along with page_contents and page number.

        You should only answer the user based on the following context and navigate the user to open the right page number to know more.

        Context:
        {context}
    """

    response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages= [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )
    print(f"🤖: {response.choices[0].message.content}")
    return response.choices[0].message.content