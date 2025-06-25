import os
import requests
from dotenv import load_dotenv
import time
load_dotenv()

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
