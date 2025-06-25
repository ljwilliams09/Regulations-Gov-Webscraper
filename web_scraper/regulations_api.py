import requests
import csv
from datetime import datetime, timedelta
import json
import time
import os
from dotenv import load_dotenv



def get_next_time(progress="PROGRESS.txt"):
    """
    Reads the first line from the specified progress file and returns it as a stripped string.

    Args:
        progress (str): The path to the progress file. Defaults to "PROGRESS.txt".

    Returns:
        str: The first line of the file, with leading and trailing whitespace removed.
    """
    with open(progress, 'r') as file:
        return file.readline().strip()

def to_iso_format(time):
    """
    Converts an ISO 8601 formatted UTC time string to a formatted string in local time (UTC-4).

    Args:
        time (str): A time string in the format "%Y-%m-%dT%H:%M:%SZ" (e.g., "2023-06-01T12:00:00Z").

    Returns:
        str: The converted time string in the format "%Y-%m-%d %H:%M:%S" adjusted to UTC-4.

    Raises:
        ValueError: If the input time string does not match the expected format.
    """
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    return (time - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    
def get_seen_comments(comment_ids="seen_comments.json"):
    """
    Loads a set of seen comment IDs from a JSON file.

    Args:
        comment_ids (str): Path to the JSON file containing a list of seen comment IDs. Defaults to "seen_comments.json".

    Returns:
        set: A set containing the comment IDs that have already been seen.
    """
    with open(comment_ids, "r") as seen:
        return set(json.load(seen))
    
def save_progress(lastDate, progress="PROGRESS.txt", seen_comments="seen_comments.json"):
    """
    Saves the current progress of the web scraper, including the last processed date and the set of seen comments.

    Args:
        lastDate (str): The last date processed by the scraper, to be saved for resuming progress.
        progress (str, optional): The filename for storing the last processed date. Defaults to "PROGRESS.txt".
        seen_comments (str, optional): The filename for storing the set of seen comment IDs in JSON format. Defaults to "seen_comments.json".

    Note:
        The function writes the lastDate to the specified progress file and serializes the seen_comments set to a JSON file.
    """
    with open(progress, 'w') as file:
        file.write(f"{lastDate}\n")

    with open("seen_comments.json", "w") as seen:
        json.dump(list(seen_comments), seen)

    
def main():
    """
    Main function to fetch and store comments from the Regulations.gov API.

    This function performs the following steps:
    1. Loads environment variables and initializes API parameters.
    2. Reads progress and previously seen comment IDs from files.
    3. Iteratively fetches comment data from the API, handling pagination and rate limiting.
    4. Writes new comment data to a CSV file, avoiding duplicates using a set of seen comment IDs.
    5. Updates progress and seen comment IDs after each batch or upon encountering errors.

    The function continues fetching data until all available comments are retrieved or an error occurs.
    """
    # Links, File Paths, and Default Parameters
    load_dotenv()
    baseURL = "https://api.regulations.gov/v4/comments"
    api_key = os.getenv("REG_GOV_API_KEY_LW")
    rawdata = "comment_data.csv"
    progress = "PROGRESS.txt"
    comment_ids = "seen_comments.json"
    default_page_size = 250
    pageNumber = 1
    iteration = 1
    last_date = get_next_time(progress)
    seen_comments = get_seen_comments(comment_ids)

    while True:
        print("Param_date: ", get_next_time(progress))
        # Parameters for page and filters to call
        params = {
        "api_key" : api_key,
        "sort" : "lastModifiedDate,documentId",
        "filter[lastModifiedDate][ge]" : to_iso_format(get_next_time(progress)),
        "page[number]" : pageNumber,
        "page[size]" : default_page_size
        }

        print(f"Fetching data from {params['filter[lastModifiedDate][ge]']}. Current Page Number: {pageNumber}")

        # Getting the page
        page = requests.get(baseURL, params=params)
        # Handle a failure and break
        if (page.status_code != 200): # page limit is code 429
            print("Something went wrong")
            if (page.status_code == 429):
                print("Rate limited. Sleeping for 1 hour...")
                time.sleep(3600)
                continue
            print("Status code: ", page.status_code)
            save_progress(get_next_time(progress), progress,seen_comments)
            break

        # Data is in the page in JSON
        data = page.json()
        comments = data["data"]

        with open(rawdata, mode="a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for comment in comments:
                if comment["id"] not in seen_comments:
                    observation = []
                    observation.append(comment["id"])
                    observation.append(comment["attributes"]["documentType"])
                    observation.append(comment["attributes"]["lastModifiedDate"])
                    observation.append(comment["attributes"]["withdrawn"])
                    observation.append(comment["attributes"]["agencyId"])
                    observation.append(comment["attributes"]["title"])
                    observation.append(comment["attributes"]["objectId"])
                    observation.append(comment["attributes"]["postedDate"])
                    seen_comments.add(comment["id"])
                    writer.writerow(observation)
            last_date = max(comment["attributes"]["lastModifiedDate"] for comment in comments)

        # Handle where there is a next page: we can keep going and there is no problem
        if data["meta"]["hasNextPage"]: 
            pageNumber += 1
            print("Next Page...")
        # If there isn't a next page, there are two scenarios:
        elif pageNumber == 40 and comment["meta"]["totalElements"] < 10000:
            save_progress(get_next_time(progress), progress, seen_comments)
            break
        else:
            print("No next page")
            save_progress(last_date, progress, seen_comments)
            pageNumber = 1
        iteration += 1

main()

