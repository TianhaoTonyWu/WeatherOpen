import pandas as pd
import os

# Specify the directory where your CSV files are located
directory = '.'

# List to hold data from each CSV file
dataframes = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Construct the full file path
        filepath = os.path.join(directory, filename)
        # Read the CSV file and append it to the list
        dataframes.append(pd.read_csv(filepath))

# Concatenate all the dataframes in the list
merged_dataframe = pd.concat(dataframes, ignore_index=True)

# Sort by ddt
merged_dataframe = merged_dataframe.sort_values(by='dt')

# Specify the filename for the merged CSV
output_filename = 'merged_csv_file.csv'

# Save the merged dataframe to a new CSV file
merged_dataframe.to_csv(output_filename, index=False)

print(f'Merged CSV file has been created: {output_filename}')
