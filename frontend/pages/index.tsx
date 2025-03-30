import { useState } from 'react';
import axios from 'axios';
import Head from 'next/head';
import styles from './SearchBar.module.css';
import cardStyles from './Cards.module.css';
import backgroundStyles from '../styles/Background.module.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';




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
    trend_forecast: string;
  };
}

const Home = () => {
  const [ticker, setTicker] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(false);


  const [error, setError] = useState<string | null>(null);

  const handleFetch = async () => {
    const loading = true; // ⚠️ TEMPORARY override to test visibility

    if (!startDate || !endDate) {
      toast.error("Start Date and End Date are required.");
      return;
    }
  
    if (new Date(endDate) <= new Date(startDate)) {
      toast.error("End Date must be greater than Start Date.");
      return;
    }

    setLoading(true);
    setError(null);
    setStockData(null);

    try {
      const response = await axios.post("http://localhost:8000/forecast", {
        ticker,
        start_date: startDate,
        end_date: endDate
      });
      setStockData(response.data);
    } catch (error) {
      toast.error("Failed to fetch data. Please try again.");
      console.error("Error fetching stock data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Stock Price Forecasting</title>
        <meta name="description" content="Stock Price Forecasting App" />
      </Head>

      <div className={backgroundStyles.backgroundWrapper}>
        <div className={backgroundStyles.waveOverlay} />
      </div>

      <div className="main-container">
      <div className={styles.headerContainer}>
  <div className={styles.topRow}>
    <h1 className={styles.appTitle}>📈 Stock Price Forecasting</h1>

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

  <div className={styles.dateInputsRow}>
    <div className={styles.dateInputGroup}>
      <label htmlFor="start-date">Start Date:</label>
      <input
        type="date"
        id="start-date"
        className={styles.dateInput}
        placeholder="mm/dd/yyyy"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      />
    </div>
    <div className={styles.dateInputGroup}>
      <label htmlFor="end-date">End Date:</label>
      <input
        type="date"
        id="end-date"
        className={styles.dateInput}
        placeholder="mm/dd/yyyy"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      />
    </div>
  </div>
</div>

      

        {error && <div className="text-red-500 text-center mb-4">{error}</div>}

        {loading && (
          <div className={styles.loadingContainer}>
            <div className={styles.spinner}></div>
            <p>Loading data, please wait...</p>
          </div>
        )}

        {stockData && (
          <>
            <div className={cardStyles.infoContainer}>
              <div>High: {stockData.previous_day_info.previous_high.toFixed(2)}</div>
              <div>Close: {stockData.previous_day_info.previous_close.toFixed(2)}</div>
              <div>Open: {stockData.previous_day_info.previous_open.toFixed(2)}</div>
              <div>Volume: {stockData.previous_day_info.volume}</div>
            </div>

            <div className={cardStyles.plotsContainer}>
              <div className={cardStyles.plotItem}>
                <h2>Forecast Plot</h2>
                <img src={`data:image/png;base64,${stockData.charts.forecast}`} alt="Forecast Chart" />
              </div>
              <div className={cardStyles.plotItem}>
                <h2>Future Forecast Plot</h2>
                <img src={`data:image/png;base64,${stockData.charts.trend_forecast}`} alt="Future Forecast Chart" />
              </div>
            </div>

            <div className={cardStyles.plotsContainer}>
              <div className={cardStyles.plotItem}>
                <h2>MAV Plot</h2>
                <img src={`data:image/png;base64,${stockData.charts.mav}`} alt="MAV Chart" />
              </div>
              <div className={cardStyles.plotItem}>
                <h2>Trend Plot</h2>
                <img src={`data:image/png;base64,${stockData.charts.trend}`} alt="Trend Chart" />
              </div>
            </div>
          </>
        )}
      </div>
      <ToastContainer position="top-center" />
    </>
  );
};

export default Home;
