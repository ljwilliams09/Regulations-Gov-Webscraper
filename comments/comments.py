import requests
import csv
from datetime import datetime, timedelta
import time
import json
from dotenv import load_dotenv
from logger_comments import logger
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
    if text is None:
        return None
    return (
        text.replace('\r', ' ')
            .replace('\n', ' ')
            .replace('\u2028', ' ')
            .replace('\u2029', ' ')
            .strip()
    )

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
        params["filter[lastModifiedDate][ge]"] = date_format_param(lastModifiedDate, diff=hours)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            if response.status_code == 429:                 
                time.sleep(3600)
                continue
            else:
                logger.error(f"Testing error Connecting to API. Params: {params}")
                break
        new_elements = response.json()["meta"]["totalElements"]
        if new_elements >= totalElements - 10000:
            return date_format_param(lastModifiedDate, diff=hours)
        else:
            hours += 1

def validate_request(url, params):
    retries = 0
    limit = 5
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            if response.status_code == 429:
                time.sleep(3600)
                continue
            else:
                retries += 1
                if retries >= limit:
                    logger.error(f"Error Connecting to API. Params: {params}")
                    raise Exception(f"Error Connecting to API. Params: {params}")
                time.sleep(2 ** retries)
                continue
        return response

def fetch():
    load_dotenv()
    with open('config.json', 'r') as f:
        config = json.load(f)
    year = 2024
    api_key = config["keys"]["-"]
    url = "https://api.regulations.gov/v4/comments"
    path = config["output_path"]
    output = f"{path}csv/comments_{year}.csv"

    logger.info(f"************ {year} ***********")

    ids_set = set()
    ids_deque = deque(maxlen=10000)
    page = 1
    ge, le = year_range(year)
    params = {
        "api_key": api_key,
        "filter[postedDate][ge]": ge,
        "filter[postedDate][le]": le,
        "sort": "lastModifiedDate,documentId",
        "page[number]": page,
        "page[size]": 250
    }
    with open(output, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(["id","type","documentType","lastModifiedDate","highlightedContent", "withdrawn", "agencyId", "title", "objectId", "postedDate"])
        count = 0
        while True:
            response = validate_request(url, params)
            comments = response.json()
            totalElements = comments["meta"]["totalElements"]

            for comment in comments["data"]:
                attributes = comment["attributes"]
                if attributes["objectId"] not in ids_set:
                    writer.writerow([
                        clean_text(comment["id"]),
                        clean_text(comment["type"]),
                        clean_text(attributes["documentType"]),
                        normalize_date(attributes["lastModifiedDate"]),
                        clean_text(attributes["highlightedContent"]),
                        attributes["withdrawn"],
                        clean_text(attributes["agencyId"]),
                        clean_text(attributes["title"]),
                        clean_text(attributes["objectId"]),
                        normalize_date(attributes["postedDate"])
                    ])
                    ids_set, ids_deque = track_id(attributes["objectId"], ids_set, ids_deque)
                    count += 1
                else:
                    logger.info(f"Duplicate on: {comment['id']}")

            # Handle next page
            if comments["meta"]["hasNextPage"]:
                page += 1
                params["page[number]"] = page
            elif (not comments["meta"]["hasNextPage"]) and comments["meta"]["totalElements"] < 10000:
                logger.info(f"******** DONE ********")
                logger.info(f"******** LEFT: {totalElements} ********")
                logger.info(f"******** COUNT = {count} ********")
                break
            else:
                logger.info(f"LEFT: {totalElements}")
                logger.info(f"******** COUNT = {count} ********")
                logger.info("RESET PARAMETERS")
                page = 1
                params["page[number]"] = page
                params["filter[lastModifiedDate][ge]"] = test_reset_point(
                    url=url,
                    params=params,
                    lastModifiedDate=max(comment["attributes"]["lastModifiedDate"] for comment in comments["data"]),
                    totalElements=totalElements
                )

        logger.info(f"******** COUNT = {count} ********")
            

fetch()