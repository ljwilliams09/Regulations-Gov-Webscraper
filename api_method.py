import requests
import csv
from datetime import datetime, timedelta
import json

# regulations.gov API URL
baseURL = "https://api.regulations.gov/v4/comments"
api_key = "RWhAaanqXHMC89fGk755BO70rN8ygv1txMawAG3a"
rawdata = "comments.csv"
progress = "PROGRESS.txt"

# get the variables from the txt and json file from the previous run
with open(progress, 'r') as file:
    date_time = datetime.strptime(file.readline().strip(), "%Y-%m-%dT%H:%M:%SZ")
    adjust_for_utc = date_time - timedelta(hours=4)
    date_time = adjust_for_utc.strftime("%Y-%m-%d %H:%M:%S") 

with open("seen_comments.json", "r") as seen:
    seen_comments = set(json.load(seen))

pageNumber = 1
lastDate = date_time
iteration = 1

while True:
    # Parameters for which page and filters to be looking at since there is a pagination limit
    params = {
    "api_key" : api_key,
    "sort" : "lastModifiedDate,documentId",
    "filter[lastModifiedDate][ge]" : date_time,
    "page[number]" : pageNumber,
    "page[size]" : 250
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
            else:
                print("Duplicate Found")
            lastDate = comment["attributes"]["lastModifiedDate"]


    # Handle where there is a next page: we can keep going and there is no problem
    if data["meta"]["hasNextPage"]: 
        pageNumber += 1
        print("Has next page!")
    # If there isn't a next page, there are two scenarios:
    else:
        pageNumber = 1
        print("Transfer! ", lastDate)
        dt_obj = datetime.strptime(lastDate, "%Y-%m-%dT%H:%M:%SZ")
        date_time = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        with open(progress, 'w') as file:
            file.write(f"{lastDate}\n")
    iteration += 1
        
with open("seen_comments.json", "w") as seen:
    json.dump(list(seen_comments), seen)



        
    