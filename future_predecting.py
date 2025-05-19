import tensorflow as tf
import pandas as pd
import awswrangler as wr
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import LSTM, Dense



def get_raw_data(stock_name):
    # Replace with your bucket and path
    s3_path = f"s3://financialdatastocks/{stock_name}.csv"
    df = wr.s3.read_csv(s3_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure timestamp is in datetime format
    return df

def main():
    stocks = ['IBM', 'AAPL']
    for stock in stocks:
        df_data = get_raw_data(stock)

    # Split data into training and testing sets
        high_prices = df_data.loc[:,'2. high'].values
        low_prices = df_data.loc[:,'3. low'].values
        scaler = MinMaxScaler()
        high_prices_scaled = scaler.fit_transform(high_prices.reshape(-1,1))
        low_prices_scaled = scaler.fit_transform(low_prices.reshape(-1,1))
        split = int(0.8 * len(high_prices_scaled))
        high_price_train, high_price_test = high_prices_scaled[:split], high_prices_scaled[split:]
        low_price_train, low_price_test = low_prices_scaled[:split], low_prices_scaled[split:]
        model = Sequential()
        



if __name__ == '__main__':
    get_raw_data()






