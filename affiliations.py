import csv
import attachments as a
import comments as c
import titles as t


def main():
    comments = "comments.csv"  # column 0: id, column 1: title 
    results = "affiliations.csv" # column 0: id, column 1: title, column 2: affiliation

    with open(comments, 'r') as f:
        reader = csv.reader(f)
        next(f)
        with open(results, 'a') as r:
            writer = csv.writer(r)
            writer.writerow(["id", "title", "affiliation"])
            for row in reader:

                title = t.scan(row[1])
                if title != "N/A":
                    writer.writerow([row[0], row[1], title])
                    print(f"Affilation of {row[1]} found in title!")
                    continue

                comment = c.scan(row[0])
                if comment != "N/A":
                    writer.writerow([row[0], row[1], comment])
                    print(f"Affilation of {row[1]} found in comment!")
                    continue

                attachment = a.scan(row[0])
                if attachment != "N/A":
                    writer.writerow([row[0], row[1], attachment])
                    print(f"Affilation of {row[1]} found in attachment!")
                    continue
                print(f"Affilation of {row[1]} not found!")
                writer.writerow([row[0], row[1], "n/a"])
                
main()