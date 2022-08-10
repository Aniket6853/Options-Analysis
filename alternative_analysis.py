import warnings
from datetime import datetime, timedelta

import numpy
import statsmodels.tsa.stattools as stattools
from matplotlib import pyplot as plt
# Set the figure size - handy for larger
# Set up with a higher resolution screen (useful on Mac)
from pandas import pandas
import seaborn as sns
from scipy.stats import stats

plt.rcParams["figure.figsize"] = [10, 6]

from OptionTrading.OptionTrading.Kite.KiteAuthentication import KiteAuthentication

pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_rows', None)  # or
pandas.set_option('display.max_colwidth', None)  # or 199
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_data(symbol_dic):
    interval = 'day'
    from_date = (datetime.now() - timedelta(days=2000)).replace(hour=9, minute=15)
    to_date = datetime.now()
    
    bank_historical_data = kite.historical_data(instrument_token=symbol_dic['instrument_token'], from_date=from_date, to_date=to_date, interval=interval)
    data_frame = pandas.DataFrame(bank_historical_data)
    data_frame['date'] = pandas.to_datetime(data_frame['date'])
    data_frame['day_name'] = data_frame['date'].dt.day_name()
    data_frame['change'] = data_frame['close'].pct_change(periods=1) * 100
    result_df = pandas.DataFrame()
    for index, row in data_frame.iterrows():
        if row['day_name'] == 'Thursday':
            current_date = row['date']
            last_friday_date = current_date - timedelta(days=6)
            # print(current_date, last_friday_date)
            previous_df = data_frame[(data_frame['date'] >= last_friday_date) & (data_frame['date'] < current_date)]
            mean_df = round(previous_df["change"].sum())
            row['week_change'] = mean_df
            row['thursday_change'] = round(row['change'])
            result_df = result_df.append(row)
    
    result_df.set_index('date', inplace=True)
    print(result_df)
    
    print(len(result_df))
    
    print("Week > 0 and Thu > 0")
    result = result_df.query('week_change >= 3')
    print(result)
    print(result["thursday_change"].mean())
    print(len(result))

    print("Week < 0 and Thu < 0")
    print(len(result_df[(result_df['week_change'] < 0) & (result_df['thursday_change'] < 0)]))

    print("Week < -2 and Thu < -2")
    print(len(result_df[(result_df['week_change'] < 0) & (result_df['thursday_change'] < 0)]))

    print("Week > 2 and Thu > 1")
    print(len(result_df[(result_df['week_change'] < 0) & (result_df['thursday_change'] < 0)]))
    
    # result_df[['week_change', 'thursday_change']].plot()
    # plt.title("Mince Pie Consumption Study")
    # plt.figure(figsize=(15, 5));
    # plt.xlabel("Family Member")
    # plt.ylabel("Pies Consumed")
    # plt.show()



if __name__ == '__main__':
    kite = KiteAuthentication().get_kite_instance()
    
    trading_symbols = [{'symbol': 'BANKNIFTY', 'lot_size': 25, 'trading_symbol': 'BANKNIFTY22JUNFUT', 'instrument_token': '260105', 'brick_size': 0},
                       {'symbol': 'NIFTY 50', 'lot_size': 50, 'trading_symbol': 'NIFTY22JUNFUT', 'instrument_token': '256265', 'brick_size': 0}]
    
    get_data(trading_symbols[0])