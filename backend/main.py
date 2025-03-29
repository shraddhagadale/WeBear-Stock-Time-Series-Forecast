from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import fetch_data, preprocess_data, train_arima_model

app = FastAPI()

class StockRequest(BaseModel):
    ticker: str


@app.post("/forecast")
async def get_stock_forecast(request: StockRequest):
    try:
        # Fetch stock data
        stock_data = fetch_data(request.ticker)
        if stock_data.empty:
            raise HTTPException(status_code=404, detail="Stock data not found")

        # Preprocess data
        prepared_data = preprocess_data(stock_data)

        # Train ARIMA model and forecast
        forecast, prev_day_info = train_arima_model(prepared_data)

        return {
            "forecast": forecast,
            "previous_day_info": prev_day_info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))