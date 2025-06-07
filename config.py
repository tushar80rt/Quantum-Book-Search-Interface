import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='api.env')

def get_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing in environment variables.")
    return api_key
