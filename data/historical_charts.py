import yfinance as yf
import pandas as pd
import pandas_ta as ta

def get_historical_data(ticker: str, period="1mo", interval="1d"):
    """
    Fetches historical market data and adds technical indicators.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)
        
        if data.empty:
            raise ValueError("No data found for the given ticker.")
            
        # Add Technical Indicators
        # SMA 20
        data['SMA_20'] = ta.sma(data['Close'], length=20)
        # SMA 50
        data['SMA_50'] = ta.sma(data['Close'], length=50)
        # RSI 14
        data['RSI'] = ta.rsi(data['Close'], length=14)
        
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()