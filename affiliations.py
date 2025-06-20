import csv
import attachments
import comments
import title


def main():
    comments = "comments.csv"  # column 0: id, column 1: title 
    results = "affiliations.csv" # column 0: id, column 1: title, column 2: affiliation

    with open(comments, 'r') as f:
        reader = csv.reader(f)
        with open(results, 'a') as r:
            writer = csv.writer(r)
            for row in reader:

                title = title.scan(row[1])
                if title != -1:
                    writer.writerow([row[0], row[1], title])
                    continue

                comment = comment.scan(row[0])
                if comment != -1:
                    writer.writerow([row[0], row[1], comment])
                    continue

                attachment = attachment.scan(row[0])
                if attachment != -1:
                    writer.writerow([row[0], row[1], attachment])
                    continue
                
                writer.writerow([row[0], row[1], "n/a"])
                
