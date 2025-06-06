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
    return conn.cursor()

def get_data():
    cursor = connection()
    query = """
    SELECT * FROM STOCK_DATA_DW LIMIT 30;
"""
    data = cursor.execute(query)
    
def create_sequences(features,target, seq_length):
    X, y = [], []
    for i in range(len(features) - seq_length):
        X.append(features[i:i + seq_length])
        y.append(target[i + seq_length])
    return np.array(X), np.array(y)

def preliminary_analysis():
    df_data = get_data()
    feature_columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'POLARITY',
                       'COMPOUND', 'POS', 'NEU', 'NEG', 'POSITIVE_KEYWORDS', 'NEGATIVE_KEYWORDS']
    features = df_data[feature_columns]
    target = df_data['CLOSE']

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(features)
    scaled_target = scaler.fit_transform(features['CLOSE'])
    X,y = create_sequences(scaled_data,scaled_target,seq_length=10)
    split = int(0.8 * len(df_data))
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    return X_train,X_test, y_train,y_test

        
def define_model(df_train):
    model = Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=df_train.shape[1]))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model = model.compile(optimizer='adam',metrics=['accuracy'])
    return model

def fit_model(model,X_train,y_train,X_test,y_test,scaler):
    model.fit(X_train,y_train,epochs=5,batch_size=32)
    predictions = model.predict()
    predictions = scaler.inverse_transform(predictions)
    actual = scaler.inverse_transform(y_test)
    mse = mean_squared_error(actual, predictions)
    return predictions , mse

class tcn_model:
    def __init__(self):
        model = Sequential([
            Input(shape=(10,1)),
            Conv1D(64,kernel_size=4,padding="casual",activation='relu'),
            Dense(1)

        ]
        )
        model.compile(optimizer='adam',loss='mse')
    def fit(self,model,X,y):
        self.model.fit(X,y,epochs=5,batch_size=32)
    def predict(self,X):
        return X

def combine_model():
    
        

        
        
        







if __name__ == '__main__':
    





