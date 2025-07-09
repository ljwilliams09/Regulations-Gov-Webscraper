import requests
import os
from dotenv import load_dotenv
import time
import csv
from logger_dockets import logger


load_dotenv()

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


def scan():
    input_file = "dockets.csv" # csv of all dockets
    output_file = "valid_dockets.csv"
    url = "http://api.regulations.gov/v4/documents"

    with open('input_file.csv', 'r') as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            docket = row[0]
            params = {
                "api_key" : " ",
                "filter[docketId]" : docket,
            }
            response = validate_request(url, params)

    