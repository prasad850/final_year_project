import os 
from groq import Groq 
from dotenv import load_dotenv


load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"

def generate(prompt: str, json_mode: bool= False, temperature:float=0.2) -> str:
    """Send a prompt to Groq and return the text response."""
    kwargs = {
        "model":MODEL,
        "messages":[{"role":"user", "content": prompt}],
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"]={"type":"json_object"}

    response =_client.chat.completions.create(**kwargs)
    return response.choices[0].message.content