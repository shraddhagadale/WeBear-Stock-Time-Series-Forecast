import pandas as pd
import numpy as np
import pmdarima as pm
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import matplotlib.pyplot as plt
from app.config.config import settings
import base64
from io import BytesIO

def plot_to_base64():
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def train_arima_model(data: pd.DataFrame, stock_data: pd.DataFrame, 
                      forecast_days: int = 30, train_end_date: str = settings.DEFAULT_END_DATE) -> dict:
    print("Training ARIMA model...")
    
    # Split data into training and testing sets
    size = int(len(data) * 0.95)
    train, test = data[:size], data[size:]
    stock_train, stock_test = stock_data[:len(train)], stock_data[len(train):]

    future_dates = pd.date_range(start=train.index[-1] + pd.Timedelta(days=1), 
                                 periods=forecast_days, freq='D')

    # Fit ARIMA model
    model = pm.auto_arima(train['y'], test='adf', 
                          exogenous=stock_train['Volume'],
                          start_p=1, start_q=1,     
                          max_p=7, max_q=7,
                          d=None, seasonal=True,  
                          start_P=0, start_Q=0,
                          max_P=2, max_Q=2, 
                          m=7, trace=True, 
                          error_action='ignore',  
                          suppress_warnings=True, 
                          stepwise=False, D=1, 
                          information_criterion='aic',
                          n_jobs=-1)

    print("Model fitting complete.")

    # Prepare previous day information
    prev_day_info = {
        "previous_close": float(stock_train['Close'].iloc[-1].values[0]),
        "previous_open": float(stock_train['Open'].iloc[-1].values[0]),
        "previous_high": float(stock_train['High'].iloc[-1].values[0]),
        "volume": float(stock_train['Volume'].iloc[-1].values[0])
    }

    # Forecast
    # forecast, confidence_interval = model.predict(X=test['y'], exogenous=stock_test['Volume'], 
    #                                               n_periods = len(test['y']), return_conf_int = True)
    # forecasts = pd.Series(forecast, index = test['y'][:len(test['y'])].index)
    # lower = pd.Series(confidence_interval[:, 0], index=test['y'][:len(test['y'])].index)
    # upper = pd.Series(confidence_interval[:, 1], index=test['y'][:len(test['y'])].index)

    # rmse = np.sqrt(mean_squared_error(test['y'], forecast))

    last_known_volume = stock_train['Volume'].iloc[-forecast_days:]
    volume_forecast = np.tile(last_known_volume.values.mean(), forecast_days)
    forecast, confidence_interval = model.predict(exogenous=volume_forecast.reshape(-1, 1), 
                                                  n_periods = forecast_days, 
                                                  return_conf_int = True)
    forecasts = pd.Series(forecast, index = future_dates)
    lower = pd.Series(confidence_interval[:, 0], index = future_dates)
    upper = pd.Series(confidence_interval[:, 1], index = future_dates)

    real_for_mape = data['y'].iloc[-forecast_days:]
    pred_for_mape = forecast[:len(real_for_mape)]
    mape = mean_absolute_percentage_error(real_for_mape, pred_for_mape) * 100

    print("Forecasting complete.")

    print(f"MAPE: {mape:.2f}%")

    # Plot Forecast Chart
    plt.figure(figsize=(10, 5))
    plt.plot(train.index, train['y'], label="Training Data")
    plt.plot(forecasts.index, forecasts, color="orange", label="Forecast")
    plt.fill_between(forecasts.index, lower, upper, color='pink', alpha=0.3, label="Confidence Interval")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    forecast_chart = plot_to_base64()

    print("Forecast chart saved.")

    # Plot Moving Average (MAV) Chart
    data['MAV_10'] = data['y'].rolling(window=10).mean()
    data['MAV_50'] = data['y'].rolling(window=50).mean()
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['y'], label="Stock Price")
    plt.plot(data.index, data['MAV_10'], label="10-Day MAV", color="red")
    plt.plot(data.index, data['MAV_50'], label="50-Day MAV", color="green")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    mav_chart = plot_to_base64()

    print("MAV chart saved.")

    # Plot Trend Chart
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['y'], label="Stock Price", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    trend_chart = plot_to_base64()

    print("Trend chart saved.")

    #Plot Future Trend Chart
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['y'], label="Historical Trend", color="blue")
    plt.plot(forecasts.index, forecasts, label="Forecast", color="orange")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    trend_forecast_chart = plot_to_base64()

    return {
        "previous_day_info": prev_day_info,
        "charts": {
            "forecast": forecast_chart,
            "mav": mav_chart,
            "trend": trend_chart,
            "trend_forecast": trend_forecast_chart
        }
    }