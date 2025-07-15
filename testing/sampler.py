import csv, random

input_file = "random.csv"
output_file = "30unaffiliated.csv"
with open(input_file) as infile:
    rows = list(csv.reader(infile))

header, data = rows[0], rows[1:]
sample = random.sample(data, 30)  # exactly 70 random rows

with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)
    writer.writerows(sample)