import os
from dotenv import load_dotenv
import csv
from openai import OpenAI
import requests
load_dotenv()

def linker(comment_id):
    url = "https://api.regulations.gov/v4/comments/" + comment_id
    params = {
        "api_key" : "RWhAaanqXHMC89fGk755BO70rN8ygv1txMawAG3a"
    }

    comment_page = requests.get(url, params=params) # get the comment
    if comment_page.status_code != 200:
        raise Exception(f"Failed to access the comment page for the comment {comment_id}, with staus code {comment_page.status_code}")
    
    link = (comment_page.json())["relationships"]["attachments"]["links"]["related"]

    link_page = requests.get(link, params=params)
    if link_page.status_code != 200:
            raise Exception(f"Failed to access the link page for the comment {comment_id}, with status code {link_page.status_code}")
    
    attachment = (link_page.json())["data"]["fileFormats"]["file_url"]

    return attachment

def client(filename):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    file = client.files.create(
        file=open(filename, "rb"),
        purpose="user_data"
    )
    response = client.responses.create(
        model='gpt-4.1',
        input=[
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "input_file",
                        "file_id" : file.id
                    },
                    {
                        "type" : "input_text",
                        "text" : "What is the affiliation, if any, of the author(s) of this document? Only respond with the affiliation, and -1 if there seems to be no affiliation."
                    }
                ]
            }
        ]
    )
    return response.output_text

def scan(comment_id):
    attachment = linker(comment_id)

    response = requests.get(attachment)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch attachment for comment {comment_id}")

    file = "temp_attachment.pdf"

    with open(file, "wb") as f:
        f.write(____.content)
    
    result = client(file)
    try:
        os.remove(file)
    except FileNotFoundError:    
        print("File could not be located and deleted")
    print(result)
    return result