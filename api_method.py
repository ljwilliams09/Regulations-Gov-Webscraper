import requests
import csv
from datetime import datetime, timedelta

# regulations.gov API URL
baseURL = "https://api.regulations.gov/v4/comments"
api_key = input("API Key: ")

# CSV to save data, and txt file to save the date and page info between parsing
rawdata = "comments.csv"
progress = "PROGRESS.txt"

# Moves the dates back to the day before and resets their clocks to be at the ends
def previousDay(startDate):
    start = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
    prev = start.date() - timedelta(days=1)
    new_start = datetime.combine(prev, datetime.min.time()).strftime("%Y-%m-%d %H:%M:%S")
    new_end = datetime.combine(prev, datetime.max.time().replace(microsecond=0)).strftime("%Y-%m-%d %H:%M:%S")
    return new_end, new_start

# get the variables from the txt file from the previous run
with open("progress.txt", 'r') as file:
    lines = file.readlines()
    endDate = lines[0].strip()
    startDate = lines[1].strip()
    # pageNumber = int(lines[2].strip())  

# Continue looping and break on a few conditions; each loop is a call to a new page of the API
iteration = 1

while True:
    # Parameters for which page and filters to be looking at since there is a pagination limit
    params = {
    "page[number]" : pageNumber,
    "api_key" : api_key,
    "sort" : "-lastModifiedValue",
    "filter[lastModifiedDate][le]" : endDate,
    "filter[lastModifiedDate][ge]" : startDate,
    "page[size]" : 250
    }
    print(f"Fetching data from {params['filter[postedDate]']} and page {params['page[number]']}.  Page Call #: {iteration}")

    # Getting the page
    page = requests.get(baseURL, params=params)


    # Handle a failure and break
    if (page.status_code != 200):
        print("Error connecting!")
        print("Status Code: ", page.status_code)
        print("Error: ", page.json())
        print("Current Date: ", date)
        print("Page: ", pageNumber)
        # Write stopping point to txt file to start at
        with open("progress.txt", 'w') as file:
            file.write(f"{endDate}\n")
            file.write(f)
        break

    # Data is in the page in JSON
    data = page.json()
    comments = data["data"]
    # Write to CSV file

    with open(rawdata, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for comment in comments:
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
            observation.append(comment["links"]["self"])
            writer.writerow(observation)

    # Handle where there is a next page: we can keep going and there is no problem
    if data["hasNextPage"]: 
        pageNumber += 1
    # If there isn't a next page, there are two scenarios:
    else:
        # There are more than 10,000 comments in this filter, meaning that there are more past the 250 comments per page x 40 pages that we are able to see
        if data["totalElememts"] > 10000:
            endDate, startDate = previousDay(startDate)
        
    iteration += 1