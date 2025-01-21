import pandas as pd
import os
import sqlalchemy as sa
import sqlalchemy.engine.url as URL

AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')


def transform_data(stock_name):
    df = pd.read_csv(f"s3://{AWS_S3_BUCKET}/{stock_name}.csv")
    df =df.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'} )
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(int)
    store_data_redshift(df,stock_name)


def store_data_redshift(df,stock_name):
    url = URL.create(
    drivername='redshift+redshift_connector', 
    host='default-workgroup.058264275627.us-east-1.redshift-serverless.amazonaws.com', 
    port=5439, 
    database='', # Amazon Redshift database
    username= os.environ.get('redshift_user'), # Amazon Redshift username
    password= os.environ.get('redshift_password') # Amazon Redshift password
    )
    engine = sa.create_engine(url)
    table_name = f"{stock_name}_stock_data"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
    index INT,
    timestamp TIMESTAMP,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume INT
    );
    """
    engine.execute(create_table_query)
    
def stock_transform_data():
    get_stock_list = ['IBM','AAPL']
    for stock_name in get_stock_list:
        transform_data(stock_name)

if __name__ == '__main__':
    stock_transform_data()