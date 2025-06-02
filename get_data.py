import requests
import os
import pandas as pd
import asyncio
import snowflake.connector

API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

async def connect_snowflake_async():
    loop = asyncio.get_event_loop()
    conn = await loop.run_in_executor(
        None,
        lambda: snowflake.connector.connect(
            user=os.environ.get('SNOWFLAKE_USER'),
            password=os.environ.get('SNOWFLAKE_PASSWORD'),
            account=os.environ.get('SNOWFLAKE_ACCOUNT'),
            warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
            database=os.environ.get('SNOWFLAKE_DATABASE'),
            schema="STOCK_DM"
        )
    )
    return conn

# Usage:
# conn = asyncio.run(connect_snowflake_async())


stock_name = "AAPL"
def get_data():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_name}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    df = data['Time Series (Daily)']
    latest_dates = sorted(df.keys(), reverse=True)[:2]
    df = {date: df[date] for date in latest_dates}
    df = pd.DataFrame.from_dict(df, orient="index")
    df.reset_index(inplace=True)
    df.rename(columns={"index":"timestamp"},inplace=True)
    df =df.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'} )
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(int)
    conn = asyncio.run(connect_snowflake_async())
    cursor = conn.cursor()
    for i,row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO {stock_name.lower()} (index, timestamp, open, high, low, close, volume)
            VALUES (?,?,?,?,?,?,?)
        """, (i, row['timestamp'], row['open'], row['high'], row['low'], row['close'], row['volume']))
        conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    get_data()