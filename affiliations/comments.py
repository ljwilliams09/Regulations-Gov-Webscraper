import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import html
import time

def client(comment, title, summary, potent, organization=""):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Does this following comment, title, attachment summary, potential affiliation, and organization indicate the affiliation of the commenter? Only provide the affiliation if yes, and N/A if not. Title: {title}. Organization: {organization}. Comment: {comment}. Summary:{summary}. Potential Affiliation: {potent}"

    response = client.chat.completions.create(
        model="o4-mini",
        messages = [{
            "role" : "user",
            "content" : prompt
        }]
    )
    return response.choices[0].message.content.strip()

def scan(comment_id, summary, potent):
    regulations_api = os.getenv("REG_GOV_API_KEY_AB")
    params = {
        "api_key" : regulations_api
    }
    while True:
        url = "https://api.regulations.gov/v4/comments/" + comment_id
        response = requests.get(url, params=params)

        if response.status_code != 200:
            if response.status_code == 429:
                time.sleep(3600)
            else:
                raise Exception ("Failed to access the comments page")
        else:
            break
    data = response.json()["data"]["attributes"]
        
    organization = data["organization"]
    comment = html.unescape(data["comment"])
    title = data["title"]
    if organization is not None:
        return comment, client(comment, title, summary, potent, organization)

    return comment, client(comment, title, summary, potent)

