from openai import OpenAI
import os
import requests
import time
import helpers

def client(filename):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    file = client.files.create(
        file=open(filename, "rb"),
        purpose="user_data"
    )

    text = "If the document is eligible, return a summary of the document. If not, say the summary is INELIGBLE. Additionally, what is the affiliation, if any, of the author(s) of this document. Either give the affiliation, N/A if there seems to be no affiliation, or INELIGIBLE if it is ineligible. Give just the result of the as summmary and affiliation delinated by '|||'"
  
    response = client.responses.create(
        model='o4-mini',
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
                        "text" : text
                    }
                ]
            }
        ]
    )
    return response.output_text

def scan(comment_id):
    attachment = helpers.linker(comment_id)
    if attachment == "N/A":
        return "N/A","N/A"

    response = requests.get(attachment)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch attachment for comment {comment_id}")

    file = "temp_attachment.pdf"

    with open(file, "wb") as f:
        f.write(response.content)
    
    result = client(file).split('|||')
    try:
        os.remove(file)
    except FileNotFoundError:    
        print("File could not be located and deleted")
  
    return result[0], result[1]

