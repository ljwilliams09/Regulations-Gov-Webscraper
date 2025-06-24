import requests
import csv
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

def year_range(year):
    return f'{year}-01-01', f'{year}-12-31'

def date_format_param(last_date):
    date = datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%SZ")
    return (date - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")

def normalize_date(date):
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return date.strftime("%Y-%m-%d %H:%M:%S")

def clean_text(text):
    return text.replace('\r', ' ').replace('\n', ' ').strip()


def fetch():
    passed_through = False
    year = 1999
    url = "https://api.regulations.gov/v4/comments"
    output = "comments.csv"
    start_date = f"0001-01-01T00:00:00"
    ids = set()

    print(f"Year: {year}")
    page = 1
    ge, le = year_range(year)
    params = {
                "api_key" : os.getenv("REG_GOV_API_KEY_LW"),
                "filter[postedDate][ge]" : ge,
                "filter[postedDate][le]" : le,
                "sort" : "lastModifiedDate,documentId", 
                "page[number]" : page,
                "page[size]" : 250            
    }
    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "postedDate", "lastModifiedDate"])
        while True:
            print(f"Page: {page}")
            print(f"Params: {params}")
                
            response = requests.get(url, params=params)
            if response.status_code != 200:
                if response.status_code == 429:
                    print("Limit Reached, going to sleep for a while")                    
                    time.sleep(3600)
                    continue
                else:
                    print("Error connecting to API")
                    break

            print(f"MAX COMMENTS: {(response.json())['meta']['totalElements']}")
        
          
            for comment in ((response.json())["data"]):
                if (comment["id"] not in ids):
                    writer.writerow([comment["id"],clean_text(comment["attributes"]["title"]),normalize_date(comment["attributes"]["postedDate"]),normalize_date(comment["attributes"]["lastModifiedDate"])])
                    ids.add(comment["id"])
                
            # Handle next page
            if (response.json())["meta"]["hasNextPage"]:
                page += 1
                params["page[number]"] = page
            elif (not (response.json())["meta"]["hasNextPage"]) and (response.json())["meta"]["totalElements"] < 10000:
                break
            else: 

                print("RESET PARAMETERS")
                start_date = date_format_param(max(comment["attributes"]["lastModifiedDate"] for comment in (response.json())["data"]))
                params["filter[lastModifiedDate][ge]"] = start_date
                page = 1
                params["page[number]"] = page



fetch()