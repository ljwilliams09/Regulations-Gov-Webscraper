from openai import OpenAI
import os
import csv
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("CHAT_API_KEY"))

def api_call(comment_title, comID):
    prompt = f"""Does the following comment title contain an affiliation or organization for the commenter? Respond only with 1 for Yes, or 0 for No.

    Title: {comment_title}, Comment ID: {comID}
    """
    response = client.chat.completions.create(model="gpt-4.1",
    messages=[{
        "role":"user",
        "content":prompt
        }],
    temperature=0)

    return response.choices[0].message.content.strip()

def main():
    # Variables and Paths
    titles = "500_sample.csv"
    results = "chatGPT_500_coding.csv"

    with open(titles, 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        with open(results, 'a', newline='', encoding='utf-8') as r:
            writer = csv.writer(r)
            for row in reader:
                response = api_call(row[1], row[0])
                print("Response: ", response)
                writer.writerow([row[1], response])
main()

