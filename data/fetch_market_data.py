
from utils.yfinance_helper import get_ticker_history

def get_stock_data(ticker: str, period='1d', interval='5m'):
    """
    Fetches historical market data for a given stock ticker.
    Uses the robust helper with rate limiting and caching.
    """
    return get_ticker_history(ticker, period=period, interval=interval)

if __name__ == "__main__":
    print(get_stock_data('AAPL'))