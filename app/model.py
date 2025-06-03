import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.python.keras.layers import LSTM, Dense,Dropout,Input,Conv1D
from tensorflow.python.keras.models import Sequential
from sklearn.metrics import mean_squared_error
import numpy as np
import snowflake.connector
import os 



def connection():
    conn = snowflake.connector.connect(user = os.environ.get('SNOWFLAKE_USER'),
                                    password = os.environ.get('SNOWFLAKE_PASSWORD'),
                                    account = os.environ.get('SNOWFLAKE_ACCOUNT'),
                                    warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE'),
                                    database = os.environ.get('SNOWFLAKE_DATABASE'),
                                    schema = os.environ.get('SNOWFLAKE_SCHEMA')


)

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def premilinary_analysis():
        df_data = get_raw_data(stock)

    # Split data into training and testing sets
        timestamps = df_data['timestamp'].values
        high_prices = df_data.loc[:,'2. high'].values
        low_prices = df_data.loc[:,'3. low'].values
        scaler = MinMaxScaler()
        high_prices_scaled = scaler.fit_transform(high_prices.reshape(-1,1))
        low_prices_scaled = scaler.fit_transform(low_prices.reshape(-1,1))
        split = int(0.8 * len(high_prices_scaled))
        high_price_train, high_price_test = high_prices_scaled[:split], high_prices_scaled[split:]
        low_price_train, low_price_test = low_prices_scaled[:split], low_prices_scaled[split:]
        timestamp_train, timestamp_test = timestamps[:split], timestamps[split:]
        return high_price_train,high_price_test,low_price_train,low_price_test,timestamp_test,timestamp_train
        
def define_model(high_price_train):
    model = Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(high_price_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model = model.compile(optimizer='adam',metrics=['accuracy'])
    return model

def fit_model(model,high_price_train,low_price_train,scaler):
    model.fit(high_price_train,low_price_train,epochs=5,batch_size=32)
    predictions = model.predict(high_price_test)
    predictions = scaler.inverse_transform(predictions)
    actual = scaler.inverse_transform(low_price_test)
    mse = mean_squared_error(actual, predictions)
    return mse

class tcn_model():
    def __init__(self):
        model = Sequential([
            Input(shape=(10,1)),
            Conv1D(64,kernel_size=4,padding="casual",activation='relu'),
            Dense(1)

        ]
        )
        model.compile(optimizer='adam',loss='mse')
        
        
        







if __name__ == '__main__':
    get_raw_data()






