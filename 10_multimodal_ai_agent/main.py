from openai import OpenAI
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

uploaded_file = client.files.upload(file="./image.jpg")

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=[
        {"type": "text", "text": "Describe this image."},
        {
            "type": "image",
            "uri": uploaded_file.uri,
            "mime_type": uploaded_file.mime_type
        }
    ]
)
print(interaction.output_text)
