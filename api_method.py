import requests
import csv

baseURL = "https://api.regulations.gov/v4/comments"
api_key = input("API Key: ")
rawdata = ("rawdata.csv")
pages2parse = 100

params = {
    "page[number]" : 1,
    "api_key" : api_key,
    "sort" : "-postedDate"
}

while params["page[number]"] < pages2parse + 1:
    print(f"Fetching JSON data from page {params['page[number]']}")
    page = requests.get(baseURL, params=params)

    if (page.status_code != 200):
        print("Error connecting!")
        break

    data = page.json()
    comments = data["data"]
    for comment in comments:
        observation = []
        observation.append(comment["id"])
        observation.append(comment["attributes"]["documentType"])
        observation.append(comment["attributes"]["lastModifiedDate"])
        observation.append(comment["attributes"]["highlightedContent"])
        observation.append(comment["attributes"]["withdrawn"])
        observation.append(comment["attributes"]["agencyId"])
        observation.append(comment["attributes"]["title"])
        observation.append(comment["attributes"]["objectId"])
        observation.append(comment["attributes"]["postedDate"])
        # observation.append(comment["links"]["self"])
        with open(rawdata, mode="a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(observation)
    params["page[number]"] += 1