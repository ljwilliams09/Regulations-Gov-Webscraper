import csv
import json

def load_data():
    meta_data = "meta_data2.csv"
    coded_data = "benn_coded2.csv"
    with open(meta_data, 'r') as meta, open('training.jsonl', 'w') as output, open(coded_data, 'r') as benn:
        benn = csv.reader(benn)
        meta = csv.reader(meta)
        next(meta)
        next(benn)

        for meta, benn in zip(meta, benn):
            # meta data
            meta_id = meta[0]
            title = meta[1]
            comment = meta[2]
            organization = meta[3]
            agency = meta[4]
            attachment = meta[5]

            # coded data from Prof. Benn
            benn_id = benn[0]
            affiliation = benn[1]
            individual = benn[2]
            expert = benn[3]
            
            if meta_id != benn_id:
                raise Exception("ID's DO NOT MATCH")
            
            expected_output = f"{affiliation}|||{individual}|||{expert}"

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
                f"- Government Agency: {agency}\n"
                f"- Attachment: {attachment}\n\n"
                "### Output:\n"
                "Respond with a single line of output formatted following the guidelines above:\n"
                "<ORGANIZATION>|||<INDIVIDUAL>|||<EXPERT>"
            )
            example = {
                "messages" : [
                    {"role": "system", "content": "You are a data analyst who only returns data in the exact format as specified."},
                    {"role": "user", "content" : prompt},
                    {"role": "assistant", "content": expected_output}
                ]
            }
            # Write it as a line in the JSONL file
            json.dump(example, output)
            output.write('\n')


if __name__ == "__main__":
    load_data()

      






