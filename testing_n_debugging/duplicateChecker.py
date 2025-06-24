import csv

filename = 'comments.csv'

seen = set()
duplicates = set()

with open(filename, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        comment_id = row['id']
        if comment_id in seen:
            duplicates.add(comment_id)
        else:
            seen.add(comment_id)

print(f"Duplicate IDs found: {duplicates}")
