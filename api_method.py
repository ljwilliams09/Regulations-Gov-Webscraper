import requests
import csv
from datetime import datetime, timedelta
import json

# get the variables from the txt and json file from the previous run
with open("progress.txt", 'r') as file:
    date_time = file.readline().strip()
with open("seen_comments.json", "r") as seen:
    seen_comments = set(json.load(seen))

# regulations.gov API URL
baseURL = "https://api.regulations.gov/v4/comments"
api_key = input("API Key: ")
rawdata = "comments.csv"
progress = "PROGRESS.txt"
pageNumber = 1
lastDate = date_time
iteration = 1

while True:
    # Parameters for which page and filters to be looking at since there is a pagination limit
    params = {
    "api_key" : api_key,
    "sort" : "lastModifiedDate",
    "filter[lastModifiedDate][ge]" : date_time,
    "page[number]" : pageNumber,
    "page[size]" : 25
    }
    print(f"Fetching data from {params['filter[lastModifiedDate][ge]']}.  Page Call #: {iteration}")

    # Getting the page
    page = requests.get(baseURL, params=params)
    # Handle a failure and break
    if (page.status_code != 200): # page limit is code 429
        print("Error connecting!")
        print("Status Code: ", page.status_code)
        print("Error: ", page.json())
        print("End Date and Time: ", date_time)
        break

    # Data is in the page in JSON
    data = page.json()
    comments = data["data"]
    # Write to CSV file

    with open(rawdata, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for comment in comments:
            if comment["id"] not in seen_comments:
                observation = []
                observation.append(comment["id"])
                observation.append(comment["attributes"]["documentType"])
                observation.append(comment["attributes"]["lastModifiedDate"])
                observation.append(comment["attributes"]["highlightedContent"])
                observation.append(comment["attributes"]["withdrawn"])
                observation.append(comment["attributes"]["agencyId"])
                observation.append(comment["attributes"]["title"])
                observation.append(comment["attributes"]["objectId"])
                observation.append(comment["attributes"]["postedDate"])
                # observation.append(comment["links"]["self"])
                seen_comments.add(comment["id"])
                writer.writerow(observation)
            lastDate = comment["attributes"]["lastModifiedDate"]


    # Handle where there is a next page: we can keep going and there is no problem
    if data["meta"]["hasNextPage"]: 
        pageNumber += 1
    # If there isn't a next page, there are two scenarios:
    else:
        # There are more than 10,000 comments in this filter, meaning that there are more past the 250 comments per page x 40 pages that we are able to see
        if data["meta"]["totalElements"] > 10000:
            pageNumber = 1
            date_time = lastDate
    iteration += 1

with open("progress.txt", 'w') as file:
            file.write(f"{lastDate}\n")
        
with open("seen_comments.json", "w") as seen:
    json.dump(list(seen_comments), seen)
    