import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

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
    return data


def train_arima_model(data: pd.DataFrame):
    # Split data into training and testing sets
    size = int(len(data) * 0.95)
    train, test = data[:size], data[size:]

    # Fit ARIMA model
    model = ARIMA(train['y'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast
    forecast = model_fit.forecast(steps=len(test))
    rmse = np.sqrt(mean_squared_error(test['y'], forecast))

    # Previous day high, open, and close
    prev_day_info = {
        "previous_close": data['y'][-2],
        "previous_open": data['y'][-2],
        "previous_high": data['y'][-2],
    }

    return forecast.tolist(), prev_day_info
