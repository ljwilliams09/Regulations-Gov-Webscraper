import requests
import csv
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
from logger_config import logger
from collections import deque

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

def track_id(new_id, ids_set, ids_deque):
    if new_id not in ids_set:
        if len(ids_deque) == ids_deque.maxlen:
            oldest = ids_deque.popleft()
            ids_set.remove(oldest)
        ids_deque.append(new_id)
        ids_set.add(new_id)
        return ids_set, ids_deque
    else:
        logger.error("track_id: id already in set")
        raise Exception("")



def test_reset_point(url, params, lastModifiedDate, totalElements): 
    hours = 1
    while True:
        logger.info(f"Testing Reset Point with {hours} hour(s) differential")
        logger.info(f"totalElements Before: {totalElements}")
        params["filter[lastModifiedDate][ge]"] = date_format_param(lastModifiedDate, diff=hours)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            if response.status_code == 429:
                logger.info("Rate limited")                   
                time.sleep(3600)
                continue
            else:
                logger.error(f"Testing error Connecting to API. Params: {params}")
                break
        new_elements = response.json()["meta"]["totalElements"]
        logger.info(f"totalElements After: {new_elements}")
        if new_elements >= totalElements - 10000:
            return date_format_param(lastModifiedDate, diff=hours)
        else:
            hours += 1

def fetch():
    load_dotenv()
    year = 2025
    url = "https://api.regulations.gov/v4/comments"
    output = f"comments.csv"

        logger.info(f"************ {year} ***********")

        ids_set = set()
        ids_deque = deque(maxlen=10000)
        # print(f"Year: {year}")
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
        with open(output, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "postedDate", "lastModifiedDate"])
            count = 0
            while True:
               retries = 0
               limit = 5
               while True:
                    response = requests.get(url, params=params)
                    if response.status_code != 200:
                        if response.status_code == 429
                            logger.info("Rate limited")                   
                            time.sleep(3600)
                            continue
                    else:
                        retries += 1
                        if retries >= limit:
                            logger.error(f"Error Connecting to API. Params: {params}")
                            raise Exception(f"Error Connecting to API. Params: {params}")
                        time.sleep(2 ** retries)
                        

                # print(f"MAX COMMENTS: {(response.json())['meta']['totalElements']}")
                comments = response.json()
                totalElements = comments["meta"]["totalElements"]
            
                for comment in (comments["data"]):
                    if (comment["id"] not in ids_set):
                        writer.writerow([comment["id"],clean_text(comment["attributes"]["title"]),normalize_date(comment["attributes"]["postedDate"]),normalize_date(comment["attributes"]["lastModifiedDate"])])
                        ids_set, ids_deque = track_id(comment["id"], ids_set, ids_deque)
                        count += 1
                    else:
                        logger.info(f"Duplicate on: {comment['id']}")
                    
                # Handle next page
                if (comments)["meta"]["hasNextPage"]:
                    page += 1
                    params["page[number]"] = page
                elif (not (comments)["meta"]["hasNextPage"]) and (comments)["meta"]["totalElements"] < 10000:
                    break
                else: 
                    logger.info(f"Elements left: {response.json()['meta']['totalElements']}")
                    logger.info("RESET PARAMETERS")
                    page = 1
                    params["page[number]"] = page
                    params["filter[lastModifiedDate][ge]"] = test_reset_point(url=url, params=params, lastModifiedDate=max(comment["attributes"]["lastModifiedDate"] for comment in (comments["data"])), totalElements=totalElements)

        logger.info(f"******** COUNT = {count} ********")
            

fetch()