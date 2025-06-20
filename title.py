from openai import OpenAI
import os
import csv
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("CHAT_API_KEY"))

def scan(comment_title):
    prompt = f"""Does the following comment title contain an affiliation or organization for the commenter? Only respond with the affiliation if Yes, or -1 if no. Be mindful that the commenter might be including the rules ID in their comment and it is not their affiliation

    Title: {comment_title}
    """
    response = client.chat.completions.create(model="gpt-4.1",
    messages=[{
        "role":"user",
        "content" : prompt
        }],
    temperature=0)
    return response.choices[0].message.content.strip()
