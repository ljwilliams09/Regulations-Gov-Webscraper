import csv
import attachments as a
import comments as c
import titles as t



def main():
    comments = "comments.csv"  # column 0: id
    results = "affiliations.csv" # column 0: id, column 1: title, column 2: affiliation, column 3: comment

    with open(comments, 'r') as f:
        reader = csv.reader(f)
        next(f)
        with open(results, 'a') as r:
            writer = csv.writer(r)
            writer.writerow(["id", "title", "affiliation", "comment"])
        
            for row in reader:
                comment = ""
                affiliation = ""
                attachment = ""
                found = False

                comment, affiliation = c.scan(row[0], found)
                if affiliation != "N/A":
                    found = True

                attachment = a.scan(row[0], found)
                if attachment != "N/A":
                    writer.writerow([row[0], row[1], attachment])
                    print(f"Affilation of {row[1]} found in attachment!")
        
                print(f"Affilation of {row[1]} not found!")
                writer.writerow([row[0], row[1], "n/a"])
                
main()