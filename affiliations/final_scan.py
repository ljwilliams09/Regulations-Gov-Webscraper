import openai
import os
from dotenv import load_dotenv

def result():
    load_dotenv()
    client = openai.OpenAI(os.getenv("OPENAI_API_KEY"))