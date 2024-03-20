import pandas as pd
import os

df = pd.read_csv('climate-stations.csv')
# BC
df = df.where(df['PROV_STATE_TERR_CODE'] == 'BC')
# Modern station
df = df.where(df['STATION_TYPE'] != 'N/A')
df = df.where(pd.to_datetime(df['LAST_DATE']) > pd.to_datetime('2010-01-01 12:30:01'))
# Relevant Cols
df = df[['x','y','STATION_NAME','ELEVATION']]
# lower mainland
df = df.where(df['x'] >  -123.27755834648062)
df = df.where(df['x'] <  -122.18914979566772)
df = df.where(df['y'] > 49.02114496925582)
df = df.where(df['y'] < 49.385658957652986)
# Clean
df = df.dropna()
df = df.drop_duplicates()
# Store
df.to_csv('vancouver_stations.csv', index=False)
