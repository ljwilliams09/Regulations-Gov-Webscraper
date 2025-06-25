import csv
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
            

def write_header(filename):
    """
    Appends a header row to a CSV file with predefined column names.

    Parameters:
        filename (str): The path to the CSV file where the header will be written.

    Notes:
        - If the file already exists, the header will be appended to the end of the file.
        - The header includes the following columns: "id", "title", "affiliation", "comment", "attachment_summary".
    """
    with open(filename, 'a') as r:
            writer = csv.writer(r)
            writer.writerow(["id", "title", "affiliation", "comment", "attachment_summary"])

def clean(comment):
    """
    Replaces carriage return ('\r') and newline ('\n') characters in the input string with spaces.

    Args:
        comment (str): The input string to be cleaned.

    Returns:
        str: The cleaned string with all '\r' and '\n' characters replaced by spaces.
    """
    return comment.replace('\r', ' ').replace('\n', ' ')
    
