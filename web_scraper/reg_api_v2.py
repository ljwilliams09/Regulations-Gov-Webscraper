import requests
import csv
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
from logger_config import logger

def year_range(year):
    return f'{year}-01-01', f'{year}-12-31'

def date_format_param(last_date, diff=6):
    date = datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%SZ")
    return (date - timedelta(hours=diff)).strftime("%Y-%m-%d %H:%M:%S")

def normalize_date(date):
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return date.strftime("%Y-%m-%d %H:%M:%S")

def clean_text(text):
    return text.replace('\r', ' ').replace('\n', ' ').strip()

def test_reset_point(url, params, lastModifiedDate, totalElements): 
    hours = 1
    logger.info(f"Testing Reset Point with {hours} hour(s) differential")
    logger.info(f"totalElements Before: {totalElements}")
    while True:
        params[lastModifiedDate] = date_format_param(lastModifiedDate, diff=hours)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            if response.status_code == 429:
                logger.info("Rate limited")                   
                time.sleep(3600)
                continue
            else:
                logger(f"Error Connecting to API. Params: {params}")
                break
        new_elements = response.json()["meta"]["totalElements"]
        logger.info(f"totalElements After: {new_elements}")
        if new_elements >= totalElements - 10000:
            return lastModifiedDate
        else:
            hours + 1

        
        



def fetch():
    load_dotenv()
    year = 1999
    url = "https://api.regulations.gov/v4/comments"
    output = "comments.csv"
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
                    logger.info("Rate limited")                   
                    time.sleep(3600)
                    continue
                else:
                    logger(f"Error Connecting to API. Params: {params}")
                    break

            print(f"MAX COMMENTS: {(response.json())['meta']['totalElements']}")
            comments = response.json()
            totalElements = comments["meta"]["totalElements"]
          
            for comment in (comments["data"]):
                if (comment["id"] not in ids):
                    writer.writerow([comment["id"],clean_text(comment["attributes"]["title"]),normalize_date(comment["attributes"]["postedDate"]),normalize_date(comment["attributes"]["lastModifiedDate"])])
                    ids.add(comment["id"])
                else:
                    logger.info(f"Duplicate on: {comment['id']}")
                
            # Handle next page
            if (comments)["meta"]["hasNextPage"]:
                page += 1
                params["page[number]"] = page
                logger.info(f"Elements left: {response.json()['meta']['totalElements']}")
            elif (not (comments)["meta"]["hasNextPage"]) and (comments)["meta"]["totalElements"] < 10000:
                break
            else: 
                logger.info("RESET PARAMETERS")
                params["filter[lastModifiedDate][ge]"] = test_reset_point(url=url, params=params, lastModifiedDate=max(comment["attributes"]["lastModifiedDate"] for comment in (comments["data"])), totalElements=comments["meta"]["totalElements"])
                page = 1
                params["page[number]"] = page



fetch()