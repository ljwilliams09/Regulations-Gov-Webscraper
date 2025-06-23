import requests
import csv
from datetime import datetime, timedelta
import json
import time
import os
from dotenv import load_dotenv

def year_to_date_range(year):
    """
    Given an integer year, returns a tuple of strings representing
    the first and last days of that year in 'YYYY-mm-dd' format.
    """
    first_day = f"{year}-01-01"
    last_day = f"{year}-12-31"
    return first_day, last_day

# Example usage:
# start, end = year_to_date_range(2024)
# print(start)  # '2024-01-01'
# print(end)    # '2024-12-31'

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
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Connection Failed")
            break;
        data = response.json()
        with open(output, 'a') as f:
            writer = csv.writer()
            writer.writerow([year, data["data"]["totalElements"]])
        year -= 1
        if year == 1800:
            break
        break
    
main()
