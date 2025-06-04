import requests

baseURL = "https://api.regulations.gov/v4/comments"
api_key = ""

params = {
    "page[number]" : 1,
    "api_key" : api_key,
    "sort" : "-postedDate"
    "sortDirection"

}

while True:
    print(f"Fetching JSON data from page {params['page[number]']}")
    page = requests.get(baseURL, params=params)

    if (page.status_code != 200):
        print("Error connecting!")
        break

    data = response.json()
    comments = data["data"]
    for comment in comments:




    params["page[number]"] += 1