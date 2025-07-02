import requests
import os
import time
from dotenv import load_dotenv()




def main():
    load_dotev()
    results = "dockets.csv" # a csv of valid docket Id's 
    url = "https://api.regulations.gov/v4/dockets"
    RULES = 1
    PROPOSED_RULES = 1

    with open(results, 'a') as f:
        page = 1
        while True:

            params = {
                "api_key" : os.getenv("REG_GOV_API_KEY_ES"),
                "sort" : "lastModifiedDate,documentId",
                "page[size]" : 250,
                "page[number]" : page
            }

            response = requests.get(url, params)

            if response.status_code != 200:
                if response.status_code == 429:


