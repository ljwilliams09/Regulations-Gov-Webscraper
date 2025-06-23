import requests
import csv
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

def year_range(year):
    return f'{year}-01-01', f'{year}-12-31'

def fetch():
    year = 2024
    url = "https://api.regulations.gov/v4/comments"
    output = "comments.csv"

    # each iteration is a look at a new year
    while True:
        print("Year: {year}")

        while True:
            ge, le = year_range(year)
            params = {
                "api_key" : os.getenv("REG_GOV_API_KEY_LW"),
                "filter[postedDate][ge]" : ge,
                "filter[postedDate][le]" : le,
                "sort" : "lastModifiedDate"
            }
            response = requests.get(url, params=params)
            comments = (response.json())["data"]
            with open(output, 'a') as f:
                writer = csv.writer(f)
                for comment in comments:
                    writer.writerow([comment["id"],comment["attributes"]["title"],comment["attributes"]["postedDate"],comment["attributes"]["lastModifiedDate"]])
                
        year -= 1