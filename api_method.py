import requests
import csv
from datetime import datetime, timedelta
import json
import time



def get_next_time(progress="PROGRESS.txt"):
    '''
    Takes the time from the file path
    '''
    with open(progress, 'r') as file:
        return file.readline().strip()

def to_iso_format(time):
    '''turns to iso_format and adjusts for utc time for parameter'''
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    return (time - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    
def get_seen_comments(comment_ids="seen_comments.json"):
    with open(comment_ids, "r") as seen:
        return set(json.load(seen))
    
def save_progress(lastDate, progress="PROGRESS.txt", seen_comments="seen_comments.json"):
    '''
    Saves the progress when there is an issue. Last date should be in "%Y-%m-%dT%H:%M:%SZ" format.
    '''
    with open(progress, 'w') as file:
        file.write(f"{lastDate}\n")

    with open("seen_comments.json", "w") as seen:
        json.dump(list(seen_comments), seen)

    
def main():
    # Links, File Paths, and Default Parameters
    baseURL = "https://api.regulations.gov/v4/comments"
    api_key = "RWhAaanqXHMC89fGk755BO70rN8ygv1txMawAG3a"
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
        if not comments:
            save_progress(get_next_time(progress), progress, seen_comments)
            break
        
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
        else:
            print("No next page")
            save_progress(last_date, progress, seen_comments)
            pageNumber = 1
        iteration += 1

main()

