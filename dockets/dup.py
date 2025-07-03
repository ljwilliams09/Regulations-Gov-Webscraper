import csv

csv_path = '/Users/lucawilliams/Desktop/Summer Research/Regulations-Gov-Webscraper/dockets/docket.csv'

with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    duplicates = set([x for x in header if header.count(x) > 1])

if duplicates:
    print("Duplicate columns found:", duplicates)
else:
    print("No duplicate columns found.")