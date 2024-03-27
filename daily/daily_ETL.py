import pandas as pd

df = pd.read_csv('climate-daily.csv')
print(df.columns)
df1 = pd.read_csv('climate-stations.csv')
df1 = df1[['STATION_NAME','ELEVATION']]
print(df1.columns)

merged_df = pd.merge(df, df1, on='STATION_NAME', how='left')
merged_df.to_csv('metro_vancouver_climate.csv', index=False)
