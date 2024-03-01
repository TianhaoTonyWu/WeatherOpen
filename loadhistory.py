import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

# convert date to unix timestamp
def to_unix_time(date):
    return int(datetime.timestamp(date))

# make an api call for a specific date
def fetch_weather_data(lat, lon, date, api_key):
    unix_time = to_unix_time(date)
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={unix_time}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# convert unix timestamp to human-readable format
def timestamp_to_readable(unix_time):
    if pd.isna(unix_time):
        return np.nan
    return datetime.utcfromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')

# extract and transform the data from the JSON column into separate columns
def transform_data(row, new_columns):
    if isinstance(row, str):
        try:
            data_list = json.loads(row.replace("'", '"'))
            data_dict = data_list[0] if data_list else {}
        except json.JSONDecodeError:
            return pd.Series({col: np.nan for col in new_columns})
    elif isinstance(row, list) and len(row) > 0:
        data_dict = row[0]
    else:
        return pd.Series({col: np.nan for col in new_columns})
    
    new_row = {col: data_dict.get(col, np.nan) for col in new_columns}

    if 'weather' in data_dict and data_dict['weather']:
        new_row['weather'] = data_dict['weather'][0].get('main', np.nan)

    new_row['rain'] = data_dict.get('rain', {'1h': np.nan}).get('1h', np.nan)
    
    # Convert timestamps to human-readable format
    new_row['dt'] = timestamp_to_readable(new_row['dt'])
    new_row['sunrise'] = timestamp_to_readable(new_row['sunrise'])
    new_row['sunset'] = timestamp_to_readable(new_row['sunset'])
    
    return pd.Series(new_row)


# TODO: Replace with your API key
api_key = "50962ff9bc1b62f99b62f190b269d911"

# TODO: latitude and longitude
latitude = 49.28
longitude = -123.12

# TODO: city and province
city = "Vancouver"
province = "British Columbia"

# TODO: Start and end dates
start_date = datetime(2023, 6, 15)
end_date = datetime(2023, 8, 13)

# define the new column names for extraction (without 'uvi')
new_columns = [
    'dt', 'sunrise', 'sunset', 'temp', 'feels_like', 'pressure',
    'humidity', 'dew_point', 'clouds', 'visibility',
    'wind_speed', 'wind_deg', 'weather', 'rain'
]

# fetch and process the weather data
weather_data = []
for current_date in pd.date_range(start_date, end_date - timedelta(days=1), freq='D'):
    daily_data = fetch_weather_data(latitude, longitude, current_date, api_key)
    print(daily_data)
    weather_data.append(daily_data)

df = pd.DataFrame(weather_data)

# flatten the JSON data into separate columns and convert timestamps
transformed_df = df.apply(lambda row: transform_data(row, new_columns))

# add city and province to the DataFrame if any data has been fetched
transformed_df.insert(0, 'city', city)
transformed_df.insert(0, 'province', province)

# Save the transformed data to a CSV file
# TODO: File name
transformed_df.to_csv('transformed_weather_data-4.csv', index=False)

