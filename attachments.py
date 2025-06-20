import os
from dotenv import load_dotenv
import csv
from networkx import NodeNotFound
from openai import OpenAI
import requests
load_dotenv()

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

def attachments(attachment_link):
    response = requests.get(attachment_link)
    if response.status_code != 200:
        raise Exception(f"Failed to download the attachment for the link {attachment_link}")
    
    file = "temp_attachment.pdf"

    with open(file, "wb") as f:
        f.write(response.content)
    
    result = client(file)
    try:
        os.remove(file)
    except FileNotFoundError:    
        print("File could not be located and deleted")
    return result
    