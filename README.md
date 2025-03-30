# WeBear : Stock Forecast

## Overview

This project provides a web-based application that forecasts stock prices using advanced time series analysis techniques.  
Users can input a stock ticker along with a date range to visualize historical data and predictive trends through interactive charts.

---

## Features

- **Stock Ticker Search** – Search for any valid stock symbol (e.g., AAPL)
- **Date Range Selection** – Choose start and end dates to customize your analysis
- **Interactive Charts** – Forecast Plot, MAV Plot, and Trend Plot rendered in real-time
- **Loading Spinner** – Shows feedback during data fetch
- **Chart Zoom** – Click charts to view in popup modal with close option
- **Dialog & Toasts** – Smooth user feedback for errors
- **Responsive UI** – Clean and accessible across screen sizes

---

## Tech Stack

| Layer       | Tech Stack                       |
|-------------|----------------------------------|
| Frontend    | React + Next.js                  |
| Backend     | FastAPI                          |
| Styling     | CSS Modules                      |
| Forecasting | ARIMA (AutoRegressive Model)     |
| Visualization | Base64-encoded PNG chart images |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gupta-nakul/Stock-Time-Series-Analysis-Forecast.git
cd Stock-Time-Series-Analysis-Forecast
```
### 2. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```
Visit http://localhost:3000

### 3. Setup Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## How It Works

1. User types a stock symbol and selects a date range
2. Clicks Search 
3. Frontend sends a POST request to backend with:
```json
{
  "ticker": "AAPL",
  "start_date": "2020-01-01",
  "end_date": "2021-01-01"
}
```
4. Backend responds with:
  - Previous Close, Open, High, Volume
  - Base64-encoded charts for MAV, Forecast, Trend and Future Forcast
5. Frontend displays the stats along with interactive charts.




