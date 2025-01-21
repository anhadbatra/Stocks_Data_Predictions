import requests
import os
import pandas as pd

API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')


def stock_raw_data():
    list = ['IBM','AAPL']
    for stock_name in list:
        get_raw_data(stock_name)

def get_raw_data(stock_name):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_name}&interval=5min&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    df = data['Time Series (5min)']
    df = pd.DataFrame.from_dict(df, orient="index")
    df.reset_index(inplace=True)
    df.rename(columns={"index":"timestamp"},inplace=True)
    write_to_S3(df,stock_name)
    return df,stock_name

def write_to_S3(df,stock_name):
    df.to_csv(
    f"s3://{AWS_S3_BUCKET}/{stock_name}.csv",
    index=False,
    storage_options={
        "key": os.environ.get('AWS_ACCESS_KEY_ID'),
        "secret": os.environ.get('AWS_SECRET_ACCESS_KEY'),
        }
)

if __name__ == '__main__':
    stock_raw_data()