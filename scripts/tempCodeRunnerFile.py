
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load the API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Initialize the Groq model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

try:
    # Send a test question
    response = llm.invoke("Hi, how are you?")

    print("API key is working!")
    print("Model response:")
    print(response.content)

except Exception as e:
    print("Groq API request failed.")
    print("Error:", e)
