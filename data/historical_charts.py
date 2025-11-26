import pandas as pd
import pandas_ta as ta
from utils.yfinance_helper import get_ticker_history

def get_historical_data(ticker: str, period="1mo", interval="1d"):
    """
    Fetches historical market data and adds technical indicators.
    Uses rate-limited helper to avoid 429 errors.
    """
    try:
        # Use raise_on_error=True to get actual error messages
        data = get_ticker_history(ticker, period=period, interval=interval, raise_on_error=True)
        
        if data.empty:
            raise ValueError(f"Empty DataFrame returned for {ticker}")
        
        # Ensure we have Close column
        if 'Close' not in data.columns:
            raise ValueError(f"Data missing 'Close' column for {ticker}")
            
        # Add Technical Indicators
        # SMA 20
        data['SMA_20'] = ta.sma(data['Close'], length=20)
        # SMA 50
        data['SMA_50'] = ta.sma(data['Close'], length=50)
        # RSI 14
        data['RSI'] = ta.rsi(data['Close'], length=14)
        
        return data
    except Exception as e:
        # Re-raise the exception so the caller can see the actual error
        raise Exception(f"Error fetching data for {ticker}: {e}") from e