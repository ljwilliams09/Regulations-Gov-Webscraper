import csv
import attachments as a
import comments as c
from dotenv import load_dotenv
import openai
from logger_affil import logger
import os
import json
import helpers as h

def result(title, comment, organization, gov_agency, attachment):
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
    with open("./config.json", 'r') as f:
        config = json.load(f)


    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "You will be provided with several variables extracted from a public comment on regulations.gov.\n"
        "Your task is to determine, based solely on the provided variables, whether any organizational affiliation can be identified, whether the comment is from an individual or not, and whether the writer is an expert. Here are the guidelines for each output:\n"
        "Organization: if the comment is written on behalf of an organization (e.g., business, nonprofit, trade association, etc.), or if the comment was submitted by an organization on behalf of an individual, or if the writer identifies as a member of an organization, name that organization. Otherwise give 'None'.\n"
        "Individual: if the commenter is an individual expressing their own ideas, not writing on behalf of an organization, give 1. Otherwise give 0.\n"
        "Expert: if the commenter is an individual with a relevant professional qualification (e.g., an employee of a company, an accountant), or if the comment is written on behalf of an organization, give 1. Otherwise give 0.\n"
        "### Input:\n"
        f"- Title: {title}\n"
        f"- Comment: {comment}\n"
        f"- Organization: {organization}\n"
        f"- Government Agency: {gov_agency}\n"
        f"- Attachment: {attachment}\n\n"
        "### Output:\n"
        "Respond with a single line of output formatted following the guidelines above:\n"
        "<ORGANIZATION>|||<INDIVIDUAL>|||<EXPERT>"
    )

    response = client.chat.completions.create(
        model=config["assessment_model"],
        messages=[
            {"role" : "system", "content" : "You are a data analyst who only returns data in the exact format as specified."},
            {"role" : "user", "content" : prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content



def scan():
    with open("./config.json") as f:
        config = json.load(f)
    comments = config["comments"]  # column 0: id
    results = config["results"] # column 0: id, column 1: title, column 2: affiliation, column 3: comment, column 4: attachment_summary

    with open(comments, 'r') as f:
        reader = csv.reader(f)
        next(f)
        with open(results, 'w ') as r:
            writer = csv.writer(r)
            writer.writerow(["id", "organizaiton", "individual"])
            for row in reader:
                comment_id = row[0]
                attachment = a.scan(comment_id)
                title, comment, organization, gov_agency = c.scan(comment_id)
                logger.info(f"Looking at Comment: {comment_id}")
                logger.info(f"Title: {title}")
                logger.info(f"Comment: {comment}")
                logger.info(f"Organization: {organization}")
                logger.info(f"Gov_Agency: {gov_agency}")
                logger.info(f"Attachment: {attachment}")
                final_affiliation = result(title, comment, organization, gov_agency, attachment)
                print(final_affiliation)
                writer.writerow([comment_id] + final_affiliation.split("|||"))
 
scan()

