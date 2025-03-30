from fastapi import APIRouter, HTTPException, Request
from app.utils.data_loader import fetch_data, preprocess_data
from app.services.forecasting import train_arima_model
import traceback

router = APIRouter()

@router.post("/forecast")
async def get_forecast(request: Request):
    try:
        data = await request.json()
        ticker = data.get("ticker")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if not ticker:
            raise HTTPException(status_code=400, detail="Ticker is required")

        stock_data = fetch_data(ticker, start_date, end_date)
        processed_data = preprocess_data(stock_data)
        result = train_arima_model(processed_data, stock_data)

        return result
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))