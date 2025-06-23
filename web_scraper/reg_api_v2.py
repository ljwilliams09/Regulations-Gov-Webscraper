import requests
import csv
from datetime import datetime, timedelta
import json
import time
import os
from dotenv import load_dotenv

def year_range(year):
    return f'{year}-01-01', f'{year}-12-31'

def fetch():
    year = 2024
    url = "https://api.regulations.gov/v4/comments"


    # each iteration is a look at a new year
    while True:
        print("Year: {year}")

        while True:
            ge, le = year_range(year)
            params = {
                "filter[postedDate][ge]" : ge,
                "filter[postedDate][le]" : le
            }
            response = requests.get(url, params=params)
            comments = (response.json())
            break
        year -= 1