import pandas as pd
from datetime import datetime, timedelta
import requests

base_url = 'http://history.openweathermap.org/data/2.5/aggregated/day'
api_key = "3c832e85a9550b822b1300212a6ce9e3"

def fetch_weather_data_for_date(date, lat, lon):
    formatted_date = date.strftime('%Y-%m-%d')
    response = requests.get(f'{base_url}?lat={lat}&lon={lon}&month={date.month}&day={date.day}&appid={api_key}')
    if response.status_code == 200:
        print(formatted_date)
        return response.json()
    else:
        print(f"Failed to fetch data for date {formatted_date}: {response.status_code}")
        return None

def fetch_weather_data_for_n_years(n, lat, lon):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=n*365)
    all_weather_data = []
    for current_date in [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]:
        weather_data = fetch_weather_data_for_date(current_date, lat, lon)
        if weather_data:
            all_weather_data.append(weather_data['result'])
    return all_weather_data

def fetch_weather_data_for_all_stations(df):
    all_weather_data = []
    for index, row in df.iterrows():
        longitude, latitude = row['x'], row['y']
        all_weather_data.extend(fetch_weather_data_for_n_years(1, latitude, longitude))
    return all_weather_data

def save_weather_data_to_csv(all_weather_data):
    df = pd.DataFrame(all_weather_data)
    df.to_csv('weather_data_combined.csv', index=False)
    print("Combined weather data saved to weather_data_combined.csv")

def main():
    df = pd.read_csv('vancouver_stations.csv')
    all_weather_data = fetch_weather_data_for_all_stations(df)
    save_weather_data_to_csv(all_weather_data)

main()
