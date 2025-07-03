import requests
import os
import csv
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from collections import deque
from logger_dockets import logger

def track_id(new_id, ids_set, ids_deque):
    if new_id not in ids_set:
        if len(ids_deque) == ids_deque.maxlen:
            oldest = ids_deque.popleft()
            ids_set.remove(oldest)
        ids_deque.append(new_id)
        ids_set.add(new_id)
        return ids_set, ids_deque
    else:
        logger.info("Track_id: id already in set")
        raise Exception("")
    
def date_format_param(last_date, diff=6):
    date = datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%SZ")
    return (date - timedelta(hours=diff)).strftime("%Y-%m-%d %H:%M:%S")

def validate_request(url, params):
    retries = 0
    max_tries = 5
    while True:
        response = requests.get(url, params)

        if response.status_code != 200:
            if response.status_code == 429:
                logger.info("Rate limited")
                time.sleep(3600)
                continue
            else:
                retries += 1
                if retries >= max_tries:
                    logger.info("Failure to connect")
                    break
                time.sleep(retries ** 2) # exponential backoff
        return response
    

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
                logger.info(f"Testing error Connecting to API. Params: {params}")
                break
        new_elements = response.json()["meta"]["totalElements"]
        logger.info(f"totalElements After: {new_elements}")
        if new_elements >= totalElements - 10000:
            return date_format_param(lastModifiedDate, diff=hours)
        else:
            hours += 1



def main():
    load_dotenv()
    results = "dockets/dockets.csv" # col 1: docketId, col 2: title, col 3: rulemaking or nonrulemaking docket
    url = "https://api.regulations.gov/v4/dockets"
    ids_set = set()
    ids_deque = deque(maxlen=10000)
    count = 0

    with open(results, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(["docketId", "title", "rulemaking"])
        page = 1
        while True:
            params = {
                "api_key" : "5cptlDctYd9BNNtx0IzLve8hK8qr70SpImLIkwpK",
                "sort" : "lastModifiedDate,docketId",
                "page[size]" : 250, 
                "page[number]" : page
            }
        
            response = validate_request(url, params)

            dockets = response.json()
            totalElements = response.json()["meta"]["totalElements"]
            for docket in dockets["data"]:
                if docket["id"] not in ids_set:
                    writer.writerow([
                        docket["id"],
                        docket["attributes"]["title"],
                        docket["attributes"]["docketType"]
                    ])
                    ids_set, ids_deque = track_id(docket["id"], ids_set, ids_deque)
                    count += 1
                else:
                    logger.info(f"Duplicate on: {docket['id']}")

            if dockets["meta"]["hasNextPage"]:
                page += 1
                params["page[number]"] = page
            elif (not dockets["meta"]["hasNextPage"]) and dockets["meta"]:
                break
            else:
                logger.info(f"Elements left: {dockets['meta']['totalElements']}")
                logger.info("RESET PARAMETERS")
                page = 1
                params["page[number]"] = page
                params["filter[lastModifiedDate[ge]"] = test_reset_point(
                    url=url,
                    params=params,
                    lastModifiedDate=max(docket["attributes"]["lastModifiedDate"] for docket in dockets["data"]),
                    totalElements=totalElements
                )

        logger.info(f"******** COUNT = {count}********")
                
main()
                    
            
                



