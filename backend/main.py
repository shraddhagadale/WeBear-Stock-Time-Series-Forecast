import traceback
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import fetch_data, preprocess_data, train_arima_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    ticker: str


@app.post("/forecast")
async def get_stock_forecast(request: StockRequest):
    try:
        print(f"Received request for ticker: {request.ticker}")
        # Fetch stock data
        stock_data = fetch_data(request.ticker)
        if stock_data.empty:
            raise HTTPException(status_code=404, detail="Stock data not found")
        
        print(stock_data['Close'].iloc[-1].values)
        
        prev_day_info = {
            "previous_close": float(stock_data['Close'].iloc[-1].values[0]),
            "previous_open": float(stock_data['Open'].iloc[-1].values[0]),
            "previous_high": float(stock_data['High'].iloc[-1].values[0]),
            "volume": float(stock_data['Volume'].iloc[-1].values[0])
        }

        # Preprocess data
        prepared_data = preprocess_data(stock_data)

        # Train ARIMA model and forecast
        result = train_arima_model(prepared_data)
        result['previous_day_info'] = prev_day_info
        print(result)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))