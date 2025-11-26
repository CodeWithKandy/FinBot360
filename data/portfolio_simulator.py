
import pandas as pd
import time
from utils.yfinance_helper import get_ticker_history
import logging

logger = logging.getLogger(__name__)

class PortfolioManager:
    def __init__(self):
        pass

    def calculate_portfolio(self, holdings_df):
        """
        Calculate portfolio value based on a DataFrame of holdings.
        Expected columns: 'Ticker', 'Quantity', 'Avg Cost'
        """
        if holdings_df.empty:
            return [], {}

        portfolio_data = []
        total_value = 0.0
        total_cost = 0.0
        total_daily_change = 0.0

        # Iterate through unique tickers
        unique_holdings = holdings_df.groupby('Ticker').agg({
            'Quantity': 'sum',
            'Avg Cost': 'mean' # Simplified: weighted average would be better but keeping it simple for now
        }).reset_index()

        for _, row in unique_holdings.iterrows():
            ticker = row['Ticker']
            shares = float(row['Quantity'])
            avg_cost = float(row['Avg Cost'])
            
            try:
                # Fetch data
                hist = get_ticker_history(ticker, period="5d", interval="1d")
                
                if hist.empty or "Close" not in hist.columns:
                    raise ValueError("No price data found")

                # Calculate metrics
                current_price = float(hist["Close"].iloc[-1])
                prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else current_price
                
                market_value = current_price * shares
                daily_change_pct = ((current_price - prev_close) / prev_close) * 100
                daily_change_val = (current_price - prev_close) * shares
                
                total_return_val = market_value - (avg_cost * shares)
                total_return_pct = ((current_price - avg_cost) / avg_cost) * 100 if avg_cost > 0 else 0
                
                portfolio_data.append({
                    "Ticker": ticker,
                    "Quantity": shares,
                    "Avg Cost": avg_cost,
                    "Current Price": current_price,
                    "Market Value": market_value,
                    "Daily Change (%)": daily_change_pct,
                    "Total Return ($)": total_return_val,
                    "Total Return (%)": total_return_pct
                })
                
                total_value += market_value
                total_cost += (avg_cost * shares)
                total_daily_change += daily_change_val
                
                # Rate limit politeness
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")
                portfolio_data.append({
                    "Ticker": ticker,
                    "Quantity": shares,
                    "Avg Cost": avg_cost,
                    "Current Price": 0.0,
                    "Market Value": 0.0,
                    "Daily Change (%)": 0.0,
                    "Total Return ($)": 0.0,
                    "Total Return (%)": 0.0,
                    "Error": str(e)
                })

        summary = {
            "total_value": total_value,
            "total_cost": total_cost,
            "total_return": total_value - total_cost,
            "total_return_pct": ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            "daily_change": total_daily_change
        }

        return portfolio_data, summary

    @staticmethod
    def get_default_portfolio():
        return pd.DataFrame([
            {"Ticker": "AAPL", "Quantity": 10.0, "Avg Cost": 150.0},
            {"Ticker": "TSLA", "Quantity": 5.0, "Avg Cost": 200.0},
            {"Ticker": "BTC-USD", "Quantity": 0.5, "Avg Cost": 30000.0}
        ])
