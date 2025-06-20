import os
from dotenv import load_dotenv
import openai
import csv

def main():
    load_dotenv()
    regulations_api = os.getenv("REG_GOV_API_KEY")
    meta_data = ""
    results = "" # expecting a csv of just comment Id's
    base_url = "https://api.regulations.gov/v4/comments/"
    params = {
        "api_key" : regulations_api
    }
main()