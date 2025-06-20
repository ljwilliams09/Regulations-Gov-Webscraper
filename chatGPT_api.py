from openai import OpenAI
import os
import csv
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("CHAT_API_KEY"))

def api_call(comment_title, comID):
    prompt = f"""Does the following comment title contain an affiliation or organization for the commenter? Respond only with a 1 for Yes, or 0 for No. Follow that answer with a comma and no space, then the name of the affiliation if there is one, or N/A if not. Be mindful that the commenter might be including the rules ID in their comment and it is not their affiliation

    Title: {comment_title}, Comment ID: {comID}
    """
    response = client.chat.completions.create(model="gpt-4.1",
    messages=[{
        "role":"user",
        "content":prompt
        }],
    temperature=0)
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()

def main():
    # Variables and Paths
    titles = "sample_500.csv"
    results = "chatGPT_500_coding_affiliation.csv"

    with open(titles, 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        with open(results, 'a', newline='', encoding='utf-8') as r:
            writer = csv.writer(r)
            for row in reader:
                response = api_call(row[1], row[0])
                print("Response: ", response)
                writer.writerow([row[1]]+ response.split(','))
main()