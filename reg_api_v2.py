import requests
import csv
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

def year_range(year):
    return f'{year}-01-01', f'{year}-12-31'

def date_format(last_date):
    date = datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%SZ")
    return (date - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")


def fetch():
    year = 1991
    url = "https://api.regulations.gov/v4/comments"
    output = "comments.csv"
    start_date = "0001-01-01T00:00:00"

    print("Year: {year}")
    page = 1
    while True:
        print(f"Page: {page}")
        ge, le = year_range(year)
        params = {
            "api_key" : os.getenv("REG_GOV_API_KEY_LW"),
            "filter[postedDate][ge]" : ge,
            "filter[postedDate][le]" : le,
            "sort" : "lastModifiedDate",
            "filter[lastModifiedDate][ge]" : start_date, 
            "page[number]" : page,
            "page[size]" : 250            
        }
            
        response = requests.get(url, params=params)
        if response.status_code != 200:
            if response.status_code == 429:
                print("Limit Reached, going to sleep for a while")                    
                time.sleep(3600)
                continue
            else:
                print("Error connecting to API")
                break

        comments = (response.json())["data"]

        with open(output, 'a') as f:
            writer = csv.writer(f)
            for comment in comments:
                writer.writerow([comment["id"],comment["attributes"]["title"],comment["attributes"]["postedDate"],comment["attributes"]["lastModifiedDate"]])
            
        # Handle next page
        if (response.json())["meta"]["hasNextPage"]:
            page += 1
        elif page == 40 and (response.json())["meta"]["totalElements"] < 10000:
            break
        else: 
            start_date = date_format(max(comment["attributes"]["lastModifiedDate"] for comment in comments))
            page = 1

fetch()