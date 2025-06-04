import requests
import bs4 as BeautifulSoup

baseURL = "https://www.regulations.gov/search/comment"

params = {
    "sortBy" : "postedDate",
    "sortDirection" : "desc",
    "pageNumber" : 1
}

while True:
    print(f"Fetching data from page {params['pageNumber']}...")
    page = requests.get(baseURL, params=params)
    if (page.status_code != 200):
        print("Connection Failed")
        break
    params['pageNumber'] += 1

print("No errors")