# Weather Data Collection
This documentation covers two Python scripts designed for collecting historical weather data using the OpenWeather API. Each script has a different approach to data collection based on the user's needs.

## loadhistory-auto.py
This script automates the process of fetching historical weather data from the OpenWeather API and saving it locally. Considering the OpenWeather API's rate limits of 60 calls per minute and 1,000 free calls per day, this script is designed to fetch data for 60 days in one go, then sleep for 60 seconds before making another fetch. This cycle repeats 16 times.

**Customization Instructions:**

Line 40: Replace with your own API key.

Lines 43-44: Update with the longitude and latitude of the city.

Lines 46-47: Update with the name of the city and province.

Line 68: Update with the end date for the period.

Line 71: In the define_periods function, the first argument should be the number of days you wish to query backward from the end date, and the second argument is the number of cycles (loops) you want to execute.

Output file format: The script generates files named weather-data-CITY-ENDDATE.csv, which you can customize as needed.

## loadhistory.py
This script is designed for users who need to load historical weather data for a custom date range, not exceeding 60 days in total.

**Customization Instructions:**

Line 53: Replace with your own API key.

Lines 56-57: Update with the longitude and latitude of the city.

Lines 60-61: Update with the name of the city and province.

Lines 64-65: Update with the start and end dates for the period.

Line 91: Customize the output CSV file name as desired.

## Common Coordinates for Canadian Cities:
Vancouver, British Columbia

Latitude: 49.2827
Longitude: -123.1216

Edmonton, Alberta

Latitude: 53.5444
Longitude: -113.4909

Regina, Saskatchewan

Latitude: 50.4452
Longitude: -104.6189

Winnipeg, Manitoba

Latitude: 49.8951
Longitude: -97.1384

Toronto, Ontario

Latitude: 43.6532
Longitude: -79.3832

Quebec City, Quebec

Latitude: 46.8139
Longitude: -71.2082

Fredericton, New Brunswick

Latitude: 45.9636
Longitude: -66.6410

Halifax, Nova Scotia

Latitude: 44.6488
Longitude: -63.5752

Charlottetown, Prince Edward Island

Latitude: 46.2382
Longitude: -63.1281

St. John's, Newfoundland and Labrador

Latitude: 47.5615
Longitude: -52.7093

Yellowknife, Northwest Territories

Latitude: 62.4539
Longitude: -114.3525

Iqaluit, Nunavut

Latitude: 63.7467
Longitude: -68.5215

Whitehorse, Yukon

Latitude: 60.7212
Longitude: -135.0568