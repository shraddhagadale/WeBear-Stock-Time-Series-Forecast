import pandas as pd
import numpy as np
import yfinance as yf
import pmdarima as pm
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def fetch_data(ticker: str):
    # Fetch data from Yahoo Finance
    stock_data = yf.download(ticker, start="2018-01-01", end="2025-01-01")
    stock_data.reset_index(inplace=True)
    return stock_data


def preprocess_data(data: pd.DataFrame):
    # Prepare data for ARIMA model
    data = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    data['ds'] = pd.to_datetime(data['ds'])
    data.set_index('ds', inplace=True)
    data = data.asfreq('D')
    data['y'].fillna(method='ffill', inplace=True)
    return data


def train_arima_model(data: pd.DataFrame):

    print("Training ARIMA model...")
    # Split data into training and testing sets
    size = int(len(data) * 0.95)
    train, test = data[:size], data[size:]

    print(f"Training set size: {len(train)}, Testing set size: {len(test)}")

    # Fit ARIMA model
    model = pm.auto_arima(train['y'], test = 'adf', 
                          start_p = 1, start_q = 1,     
                          max_p = 3, max_q = 3,
                          d = None, seasonal = False,   
                          start_P = 0, m = 3,
                          trace = True, error_action = 'ignore',  
                          suppress_warnings = True, stepwise = True,
                          D = 1, information_criterion = 'aic')

    print("Model fitting complete.")

    # Forecast
    forecast, confidence_interval = model.predict(X=test['y'], n_periods = len(test['y']), return_conf_int = True)
    forecasts = pd.Series(forecast, index = test['y'][:len(test['y'])].index)
    rmse = np.sqrt(mean_squared_error(test['y'], forecast))

    lower = pd.Series(confidence_interval[:, 0], index=test['y'][:len(test['y'])].index)
    upper = pd.Series(confidence_interval[:, 1], index=test['y'][:len(test['y'])].index)

    print("Forecasting complete.")

    print("Training complete.")
    print(f"RMSE: {rmse}")

    # Plot Forecast Chart
    plt.figure(figsize=(10, 5))
    plt.plot(train.index, train['y'], label="Training Data")
    plt.plot(test.index, test['y'], label="Actual Price", color="blue")
    plt.plot(test.index, forecasts, label="Forecasted Price", color="orange")
    plt.fill_between(test.index, lower, upper, color='pink', alpha=0.2, label="Confidence Interval")
    plt.title("Stock Price Forecast with Confidence Interval")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()

    # Convert forecast plot to base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    forecast_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    print("Forecast chart saved.")

    # Plot Moving Average (MAV) Chart
    data['MAV_10'] = data['y'].rolling(window=10).mean()
    data['MAV_50'] = data['y'].rolling(window=50).mean()
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['y'], label="Stock Price")
    plt.plot(data.index, data['MAV_10'], label="10-Day MAV", color="red")
    plt.plot(data.index, data['MAV_50'], label="50-Day MAV", color="green")
    plt.title("Moving Average (MAV) Chart")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()

    # Convert MAV plot to base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    mav_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    print("MAV chart saved.")

    # Plot Trend Chart
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['y'], label="Stock Price", color="blue")
    plt.title("Trend of Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()

    # Convert trend plot to base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    trend_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    print("Trend chart saved.")

    return {
        "charts": {
            "forecast": forecast_chart,
            "mav": mav_chart,
            "trend": trend_chart
        }
    }
