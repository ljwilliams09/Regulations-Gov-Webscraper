import openai
import csv
from dotenv import load_dotenv
import os

def api_call(comment_title):
    prompt = f"""Does the following comment title contain an affiliation or organization for the commenter? Respond only with 1 for Yes, or 0 for No.

    Title: {comment_title}
    """
    response = openai.ChatCompletion.create(
        model="o4-mini",
        messages=[{
            "role":"user",
            "content":prompt
            }],
        temperature=0
    )

    return response["choices"][0]["message"]["content"].strip()

def main():
    load_dotenv()
    # Variables and Paths
    openai.api_key = os.getenv("CHAT_API_KEY")
    titles = "excluding_comments_on.csv"
    results = "samplecoding.csv"

    with open(titles, 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        with open(results, 'w', newline='', encoding='utf-8') as r:
            writer = csv.writer(r)
            for row in reader:
                comment_title = row[1]
                response = api_call(comment_title)
                print("Response: ", response)
                writer.writerow([row[1], response])
                break


main()

