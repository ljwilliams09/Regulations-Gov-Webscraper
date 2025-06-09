import requests
import csv
from datetime import datetime, timedelta
import json
import time


def get_next_time(progress):
    # get the time that the next page call parameter will start with
    with open(progress, 'r') as file:
        date_time = datetime.strptime(file.readline().strip(), "%Y-%m-%dT%H:%M:%SZ")
        adjust_for_utc = date_time - timedelta(hours=4)
        # adjust hours parameter to differnce between current timezone and utc
        return adjust_for_utc.strftime("%Y-%m-%d %H:%M:%S") 

def get_seen_comments(comment_ids):
    # retrieves a set of comment ids to check against newly processed comments
    with open(comment_ids, "r") as seen:
        return set(json.load(seen))
    
def save_progress(lastDate, progress, seen_comments):
    dt_obj = datetime.strptime(lastDate, "%Y-%m-%d %H:%M:%S")
    lastDate = dt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
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
    date_time = get_next_time(progress)
    seen_comments = get_seen_comments(comment_ids)
    lastDate = date_time

    while True:
        # Parameters for page and filters to call
        params = {
        "api_key" : api_key,
        "sort" : "lastModifiedDate,documentId",
        "filter[lastModifiedDate][ge]" : date_time,
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
            save_progress(lastDate, progress,seen_comments)
            break

        # Data is in the page in JSON
        data = page.json()
        comments = data["data"]
        if not comments:
            save_progress(lastDate, progress, seen_comments)
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
            lastDate = max(comment["attributes"]["lastModifiedDate"] for comment in comments)

        # Handle where there is a next page: we can keep going and there is no problem
        if data["meta"]["hasNextPage"]: 
            pageNumber += 1
            print("Next Page...")
        # If there isn't a next page, there are two scenarios:
        else:
            print("No next page")
            save_progress(lastDate, progress, seen_comments)
            pageNumber = 1
        iteration += 1

main()

        
    
