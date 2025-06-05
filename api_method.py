import requests
import csv
from datetime import datetime, timedelta

baseURL = "https://api.regulations.gov/v4/comments"
api_key = input("API Key: ")
rawdata = "comments.csv"
progress = "PROGRESS.txt"

def previousDay(date_str):
    obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (obj - timedelta(days=1)).strftime("%Y-%m-%d")

date = input("Starting Date: ")
pageNumber = 1
iteration = 1
while True:
    params = {
    "page[number]" : pageNumber,
    "api_key" : api_key,
    "filter[postedDate]" : date,
    "page[size]" : 250
    }
    print(f"Fetching data from {params['filter[postedDate]']} and page {params['page[number]']}. Iteration: {iteration}")
    page = requests.get(baseURL, params=params)

    if (page.status_code != 200):
        print("Error connecting!")
        print("Status Code: ", page.status_code)
        print("Error: ", page.json())
        print("Current Date: ", date)
        print("Page: ", pageNumber)
        break

    data = page.json()
    comments = data["data"]
    with open(rawdata, mode="a", newline='', encoding='utf-8') as file:
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

            writer = csv.writer(file)
            writer.writerow(observation)
    if len(comments) < 250: 
        pageNumber = 1
        date = previousDay(date)
    else:
        pageNumber += 1
    iteration += 1


