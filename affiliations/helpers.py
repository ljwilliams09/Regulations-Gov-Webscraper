import html
import requests
import time

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
    while True:
        attachment_number += 1
        url = f"https://downloads.regulations.gov/{comment_id}/attachment_{attachment_number}.pdf"

        for attempt in range(retries):
            response = requests.get(url)
            if response.status_code == 200:
                break
            elif attempt < retries - 1:
                time.sleep(2 ** attempt) # exponential backoff
            else:
                return attachment_number - 1


def clean(text):
    """
    Cleans a given text string by unescaping HTML entities and replacing carriage returns and newlines with spaces.

    Args:
        text (str or None): The input text to clean. Can be None.

    Returns:
        str or None: The cleaned text with HTML entities unescaped and line breaks replaced by spaces, or None if input is None.
    """
    if text == None:
        return None
    return html.unescape(text).replace('\r', ' ').replace('\n', ' ')
    
