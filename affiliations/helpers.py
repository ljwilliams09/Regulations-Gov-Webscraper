import os
import requests
from dotenv import load_dotenv


load_dotenv()

def linker(comment_id):
    url = f"https://api.regulations.gov/v4/comments/{comment_id}/attachments" 
    params = {
        "api_key" : os.getenv("REG_GOV_API_KEY_LW")
    }
    while True:
        link_page = requests.get(url, params=params)
        if link_page.status_code != 200:
            if link_page.status_code == 429:
                time.sleep(3600)
                continue
            raise Exception(f"Failed to access the link page for the comment {comment_id}, with status code {link_page.status_code}: ")
        else:
            break
    data = link_page.json()
    if not data["data"]:
        return  "N/A"
    
    return (link_page.json())["data"][0]["attributes"]["fileFormats"][0]["fileUrl"]