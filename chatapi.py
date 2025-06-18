import openai
import csv

def main():
    # Variables and Paths
    openai.api_key = input("API Key: ")
    titles = "excluding_comments_o`n.csv"
    results = "samplecoding.csv"
    prompt = "Does the following comment title contain an affiliation or organization for the commenter? Respond only with 1 for Yes, or 0 for No."

    with open(titles, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            comment_title = row[1]
            response = openai.ChatCompletion.create(
                
            )


