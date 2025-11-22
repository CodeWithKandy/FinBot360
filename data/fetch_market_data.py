import yfinance as yf

def get_stock_data(ticker: str, period='1d', interval='5m'):
    """
    Fetches historical market data for a given stock ticker.

    Parameters:
    ticker (str): The stock ticker symbol.
    period (str): The period of data to fetch (default is '1d').
    interval (str): The interval of data to fetch (default is '1m').

    Returns:
    DataFrame: A DataFrame containing the historical market data.
    """
    # Fetch the data using yfinance
    data = yf.download(ticker, period=period, interval=interval)
    return data.tail(10)  # Return the last 10 rows
    
if __name__ == "__main__":
    print(get_stock_data('AAPL'))