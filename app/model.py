import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.layers import LSTM, Dense,Dropout,Input,Conv1D
from tensorflow.keras.models import Sequential
from sklearn.metrics import mean_squared_error
import numpy as np
import snowflake.connector
import os 
from dotenv import load_dotenv

load_dotenv()


def connection():
    conn = snowflake.connector.connect(user = os.environ.get('SNOWFLAKE_USER'),
                                    password = os.environ.get('SNOWFLAKE_PASSWORD'),
                                    account = os.environ.get('SNOWFLAKE_ACCOUNT'),
                                    warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE'),
                                    database = 'STOCK_FACTTABLE_FINAL_DM',
                                    schema = 'STOCK_DM'
    
    
)
    return conn.cursor()

def get_data():
    cursor = connection()
    #cursor.execute("USE DATABASE STOCK_FACTTABLE_FINAL_DM")
    cursor.execute("SELECT * FROM stock_project.stock_facttable_final_dm.stock_dm LIMIT 30;")
    df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
    return df
    
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
    scaled_target = scaler.fit_transform(target.values.reshape(-1,1))
    X,y = create_sequences(scaled_data,scaled_target,seq_length=3)
    split = int(0.8 * min(len(X),len(y)))
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    print("X_train:", X_train.shape, "y_train:", y_train.shape)
    print("X_test:", X_test.shape, "y_test:", y_test.shape)
    return X_train,X_test, y_train,y_test,scaler

        
def define_model(X_train):
    model = Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(X_train.shape[1],X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam',loss='mean_squared_error')
    return model

def fit_model(model,X_train,y_train,X_test,y_test,scaler):
    model.fit(X_train,y_train,epochs=5,batch_size=32)
    predictions = model.predict(X_test)
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
    pass
if __name__ == '__main__':
    X_train,y_train,X_test,y_test,scaler = preliminary_analysis()
    model = define_model(X_train)
    predictions,mse = fit_model(model,X_train,X_test, y_train,y_test,scaler)
    print(predictions,mse)