import requests
import csv
from datetime import datetime, timedelta

# regulations.gov API URL
baseURL = "https://api.regulations.gov/v4/comments"
api_key = input("API Key: ")

# CSV to save data, and txt file to save the date and page info between parsing
rawdata = "comments.csv"
progress = "PROGRESS.txt"

# Moves the date back to the day before
def previousDay(date_str):
    obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (obj - timedelta(days=1)).strftime("%Y-%m-%d")

# get the variables from the txt file from the previous run
with open("progress.txt", 'r') as file:
    lines = file.readlines()
    date = lines[0].strip()
    pageNumber = int(lines[1].strip())  

# Continue looping and break on a few conditions
iteration = 1
while True:
    # Parameters for which page and filters to be looking at since there is a pagination limit
    params = {
    "page[number]" : pageNumber,
    "api_key" : api_key,
    "filter[postedDate]" : date,
    "page[size]" : 250
    }
    print(f"Fetching data from {params['filter[postedDate]']} and page {params['page[number]']}. Iteration: {iteration}")

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
            file.write(f"{date}\n")
            file.write(str(pageNumber))
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

    #
    if not comments["hasNextPage"]: 
        pageNumber = 1
        date = previousDay(date)
    else:
        pageNumber += 1
    iteration += 1


