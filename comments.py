import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

def client(comment):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""
        Does this following comment indicate the affiliation of the commenter? Only provide the affiliation if Yes, and N/A if not.
        {comment}
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages = [{
            "role" : "user",
            "content" : prompt
        }],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def scan(comment_id):
    regulations_api = os.getenv("REG_GOV_API_KEY")
    base_url = "https://api.regulations.gov/v4/comments/"
    params = {
        "api_key" : regulations_api
    }
    url = base_url + comment_id
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception ("Failed to access the comments page")
    
    organization = (response.json())["data"]["attributes"]["organization"]
    if organization is not None:
        return organization

    return client((response.json())["data"]["attributes"]["comment"])
