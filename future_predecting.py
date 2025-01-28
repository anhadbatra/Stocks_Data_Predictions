import tensorflow as tf
import pandas as pd
import awswrangler as wr
from sklearn.preprocessing import MinMaxScaler

def get_raw_data(stock_name):
    # Replace with your bucket and path
    s3_path = f"s3://financialdatastocks/{stock_name}.csv"
    print(f"Fetching data from {s3_path}")
    df = wr.s3.read_csv(s3_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure timestamp is in datetime format
    return df

stocks = ['IBM', 'AAPL']
for stock in stocks:
    df_data = get_raw_data(stock)

    # Split data into training and testing sets
    mid_prices = (df_data['high'] + df_data['low']) / 2
    train_data = mid_prices[int(len(mid_prices) * 0.8)]
    test_data = mid_prices[int(len(mid_prices) * 0.2):]

    scaler = MinMaxScaler()
    train_data = train_data.reshape(-1, 1)
    test_data = test_data.reshape(-1, 1)

    EMA = 0.0
    gamma = 0.1
    for ti in range(len(train_data)):
        EMA = gamma * train_data[ti] + (1 - gamma) * EMA
        train_data[ti] = EMA





