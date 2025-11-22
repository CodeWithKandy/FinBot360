import yfinance as yf
import pandas as pd

def calculate_portfolio_value(holdings):
    portfolio = []
    total_value = 0
    total_cost = 0
    total_daily_change = 0

    for item in holdings:
        ticker = item['ticker']
        shares = item['quantity']
        buy_price = item['buy_price']
        
        try:
            stock = yf.Ticker(ticker)
            # Fetch 2 days of data to calculate daily change
            hist = stock.history(period="5d") # Fetch a bit more to be safe

            if hist.empty or "Close" not in hist:
                raise ValueError("No closing data.")

            latest_price = float(hist["Close"].iloc[-1])
            prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else latest_price
            
            current_value = round(latest_price * shares, 2)
            daily_change_pct = ((latest_price - prev_close) / prev_close) * 100
            daily_change_val = (latest_price - prev_close) * shares
            
            # Growth Calculation
            growth_val = 0
            growth_pct = 0
            cost_basis = 0
            
            if buy_price:
                cost_basis = buy_price * shares
                growth_val = current_value - cost_basis
                growth_pct = ((latest_price - buy_price) / buy_price) * 100
                total_cost += cost_basis

            portfolio.append({
                "Ticker": ticker,
                "Shares": shares,
                "Avg Cost": buy_price if buy_price else "N/A",
                "Current Price": round(latest_price, 2),
                "Market Value": current_value,
                "Daily Change (%)": round(daily_change_pct, 2),
                "Total Return ($)": round(growth_val, 2) if buy_price else "N/A",
                "Total Return (%)": round(growth_pct, 2) if buy_price else "N/A"
            })
            
            total_value += current_value
            total_daily_change += daily_change_val
            
        except Exception as e:
            portfolio.append({
                "Ticker": ticker,
                "Shares": shares,
                "Error": str(e)
            })

    summary = {
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
        "total_growth_val": round(total_value - total_cost, 2) if total_cost > 0 else 0,
        "total_growth_pct": round(((total_value - total_cost) / total_cost) * 100, 2) if total_cost > 0 else 0,
        "total_daily_change": round(total_daily_change, 2)
    }

    return portfolio, summary
