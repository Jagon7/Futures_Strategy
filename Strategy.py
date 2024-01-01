import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt
from Data_Processing import preprocess_data

in_hours_data, after_hours_data = preprocess_data(DUE_MONTH='202312')

# in hours startegy evaluation
# 1. Calculate the moving average of the price
in_hours_data['MA_5min'] = in_hours_data['close'].rolling(5).mean()
in_hours_data['MA_20min'] = in_hours_data['close'].rolling(20).mean()
in_hours_data['MA_60min'] = in_hours_data['close'].rolling(60).mean()

in_hours_data['signal'] = np.where(in_hours_data['MA_5min'] > in_hours_data['MA_20min'], 1, 0)
in_hours_data['return'] = 0.0
DATE = ''
for date in in_hours_data.index.date:
    if date != DATE:
        DATE = date
        print(f"""|||     Date: {DATE}     |||""")
    temp = in_hours_data[in_hours_data.index.date == date]
    long_position, short_position = False, False

    for i in range(len(temp)):
        if temp['signal'].iloc[i] == 1 and not (long_position or short_position):
            long_entry = temp['close'].iloc[i]
            long_position = True
        elif temp['signal'].iloc[i] == 0 and long_position:
            long_exit = temp['close'].iloc[i]
            long_position = False
            in_hours_data.loc[temp.index[i], 'return'] = long_exit - long_entry
        elif temp['signal'].iloc[i] == 0 and not (long_position or short_position):
            short_entry = temp['close'].iloc[i]
            short_position = True
        elif temp['signal'].iloc[i] == 1 and short_position:
            short_exit = temp['close'].iloc[i]
            short_position = False
            in_hours_data.loc[temp.index[i], 'return'] = short_entry - short_exit

in_hours_data['return'].cumsum().plot()
plt.show()
