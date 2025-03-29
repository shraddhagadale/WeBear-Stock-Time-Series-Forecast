// index.tsx (Frontend - React/Next.js)

import { useState } from 'react';
import axios from 'axios';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const Home = () => {
  const [ticker, setTicker] = useState("");
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/forecast", { ticker });
      setForecast(response.data);
    } catch (error) {
      console.error("Error fetching forecast:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Card className="w-full max-w-md p-5 shadow-lg rounded-2xl">
        <CardContent>
          <h1 className="text-xl mb-4">Stock Price Forecasting</h1>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter Stock Ticker (e.g., AAPL)"
            className="border p-2 rounded-md w-full mb-4"
          />
          <Button onClick={handleFetch} disabled={loading}>
            {loading ? "Loading..." : "Get Forecast"}
          </Button>

          {forecast && (
            <div className="mt-4">
              <h2 className="text-lg">Forecast Results</h2>
              <p>Previous Close: {forecast.previous_day_info.previous_close}</p>
              <p>Previous Open: {forecast.previous_day_info.previous_open}</p>
              <p>Previous High: {forecast.previous_day_info.previous_high}</p>
              <p>Forecast: {forecast.forecast.join(", ")}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Home;
