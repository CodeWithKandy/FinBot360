import yfinance as yf

def check_yfinance():
    print("--- Checking AAPL Fundamentals ---")
    aapl = yf.Ticker("AAPL")
    info = aapl.info
    print(f"Market Cap: {info.get('marketCap')}")
    print(f"P/E Ratio: {info.get('trailingPE')}")
    print(f"52 Week High: {info.get('fiftyTwoWeekHigh')}")
    
    print("\n--- Checking BTC-USD Data ---")
    btc = yf.Ticker("BTC-USD")
    hist = btc.history(period="1d")
    print(f"BTC-USD Close: {hist['Close'].iloc[-1] if not hist.empty else 'No Data'}")
    print(f"BTC Info: {btc.info.get('name')}")

if __name__ == "__main__":
    check_yfinance()
