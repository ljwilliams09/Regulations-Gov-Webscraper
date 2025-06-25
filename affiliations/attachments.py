from openai import OpenAI
import os
import requests
import time
import helpers

def client(filename):
    """
    Uploads a file to the OpenAI API and analyzes its content to determine if it is a comment or supporting material for a comment on regulations.gov.
    If the file is identified as the actual comment, returns a summary of the comment and the affiliation of the commenter, separated by '|||'.
    If the file is identified as supporting material, returns -1.
    Args:
        filename (str): The path to the file to be uploaded and analyzed.
    Returns:
        str: A summary and affiliation separated by '$$$', or -1 if the file is supporting material.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    file = client.files.create(
        file=open(filename, "rb"),
        purpose="user_data"
    )

    text = (
    "You are a data analyst. Only return structured output in one of the following formats:\n\n"
    "1. If the file is supporting material (e.g., a technical report, appendix, or non-commentary attachment), return:\n"
    "-1\n\n"
    "2. If the file is a direct comment on a regulation, return:\n"
    "<summary of the comment in 1–2 sentences>|||<affiliation of the commenter>\n\n"
    "Rules:\n"
    "- The summary should capture the main point or position of the comment.\n"
    "- The affiliation should reflect the organization the commenter belongs to, if known.\n"
    "- If the commenter provides no explicit affiliation, but an organization is present in the email header (e.g., 'From: Earthjustice'), use that as their affiliation.\n"
    "- If there is no explicit or implied affiliation, return 'None' for affiliation.\n"
    "- Do not include any explanations or extra commentary — return only the structured output.\n\n"
    "Format: summary|||affiliation\n"
    )   


    response = client.responses.create(
    model='gpt-4.1',
    input=[
        {
            "role": "system",
            "content": "You are a data analyst that strictly returns structured outputs, no explanations."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": text
                },
                {
                    "type": "input_file",
                    "file_id": file.id
                }
            ]
        }
    ]
    )
    return response.output_text

def get_attachment(comment_id, attachment):
    """
    Attempts to download a PDF attachment for a given comment from regulations.gov.

    Args:
        comment_id (str): The unique identifier for the comment.
        attachments (list): A list of attachment identifiers (not used in current implementation).

    Returns:
        requests.Response: The HTTP response object containing the PDF attachment if successful.

    Raises:
        Exception: If the attachment cannot be accessed after the maximum number of retries.

    Notes:
        - Implements exponential backoff on failure.
        - Waits for 1 hour if rate limited (HTTP 429).
    """
    url = f"https://downloads.regulations.gov/{comment_id}/attachment_{attachment}.pdf"
    retries = 0
    max_retries = 3

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response           
        elif response.status_code == 429:
            time.sleep(3600)
        else:
            retries += 1
            if retries >= max_retries:
                raise Exception("Failed to access the comments page after 3 retries")
            time.sleep(2 ** retries) # exponential backoff


def scan(comment_id):
    attachments = helpers.linker(comment_id)
    filename = "temp_attachment.pdf"
    if attachments == 0:
        return None, None
   
    for attachment in range(attachments):
        response = get_attachment(comment_id, attachment+1)
        with open(filename, "wb") as f:
            f.write(response.content)

        gpt_response = client(filename)
        try:
            os.remove(filename)
        except FileNotFoundError:    
            print("File could not be located and deleted")
        
        if gpt_response == -1:
            continue
        results = gpt_response.split('|||')
        return results[0], results[1]
        
    return None, None

