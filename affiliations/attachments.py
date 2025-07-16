from openai import OpenAI
import os
import requests
import time
import helpers
import json
from logger_affil import logger
from pypdf import PdfWriter, PdfReader

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
    with open("./config.json", 'r') as f:
        config = json.load(f)

    text = """
    You are given a comment from Regulations.gov. Your task is to:

    1. If the document is supporting material to the comment, only return `-1`.
    2. Extract the affiliation if possible, if there is none, only return `None`.

    Respond as:
   <affiliation>

    Examples:
    - National Farmers Union
    - -1
    - None

    """

    response = client.responses.create(
        model=config["attachment_model"],
        input=[
            {
                "role": "system",
                "content": "You are an analyst that only responds in the format asked for."
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
        ],
        temperature=0
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

def trim_attachment(file, num_pages=2):
    """
    Trims a PDF file to retain only the first and last `num_pages` pages.

    This function reads a PDF file, keeps the first `num_pages` pages and the last `num_pages` pages,
    and overwrites the original file with the trimmed version. If the PDF has fewer than
    `2 * num_pages` pages, overlapping pages will not be duplicated.

    Args:
        file (str or file-like object): Path to the PDF file or a file-like object to be trimmed.
        num_pages (int, optional): Number of pages to keep from the start and end of the PDF. Defaults to 5.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PyPDF2.errors.PdfReadError: If the file is not a valid PDF.
    """
    reader = PdfReader(file)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    for i in range(min(num_pages, total_pages)):
        writer.add_page(reader.pages[i])

    start_last = max(total_pages - num_pages, num_pages)
    for i in range(start_last, total_pages):
        writer.add_page(reader.pages[i])

    with open(file, "wb") as f:
        writer.write(f)



def scan(comment_id):
    attachments = helpers.linker(comment_id)
    filename = "temp_attachment.pdf"
    if attachments == 0:
        return None, None
   
    for attachment in range(attachments):
        response = get_attachment(comment_id, attachment+1)
        with open(filename, "wb") as f:
            f.write(response.content)
        trim_attachment(filename)
        gpt_response = client(filename)
        try:
            os.remove(filename)
        except FileNotFoundError:    
           logger.error("File could not be deleted")

        if gpt_response[0] == '-1':
            continue
        results = gpt_response.split('```')
        return results[0], results[1]

    return None, None
