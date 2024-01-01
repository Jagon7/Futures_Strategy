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

# Convert multi-index to single index
df_in_hours.columns = [col[1] for col in df_in_hours.columns.values]
df_after_hours.columns = [col[1] for col in df_after_hours.columns.values]

# Fill NaN values using forward-fill
na_cols = ['open', 'high', 'low', 'close']
df_in_hours[na_cols] = df_in_hours[na_cols].fillna(method='ffill', inplace=False)
df_after_hours[na_cols] = df_after_hours[na_cols].fillna(method='ffill', inplace=False)


# for date in date_list:

#     daily_data = in_hours.loc[in_hours['Date'] == date]
#     daily_data = daily_data.sort_values(by=['Time']).reset_index(drop=True)
#     daily_data['MA1'] = df['values'].resample('1Min').sum()



#     break
