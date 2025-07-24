import requests
import os
from dotenv import load_dotenv
import time
import csv
import json


load_dotenv()

def validate_request(url, params):
    retries = 0
    max_tries = 5
    while True:
        response = requests.get(url, params)

        if response.status_code != 200:
            if response.status_code == 429:
                time.sleep(3600)
                continue
            else:
                retries += 1
                if retries >= max_tries:
                    break
                time.sleep(retries ** 2) # exponential backoff
        if (response.json())["meta"]["numberOfElements"] > 10000:
            raise Exception(f"More than 10000 documents in Docket {params['filter[docketId]']}")
        return response.json()
    

def scan():
    # call should be made from the valid_dockets folder
    input_file = "./test.csv" # csv of all dockets
    output_file = "../valid_dockets/test_output.csv"
    document_types = '../valid_dockets/document_types.json'
    url = "http://api.regulations.gov/v4/documents"

    with open(input_file, 'r') as i, open(output_file, 'w') as o:
        reader = csv.reader(i)
        writer = csv.writer(o)
        next(i)
        types = ["Rule", "Proposed Rule", "Supporting & Related Material", "Notice", "Other"]
        writer.writerow(["docketID"] + types)
        count = {doc_type: 0 for doc_type in types}
        for docket in reader:
            docketId = docket[0]
            params = {
                "api_key" : "RWhAaanqXHMC89fGk755BO70rN8ygv1txMawAG3a",
                "filter[docketId]" : docketId,
            }
            response = validate_request(url, params)['meta']['aggregations']['documentType']
            for doc_type in response:
                count[doc_type['label']] = doc_type['docCount']
                print(f"Label: {doc_type['label']}, Count: {doc_type['docCount']}")
            writer.writerow([docketId] + [count[doc_type] for doc_type in types])
scan()





    