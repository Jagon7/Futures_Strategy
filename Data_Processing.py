import pandas as pd
from datetime import datetime, time, timedelta

def preprocess_data(DUE_MONTH, FILE_PATH='Data/taiwanfuture_all_TX_second.csv'):
    # Read data
    data = pd.read_csv(FILE_PATH, encoding="GB18030")

    # Strip white spaces and filter by due_month
    data['DueMonth'] = data['DueMonth'].str.strip()
    data['Time'] = data['Time'].astype(str)
    data = data[data['DueMonth'] == DUE_MONTH].reset_index(drop=True)

    # Make time format consistent
    data['Time'] = data['Time'].apply(lambda x: '0' * (6 - len(x)) + x if len(x) < 6 else x)

    # Convert 'Date' and 'Time' to datetime
    data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
    data['Time'] = pd.to_datetime(data['Time'], format='%H%M%S').dt.time

    # Create datetime index
    data['datetime'] = data['Date'] + pd.to_timedelta(data['Time'].astype(str))
    data.set_index('datetime', inplace=True)
    data.drop(['Date', 'Time', 'DueMonth'], axis=1, inplace=True)

    # Resample data into 1 minute interval
    data = data.resample('1Min').agg({'Price': 'ohlc', 'Volume': 'sum'})

    # Split data into in-hours and after-hours
    in_hours_start_time = time(8, 45, 0)
    in_hours_end_time = time(13, 45, 0)
    after_hours_start_time = time(15, 0, 0)
    after_hours_end_time = time(5, 0, 0)

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

    return df_in_hours, df_after_hours
