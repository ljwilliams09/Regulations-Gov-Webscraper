import csv
import attachments as a
import comments as c
import helpers



def main():
    comments = "comments.csv"  # column 0: id
    results = "affiliations.csv" # column 0: id, column 1: title, column 2: affiliation, column 3: comment, column 4: attachment_summary

    with open(comments, 'r') as f:
        reader = csv.reader(f)
        next(f)
        helpers.write_header(results)
        
        for row in reader:
            comment_id = row[0]
            title, comment, organization, gov_agency = c.scan(comment_id)



            comment, affiliation = c.scan(comment_id, summary, potent_affil)
            summary, potent_affil = a.scan(comment_id)
            comment, affiliation = c.scan(comment_id, summary, potent_affil)
            writer.writerow([row[0], row[1], affiliation, comment, summary])
                
main()

# get title, organization (if any), comment (if any), summary of attachment where is relevant