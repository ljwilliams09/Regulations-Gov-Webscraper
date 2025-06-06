import requests
import csv
from datetime import datetime, timedelta

# regulations.gov API URL
baseURL = "https://api.regulations.gov/v4/comments"
api_key = input("API Key: ")
date = input("Input Start Date in YYYY-MM-DD Format: ")

# CSV to save data, and txt file to save the date and page info between parsing
commentsperday = "commentsperday.csv"

# Moves the dates back to the day before and resets their clocks to be at the ends
def previousDay(startDate):
    current = datetime.strptime(startDate, "%Y-%m-%d")
    return (current - timedelta(days=1)).strftime("%Y-%m-%d")

# Continue looping and break on a few conditions; each loop is a call to a new page of the API
iteration = 1
while True:
    # Parameters for which page and filters to be looking at since there is a pagination limit
    params = {
    "api_key" : api_key,
    "filter[postedDate]" : date,
    "page[size]" : 25
    }
    print(f"Fetching data from {params['filter[postedDate]']},  Page Call #: {iteration}")

    # Getting the page
    page = requests.get(baseURL, params=params)

    # Handle a failure and break
    if (page.status_code != 200):
        print("Error connecting!")
        print("Status Code: ", page.status_code)
        print("Error: ", page.json())
        print("Current Date: ", date)

    # Data is in the page in JSON
    data = page.json()
    total = data["meta"]["totalElements"]

    print("Total: ", total)

    # Write to CSV file

    with open(commentsperday, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, total])
        
    date = previousDay(date)
    iteration += 1