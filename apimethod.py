import requests

baseURL = "https://api.regulations.gov/v4/comments"

params = {
    "page[number]" : 1,
    "api_key" : "RWhAaanqXHMC89fGk755BO70rN8ygv1txMawAG3a"
}

while True:
    print(f"Fetching JSON data from page {params['pageNumber']}")
    page = requests.get(baseURL, params=params)

    if (page.status_code != 200):
        print("Error connecting!")
    break