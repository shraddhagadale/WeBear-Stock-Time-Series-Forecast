# WeBear : Stock Forecast
Predict stock trends with historical & future forecasts using ARIMA.


## Overview

This project provides a web-based application that forecasts stock prices using advanced time series analysis techniques.  
Users can input a stock ticker along with a date range to visualize historical data and predictive trends through interactive charts.


## Features

- **Stock Ticker Search** – Search for any valid stock symbol (e.g., AAPL)
- **Date Range Selection** – Choose start and end dates to customize your analysis
- **Interactive Charts** – Forecast Plot, MAV Plot, and Trend Plot rendered in real-time
- **Loading Spinner** – Shows feedback during data fetch
- **Chart Zoom** – Click charts to view in popup modal with close option
- **Dialog & Toasts** – Smooth user feedback for errors
- **Responsive UI** – Clean and accessible across screen sizes


## Tech Stack 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)


## Installation

### Clone the Repository

```bash
git clone https://github.com/gupta-nakul/Stock-Time-Series-Analysis-Forecast.git
cd Stock-Time-Series-Analysis-Forecast
```
### Docker Setup (Recommended)
```bash
docker-compose up --build
```
Frontend: http://localhost:3000
Backend API: http://localhost:8000

### Setup Frontend

```bash
cd frontend
npm install
npm run dev
```
Runs at: http://localhost:3000

### Setup Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Runs at: http://localhost:8000

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
  - Base64-encoded charts for MAV, Forecast, Trend and Future Forecast
5. Frontend displays the stats along with interactive charts.




