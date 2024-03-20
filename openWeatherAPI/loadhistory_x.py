import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import time
import ssl

def save_data(data, city, province, end_date):
    if not data.empty:
        data.insert(0, 'province', province)
        data.insert(0, 'city', city)
        
        filename = f"weather-data-{city}-{end_date.strftime('%Y%m%d')}.csv"
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


# convert date to unix timestamp
def to_unix_time(date):
    return int(datetime.timestamp(date))

# make an api call for a specific date
def fetch_weather_data(lat, lon, date, api_key):
    try:
        unix_time = to_unix_time(date)
        url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={unix_time}&appid={api_key}&units=metric"
        response = requests.get(url)
        return response.json()
    except requests.exceptions.SSLError:
        # Handle SSL Error by saving the data fetched so far
        if not period_data.empty:
            save_data(period_data, city, province, end_date)
        print("SSL Error occurred. Data fetched so far has been saved.")
        return None

# convert unix timestamp to human-readable format
def timestamp_to_readable(unix_time):
    if pd.isna(unix_time):
        return np.nan
    return datetime.utcfromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')

# extract and transform the data from the JSON column into separate columns
def transform_data(data_dict, new_columns):
    new_row = {col: data_dict.get(col, np.nan) for col in new_columns}

    if 'weather' in data_dict and isinstance(data_dict['weather'], list):
        weather_info = data_dict['weather'][0] if data_dict['weather'] else {}
        new_row['weather'] = weather_info.get('main', np.nan)

    for time_key in ['dt', 'sunrise', 'sunset']:
        if time_key in new_row:
            new_row[time_key] = timestamp_to_readable(new_row[time_key])
    
    return pd.Series(new_row)

######################################################

# Replace with your API key
api_key = '50962ff9bc1b62f99b62f190b269d911'

# TODO: latitude and longitude
latitude = 60.7212 
longitude =  -135.0568

# TODO: city and province
city = "Whitehorse"
province = "Yukon"


# New column names for extraction (without 'uvi')
new_columns = [
    'dt', 'sunrise', 'sunset', 'temp', 'feels_like', 'pressure',
    'humidity', 'dew_point', 'clouds', 'visibility',
    'wind_speed', 'wind_deg', 'weather'
]

# User-specified start and end dates
start_date = datetime.strptime("2021-07-06", '%Y-%m-%d')  
end_date = datetime.strptime("2023-02-25", '%Y-%m-%d')  


###################################################################

# Fetch and process the weather data for the specified period
period_data = pd.DataFrame()
for current_date in pd.date_range(start_date, end_date, freq='D'):
    daily_data = fetch_weather_data(latitude, longitude, current_date, api_key)
    print(daily_data)
    if 'data' in daily_data and isinstance(daily_data['data'], list):
        for hourly_data in daily_data['data']:
            transformed_row = transform_data(hourly_data, new_columns)
            period_data = pd.concat([period_data, transformed_row.to_frame().T], ignore_index=True)

# Add city and province to the DataFrame if any data has been fetched
if not period_data.empty:
    period_data.insert(0, 'province', province)
    period_data.insert(0, 'city', city)
    
    # Save the period data to a CSV file
    filename = f"weather-data-fix-{city}-{end_date.strftime('%Y%m%d')}.csv"
    period_data.to_csv(filename, index=False)
else:
    print(f"No data fetched for period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
 