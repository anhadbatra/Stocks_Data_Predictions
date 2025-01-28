import awswrangler as wr
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# List of stocks
stocks = ['IBM', 'AAPL']

# Function to get data for multiple stocks
def get_data(stocks):
    for stock_name in stocks:
        print(f"Processing stock: {stock_name}")
        try:
            # Fetch raw data
            df_raw = get_raw_data(stock_name)

            # Visualize data
            visualize_data(df_raw, stock_name)

            # Train model and get predictions
            y_pred, y_test, ts_test = train_model(df_raw)



            # Plot predictions vs actual
            # Plot predictions vs actual
            plt.figure(figsize=(12, 6))

# Combine test data and sort by timestamp for smooth plotting
            test_data = pd.DataFrame({
            'timestamp': ts_test,
            'Actual': y_test,
            'Predicted': y_pred.flatten()
            }).sort_values(by='timestamp')

            plt.plot(test_data['timestamp'], test_data['Actual'], label='Actual Close Price', color='blue')
            plt.plot(test_data['timestamp'], test_data['Predicted'], label='Predicted Close Price', color='red', linestyle='dashed')

            plt.title(f"{stock_name} - Actual vs Predicted Close Prices")
            plt.xlabel('Timestamp')
            plt.ylabel('Close Price')
            plt.legend()
            plt.xticks(rotation=45)  # Rotate timestamps for better readability
            plt.tight_layout()
            plt.show()


        except Exception as e:
            print(f"Error processing {stock_name}: {e}")

# Function to fetch raw data from AWS S3
def get_raw_data(stock_name):
    # Replace with your bucket and path
    s3_path = f"s3://financialdatastocks/{stock_name}.csv"
    print(f"Fetching data from {s3_path}")
    df = wr.s3.read_csv(s3_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure timestamp is in datetime format
    return df

# Function to visualize the raw data
def visualize_data(df, stock_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['1. open'], label='Open Price', color='green')
    plt.plot(df['timestamp'], df['4. close'], label='Close Price', color='blue')
    plt.title(f"{stock_name} - Open vs Close Prices")
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Function to train a linear regression model
def train_model(df):
    x = df[['1. open']]
    y = df[['4. close']]
    timestamps = df['timestamp']

    # Train-test split (timestamps remain unchanged)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Get the test timestamps

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    ts_test = timestamps.iloc[X_test.index]

    # Calculate MSE
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    return y_pred, y_test.values.flatten(), ts_test

# Main function
if __name__ == '__main__':
    get_data(stocks)
