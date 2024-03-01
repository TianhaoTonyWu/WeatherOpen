import os
import pandas as pd

file_paths = [
'weather-data-Yellowknife-20230416.csv',
'weather-data-Yellowknife-20230615.csv',
'weather-data-Yellowknife-20230814.csv',
'weather-data-Yellowknife-20231013.csv',
'weather-data-Yellowknife-20231212.csv',
'weather-data-Yellowknife-20240210.csv',
'weather-data-Yellowknife-20240220.csv']  # Update this list with your actual file paths

for file_path in file_paths:
    if os.path.exists(file_path):
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the 'rain' column exists
        if 'rain' in df.columns:
            # If 'rain' is the last column, remove it
            if df.columns[-1] == 'rain':
                df = df.iloc[:, :-1]  # Remove the last column
            else:
                # If 'rain' is not the last column but still needs to be removed
                df = df.drop(columns=['rain'])
            
            # Save the modified DataFrame back to the CSV file
            df.to_csv(file_path, index=False)
            print(f"Updated {file_path}")
        else:
            print(f"No 'rain' column found in {file_path}. No changes made.")
    else:
        print(f"File {file_path} does not exist.")