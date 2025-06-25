import os
import requests
from dotenv import load_dotenv
import time


load_dotenv()

# def linker(comment_id):
#     url = f"https://api.regulations.gov/v4/comments/{comment_id}/attachments" 
#     params = {
#         "api_key" : os.getenv("REG_GOV_API_KEY_LW")
#     }
#     while True:
#         link_page = requests.get(url, params=params)
#         if link_page.status_code != 200:
#             if link_page.status_code == 429:
#                 time.sleep(3600)
#                 continue
#             raise Exception(f"Failed to access the link page for the comment {comment_id}, with status code {link_page.status_code}: ")
#         else:
#             break
#     data = link_page.json()
#     if not data["data"]:
#         return  "N/A"
#     print((link_page.json())["data"][0]["attributes"]["fileFormats"])
#     # return (link_page.json())["data"][0]["attributes"]["fileFormats"][0]["fileUrl"]


def linker(comment_id):
    """
    Determines the number of sequential PDF attachments available for a given comment.

    This function attempts to download attachments for the specified comment ID from
    the Regulations.gov downloads endpoint, incrementing the attachment number until
    a non-200 HTTP response is received. It returns the count of successfully found
    attachments (i.e., the highest attachment number with a valid PDF).

    Args:
        comment_id (str): The ID of the comment to check for attachments.

    Returns:
        int: The number of available PDF attachments for the comment.
    """
    attachment_number = 0
    retries = 3
    wait = 1
    while True:
        attachment_number += 1
        url = f"https://downloads.regulations.gov/{comment_id}/attachment_{attachment_number}.pdf"

        for attempt in range(retries):
            response = requests.get(url)
            if response.status_code == 200:
                break
            elif attempt < retries - 1:
                time.sleep(wait * (2 ** attempt)) # exponential backoff
            else:
                return attachment_number - 1
    
print(linker("FWS-R6-ES-2016-0042-5397"))
