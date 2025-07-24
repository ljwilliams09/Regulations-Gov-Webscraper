import csv
import json

def load_data():
    with open('meta_data.csv', 'r') as meta, open('training.jsonl', 'w') as output, open('benn_coded.csv', 'r') as benn:
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
            
            if meta_id != benn_id:
                raise Exception("ID's DO NOT MATCH")
            
            expected_output = f"{affiliation}|||{individual}"

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

      






