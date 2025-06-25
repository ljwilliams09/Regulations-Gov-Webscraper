import openai
import os
from dotenv import load_dotenv

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