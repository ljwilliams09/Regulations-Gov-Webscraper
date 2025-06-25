import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import time
import helpers as h

def scan(comment_id):
    """
    Fetches and returns details of a comment from the Regulations.gov API given a comment ID.

    This function retrieves the title, comment text, organization, and government agency associated with a specific comment.
    It handles API rate limiting (HTTP 429) by waiting for an hour before retrying, and uses exponential backoff for other errors.
    If the maximum number of retries is exceeded or the response structure is unexpected, an exception is raised.

    Args:
        comment_id (str): The unique identifier for the comment to retrieve.

    Returns:
        tuple: A tuple containing the comment's title (str), comment text (str), organization (str or None), and government agency (str or None).

    Raises:
        Exception: If the API cannot be accessed after the maximum number of retries, or if the response structure is invalid.
    """
    load_dotenv()
    regulations_api = os.getenv("REG_GOV_API_KEY_AB")
    params = {
        "api_key": regulations_api
    }
    url = "https://api.regulations.gov/v4/comments/" + comment_id
    retries = 0
    max_retries = 3

    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            time.sleep(3600)
        else:
            retries += 1
            if retries >= max_retries:
                raise Exception("Failed to access the comments page after 3 retries")
            time.sleep(2 ** retries)  # exponential backoff

    try:
        data = response.json()["data"]["attributes"]
    except (KeyError, ValueError, TypeError) as e:
        raise Exception("Unexpected response structure or invalid JSON") from e


    return h.clean(data["title"]),h.clean(data["comment"]),h.clean(data["organization"]),h.clean(data["govAgency"])

