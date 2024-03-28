import pandas as pd

df = pd.read_csv('climate-daily.csv')
print(df['STATION_NAME'].unique().shape)
df1 = pd.read_csv('climate-stations.csv')
df1 = df1[['STATION_NAME','ELEVATION']]

merged_df = pd.merge(df, df1, on='STATION_NAME', how='left')
print(merged_df['STATION_NAME'].unique().shape)
merged_df.to_csv('metro_vancouver_climate.csv', index=False)
