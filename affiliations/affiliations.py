import csv
import attachments as a
import comments as c
import helpers
from dotenv import load_dotenv
import openai
import os

def result(title, comment, organization, gov_agency, summary, affiliation):
    """
    Analyzes comment data from regulations.gov and determines the affiliation of the commenter using an OpenAI language model.

    Args:
        title (str): The title of the comment in the database.
        comment (str): The contents of the comment in the database.
        organization (str): The organization of the commenter in the database.
        gov_agency (str): The government agency of the commenter in the database.
        summary (str): The summary of the comment from an attached file.
        affiliation (str): A potential affiliation extracted from the attached file.

    Returns:
        str or None: The determined affiliation of the commenter, or None if no affiliation is found.
    """
    load_dotenv()
    client = openai.OpenAI(os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Here are a variety of variables for a comment on a regulation from regulation.gov, examine them and determine an affiliation for the commenter. Return only the affiliation, or None if there is not one.\n"
        "Variables:\n"
        f"- Title (title of the comment in the database): {title}.\n"
        f"- Comment (contents of the comment in the database): {comment}\n"
        f"- Organization (organization of the commenter in the database): {organization}\n"
        f"- Gov_Agency (agency of the commenter in the database): {gov_agency}\n"
        f"- Summary (summary of an comment in an attached file): {summary}\n"
        f"- Affiliation (potential affiliation pulled from the attached file): {affiliation}" 
    )

    response = client.chat.completions(
        model="o4-mini",
        messages=[
            {"role" : "system", "content" : "You are a data analyst who only returns data in the exact format as specified."},
            {"role" : "user", "content" : prompt}
        ]
    )
    return response.choices[0].message.content



def scan():
    comments = "comments.csv"  # column 0: id
    results = "affiliations.csv" # column 0: id, column 1: title, column 2: affiliation, column 3: comment, column 4: attachment_summary

    with open(comments, 'r') as f:
        reader = csv.reader(f)
        next(f)
    with open(results, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "affiliation", "comment", "attachment_summary"])
        for row in reader:
            comment_id = row[0]
            summary, affiliation = a.scan(comment_id)
            title, comment, organization, gov_agency = c.scan(comment_id)
            print(f"Title: {title}")
            print(f"Comment: {comment}")
            print(f"Organization: {organization}")
            print(f"Gov_Agency: {gov_agency}")
            print(f"Summary: {summary}")
            print(f"Affiliation: {affiliation}")
            final_affiliation = result(title, comment, organization, gov_agency, summary, affiliation)
            writer.writerow([comment_id, title, final_affiliation, comment, summary])

scan()

