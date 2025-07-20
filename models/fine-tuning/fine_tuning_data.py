import csv


def load_data():
    with open('meta_data.csv', 'r') as meta, open('training.jsonl', 'we') as test:
        meta_reader = csv.reader(meta)
        next(meta_reader)
        for row in meta_reader:
            title = row[1]
            comment = row[2]
            organization = row[3]
            agency = row[4]
            attachment = row[5]
            prompt = (
                "You will be provided with several variables extracted from a public comment on regulations.gov.\n"
                "Your task is to determine, based solely on the provided variables, whether any affiliation (such as a company, advocacy group, government body, etc.) can be identified and whether it is a comment from an individual or not.\n"
                "### Variables:\n"
                f"- Title: {title}\n"
                f"- Comment: {comment}\n"
                f"- Organization: {organization}\n"
                f"- Government Agency: {agency}\n"
                f"- Attachment: {attachment}\n\n"
                "### Instructions:\n"
                "1. Respond with a single line of output formatted as follows:\n"
                "   <ORGANIZATION>|||<INDIVIDUAL>\n"
                "2. If no affiliation can be determined from a variable, write 'None' in its place.\n"
                "3. For individual, respond 1 if this is an individual, or 2 if it is on behalf of an organization.\n"
                "4. Do not explain or elaborate—just provide the formatted output.\n"
            )






