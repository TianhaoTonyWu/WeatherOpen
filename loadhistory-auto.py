import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import time

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
def transform_data(data_dict, new_columns):
    new_row = {col: data_dict.get(col, np.nan) for col in new_columns}

    if 'weather' in data_dict and isinstance(data_dict['weather'], list):
        weather_info = data_dict['weather'][0] if data_dict['weather'] else {}
        new_row['weather'] = weather_info.get('main', np.nan)

    for time_key in ['dt', 'sunrise', 'sunset']:
        if time_key in new_row:
            new_row[time_key] = timestamp_to_readable(new_row[time_key])
    
    return pd.Series(new_row)

# TODO: Replace with your API key
api_key = "e6a96fa02be96f6a4d9d8eebb8b99063"

# TODO: latitude and longitude
latitude = 62.4539
longitude = -114.3525

# TODO: city and province
city = "Yellowknife"
province = "Northwest Territories"

# define the new column names for extraction (without 'uvi')
new_columns = [
    'dt', 'sunrise', 'sunset', 'temp', 'feels_like', 'pressure',
    'humidity', 'dew_point', 'clouds', 'visibility',
    'wind_speed', 'wind_deg', 'weather'
]

# Define periods for data collection based on an initial end date
def define_periods(initial_end_date, days_per_period, total_periods):
    periods = []
    end_date = initial_end_date
    for _ in range(total_periods):
        start_date = end_date - timedelta(days=days_per_period)
        periods.append((start_date, end_date))
        end_date = start_date - timedelta(days=1)
    return periods

# TODO: Initial end date for the periods
initial_end_date = datetime(2024, 2, 20)

# TODO: Days of a period, loops
periods = define_periods(initial_end_date, 59, 16)

# fetch and process the weather data for each period
for start_date, end_date in periods:
    period_data = pd.DataFrame()
    for current_date in pd.date_range(start_date, end_date, freq='D'):
        daily_data = fetch_weather_data(latitude, longitude, current_date, api_key)
        if 'data' in daily_data and isinstance(daily_data['data'], list):
            for hourly_data in daily_data['data']:
                transformed_row = transform_data(hourly_data, new_columns)
                # print(transformed_row)
                period_data = pd.concat([period_data, transformed_row.to_frame().T], ignore_index=True)
    
    # add city and province to the DataFrame if any data has been fetched
    if not period_data.empty:
        period_data.insert(0, 'province', province)
        period_data.insert(0, 'city', city)
        
        # save the period data to a CSV file
        filename = f"weather-data-{city}-{end_date.strftime('%Y%m%d')}.csv"
        period_data.to_csv(filename, index=False)
    else:
        print(f"No data fetched for period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    time.sleep(60)  # sleep for 60 seconds after fetching data for one period