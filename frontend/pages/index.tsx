// index.tsx (Frontend - React/Next.js)
import { useState } from 'react';
import axios from 'axios';
import styles from './SearchBar.module.css';    // Importing the CSS for Search Bar & Button
import cardStyles from './Cards.module.css';     // Importing the CSS for Cards



interface StockData {
  previous_day_info: {
    previous_close: number;
    previous_open: number;
    previous_high: number;
    volume: number;
  };
  charts: {
    mav: string;
    forecast: string;
    trend: string;
  };
}

const Home = () => {
  const [ticker, setTicker] = useState("");
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetch = async () => {
    setLoading(true);
    setError(null);
    setStockData(null);

    try {
      const response = await axios.post("http://127.0.0.1:8000/forecast", { ticker });
      setStockData(response.data);
    } catch (error) {
      setError("Failed to fetch data. Please try again.");
      console.error("Error fetching stock data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-container">
      {/* Header Section */}
      <div className={styles.headerContainer}>
        {/* Title */}
        <h1 className={styles.appTitle}>📈 Stock Price Forecasting</h1>

        {/* Search Bar & Button */}
        <div className={styles.searchContainer}>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter Stock Ticker (e.g., AAPL)"
            className={styles.searchBar}
          />
          <button 
            onClick={handleFetch} 
            disabled={loading} 
            className={styles.searchButton}
          >
            Search
          </button>
        </div>
      </div>

      {/* Display Error Message if any */}
      {error && <div className="text-red-500 text-center mb-4">{error}</div>}
      
      {/* Cards Section */}
      {stockData && (
        <div className={cardStyles.cardsContainer}>
          <div className={cardStyles.card}>
            <div className="card-title">Previous Close</div>
            <div className="card-content">{stockData.previous_day_info.previous_close}</div>
          </div>
          <div className={cardStyles.card}>
            <div className="card-title">Previous Open</div>
            <div className="card-content">{stockData.previous_day_info.previous_open}</div>
          </div>
          <div className={cardStyles.card}>
            <div className="card-title">High</div>
            <div className="card-content">{stockData.previous_day_info.previous_high}</div>
          </div>
          <div className={cardStyles.card}>
            <div className="card-title">Volume</div>
            <div className="card-content">{stockData.previous_day_info.volume}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
