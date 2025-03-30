import yfinance as yf
import pandas as pd
from datetime import date
from app.config.config import settings

# Fetch data from Yahoo Finance
def fetch_data(ticker: str, start_date: date, end_date: date) -> pd.DataFrame:
    print(start_date, end_date)
    if not start_date:
        start_date = settings.DEFAULT_START_DATE
    if not end_date:
        end_date = settings.DEFAULT_END_DATE
    
    # Fetch data from Yahoo Finance
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    return stock_data

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    data = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    data['ds'] = pd.to_datetime(data['ds'])
    data.set_index('ds', inplace=True)
    data = data.asfreq('D')
    data['y'] = data['y'].interpolate(method='linear')
    return data
