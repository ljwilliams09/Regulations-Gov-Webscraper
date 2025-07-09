import pandas as pd

# Load the CSV file
df = pd.read_csv('/Users/lucawilliams/Desktop/Summer Research/Regulations-Gov-Webscraper/comments_2018.csv')

# Get the name of the first column
first_column = df.columns[0]

# Find duplicate values in the first column
duplicates = df[df.duplicated(subset=[first_column])]

# Print result
if not duplicates.empty:
    print("Duplicates found in the first column:")
    print(duplicates)
else:
    print("No duplicates found in the first column.")