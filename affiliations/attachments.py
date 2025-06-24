from openai import OpenAI
import os
import requests

def linker(comment_id):
    url = "https://api.regulations.gov/v4/comments/" + comment_id
    params = {
        "api_key" : "RWhAaanqXHMC89fGk755BO70rN8ygv1txMawAG3a"
    }

    comment_page = requests.get(url, params=params) # get the comment
    if comment_page.status_code != 200:
        raise Exception(f"Failed to access the comment page for the comment {comment_id}, with staus code {comment_page.status_code}")
    
    link = (comment_page.json())["data"]["relationships"]["attachments"]["links"]["related"]

    link_page = requests.get(link, params=params)
    if link_page.status_code != 200:
            raise Exception(f"Failed to access the link page for the comment {comment_id}, with status code {link_page.status_code}")

    data = link_page.json()
    if not data["data"]:
        return  "N/A" 
    
    return (link_page.json())["data"][0]["attributes"]["fileFormats"][0]["fileUrl"]


def client(filename, found):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    file = client.files.create(
        file=open(filename, "rb"),
        purpose="user_data"
    )
    found_text = "If the document is eligible, return a summary of the document. If not, say the summary is INELIGBLE."

    not_found_text = "If the document is eligible, return a summary of the document. If not, say the summary is INELIGBLE. Additionally, what is the affiliation, if any, of the author(s) of this document. Either give the affiliation, N/A if there seems to be no affiliation, or INELIGIBLE if it is ineligible. Give the result in this format: summary,affiliation"
    if found:
        temp = found_text
    else:
        temp = not_found_text

    response = client.responses.create(
        model='o4-min',
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
                        "text" : temp
                    }
                ]
            }
        ]
    )
    return response.output_text

def scan(comment_id, found):
    attachment = linker(comment_id)
    if attachment == "N/A":
        return "N/A"

    response = requests.get(attachment)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch attachment for comment {comment_id}")

    file = "temp_attachment.pdf"

    with open(file, "wb") as f:
        f.write(response.content)
    
    result = client(file, found)
    try:
        os.remove(file)
    except FileNotFoundError:    
        print("File could not be located and deleted")
  
    return result
