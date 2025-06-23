import requests
import csv
from datetime import datetime, timedelta
import json
import time
import os
from dotenv import load_dotenv

def year_to_date_range(year):
    return f"{year}-01-01", f"{year}-12-31"

def main():
    load_dotenv()
    output = "comments_per_year.csv"
    url = "https://api.regulations.gov/v4/comments"
    year = int (input("What year should we start at?: "))
    ge, le = year_to_date_range(year)
    params = {
        "api_key" : os.getenv("REG_GOV_API_KEY_AB"),
        "filter[postedDate][ge]" : ge ,  
        "filter[postedDate][le]" : le
    }

    while True:
        ge, le = year_to_date_range(year)
        params = {
        "api_key" : os.getenv("REG_GOV_API_KEY_AB"),
        "filter[postedDate][ge]" : ge ,  
        "filter[postedDate][le]" : le
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Connection Failed")
            break;
        elements = (response.json())["meta"]["totalElements"]
        with open(output, 'a') as f:
            writer = csv.writer(f)
            print(f"Year: {year} with {elements} elements")
            writer.writerow([year, elements])
        year -= 1
        if year < 1800:
            break

main()
