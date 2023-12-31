import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt

data = pd.read_csv('Data/taiwanfuture_all_TX_second.csv', encoding="GB18030")

data['DueMonth'] = data['DueMonth'].str.strip()
data['Time'] = data['Time'].astype(str)
data = data[data['DueMonth'] == '202312'].reset_index(drop=True)

# make time format consistent
data['Time'] = data['Time'].apply(lambda x: '0' * (6 - len(x)) + x if len(x) < 6 else x)
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
data['Time'] = pd.to_datetime(data['Time'], format='%H%M%S').dt.time

# make datetime index
data['datetime'] = data['Date'] + pd.to_timedelta(data['Time'].astype(str))
data.set_index('datetime', inplace=True)
data.drop(['Date', 'Time', 'DueMonth'], axis=1, inplace=True)

# resample data into 1 minute interval
data = data.resample('1Min').agg({'Price':'ohlc', 'Volume':'sum'})

# Split data strategy into two parts: In-hours and After-hours
# Define the time range
in_hours_start_time = pd.to_datetime('08:45:00').time()
in_hours_end_time = pd.to_datetime('13:45:00').time()
after_hours_start_time = pd.to_datetime('15:00:00').time()
after_hours_end_time = pd.to_datetime('05:00:00').time()

# Create boolean masks for the time ranges
in_hours = (data.index.time >= in_hours_start_time) & (data.index.time <= in_hours_end_time)
after_hours = (data.index.time >= after_hours_start_time) | (data.index.time <= after_hours_end_time)

df_in_hours = data[in_hours]
df_after_hours = data[after_hours]

# Check for NaN values before filling
print("Before filling NaNs:")
print(df_after_hours[df_after_hours.index == pd.to_datetime('2023-11-13 15:27:00')])

# Convert the specified columns to numeric type
numeric_columns = ['open', 'high', 'low', 'close']
df_after_hours['Price'][numeric_columns] = df_after_hours['Price'][numeric_columns].apply(pd.to_numeric)

# Fill NaN values using forward-fill
df_in_hours['Price'][numeric_columns].fillna(method='ffill', inplace=True)
df_after_hours['Price'][numeric_columns].fillna(method='ffill', inplace=True)

# Check the DataFrame after filling NaNs
print("\nAfter filling NaNs:")
print(df_after_hours[df_after_hours.index == pd.to_datetime('2023-11-13 15:27:00')])



# fill open, high, low, close price with the previous prices if volume is 0
# df_in_hours['Price']['open'].fillna(method='ffill', inplace=True)
# df_in_hours['Price']['high'].fillna(method='ffill', inplace=True)
# df_in_hours['Price']['low'].fillna(method='ffill', inplace=True)
# df_in_hours['Price']['close'].fillna(method='ffill', inplace=True)
# df_after_hours['Price']['open'].fillna(method='ffill', inplace=True)
# df_after_hours['Price']['high'].fillna(method='ffill', inplace=True)
# df_after_hours['Price']['low'].fillna(method='ffill', inplace=True)
# df_after_hours['Price']['close'].fillna(method='ffill', inplace=True)


# print(df_after_hours[df_after_hours.index == pd.to_datetime('2023-11-13 15:27:00')])
# save data
# df_in_hours.to_csv('Data/in_hours.csv')
# df_after_hours.to_csv('Data/after_hours.csv')

# date_list = list(in_hours.index.unique())

# for date in date_list:

#     daily_data = in_hours.loc[in_hours['Date'] == date]
#     daily_data = daily_data.sort_values(by=['Time']).reset_index(drop=True)
#     daily_data['MA1'] = df['values'].resample('1Min').sum()



#     break
