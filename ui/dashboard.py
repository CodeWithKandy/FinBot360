import sys
import os

# Add the root directory (FinBot360/) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

from data.fetch_market_data import get_stock_data
from data.fetch_news import get_finance_news
from data.portfolio_simulator import calculate_portfolio_value
from data.historical_charts import get_historical_data
from data.parser import parse_holdings
from utils.yfinance_helper import get_ticker_info, get_ticker_history

# Page Config
st.set_page_config(page_title="FinBot360 Pro", page_icon="📈", layout="wide")

# Helper function for formatting large numbers
def format_large_number(num):
    if num is None:
        return "N/A"
    if num >= 1_000_000_000_000:
        return f"{num / 1_000_000_000_000:.2f}T"
    elif num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:.2f}"

# Custom CSS for Premium Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Gradient Title */
    .gradient-title {
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FFD700, #1E90FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* Card Styling with Hover Effect */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #1E90FF, #00BFFF);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(30, 144, 255, 0.4);
    }
    
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📈 FinBot360 Pro")

# Global Custom Heading with Gradient
st.markdown("<h1 class='gradient-title'>📉 FinBot360 Pro</h1>", unsafe_allow_html=True)

page = st.sidebar.radio("Navigate", ["Market Analysis", "Portfolio Tracker"])

if page == "Market Analysis":
    st.subheader("Advanced Market Analysis")

    col1, col2 = st.columns([3, 1])

    with col1:
        ticker = st.text_input("Enter Ticker (Stock or Crypto, e.g., AAPL, BTC-USD):", "AAPL").upper()
        
    if ticker:
        try:
            # Fetch Fundamental Data with rate limiting and error handling
            with st.spinner(f"Fetching data for {ticker}..."):
                info = get_ticker_info(ticker)
            
            # Check if info is empty or invalid - check multiple price keys
            price_keys = ['currentPrice', 'regularMarketPrice', 'previousClose', 'regularMarketPreviousClose', 'ask', 'bid']
            has_price = info and any(info.get(key) is not None for key in price_keys)
            
            if not info:
                st.warning(f"⚠️ Could not fetch data for '{ticker}'. Please check the symbol or try again in a moment (rate limit may apply).")
            elif not has_price:
                # Info exists but no price - try to get from history
                st.info("ℹ️ Fetching price from historical data...")
                try:
                    from utils.yfinance_helper import get_ticker_history
                    hist = get_ticker_history(ticker, period="1d", interval="1m")
                    if not hist.empty:
                        latest_price = float(hist['Close'].iloc[-1])
                        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else latest_price
                        # Update info with price from history
                        info['currentPrice'] = latest_price
                        info['regularMarketPrice'] = latest_price
                        info['previousClose'] = prev_close
                        has_price = True
                except Exception:
                    pass
                
                if not has_price:
                    st.warning(f"⚠️ Could not fetch price data for '{ticker}'. Trying to show charts anyway...")
            
            # Display Key Metrics if we have price data
            if info and has_price:
                # Display Key Metrics
                m1, m2, m3, m4 = st.columns(4)
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                prev_close = info.get('previousClose')
                
                if current_price and prev_close:
                    delta = current_price - prev_close
                    m1.metric("Price", f"${current_price:,.2f}", f"{delta:.2f}")
                
                market_cap = info.get('marketCap')
                m2.metric("Market Cap", f"${format_large_number(market_cap)}")
                
                pe_ratio = info.get('trailingPE')
                m3.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
                
                high_52 = info.get('fiftyTwoWeekHigh')
                m4.metric("52W High", f"${high_52:,.2f}" if high_52 else "N/A")
            elif info:
                # Show basic info even without price
                st.info(f"📊 Found data for {ticker}, but price information is limited. Showing charts below...")
            
            # Technical Analysis Tabs (always show)
            tab1, tab2 = st.tabs(["Technical Chart", "News"])
                
                with tab1:
                    period = st.select_slider("Time Period:", options=["1mo", "3mo", "6mo", "1y", "2y", "5y"], value="6mo")
                    
                    hist_data = get_historical_data(ticker, period=period)
                    
                    if not hist_data.empty:
                        # Main Price Chart with SMA
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['Close'], mode='lines', name='Close Price', line=dict(width=2)))
                        
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            if st.checkbox("Show SMA 20", help="Simple Moving Average (20 days). Useful for short-term trends."):
                                fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['SMA_20'], mode='lines', name='SMA 20', line=dict(dash='dash')))
                        with c2:
                            if st.checkbox("Show SMA 50", help="Simple Moving Average (50 days). Useful for medium-term trends."):
                                fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['SMA_50'], mode='lines', name='SMA 50', line=dict(dash='dash')))
                        
                        fig.update_layout(
                            title=f"{ticker} Price Analysis",
                            xaxis_title="Date",
                            yaxis_title="Price",
                            hovermode="x unified"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # RSI Chart
                        with c3:
                            show_rsi = st.checkbox("Show RSI", help="Relative Strength Index. >70 is Overbought, <30 is Oversold.")
                        
                        if show_rsi:
                            fig_rsi = go.Figure()
                            fig_rsi.add_trace(go.Scatter(x=hist_data.index, y=hist_data['RSI'], mode='lines', name='RSI', line=dict(color='#A371F7')))
                            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
                            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
                            fig_rsi.update_layout(
                                title="Relative Strength Index (RSI)",
                                yaxis_title="RSI",
                                height=300,
                                hovermode="x unified"
                            )
                            st.plotly_chart(fig_rsi, use_container_width=True)
                    else:
                        st.warning("No historical data available.")

                with tab2:
                    st.subheader(f"🗞️ Latest News for {ticker}")
                    news = get_finance_news(ticker)
                    if news:
                        for title, link in news:
                            st.markdown(f"• [{title}]({link})")
                    else:
                        st.info("No recent news found.")
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Too Many Requests" in error_msg:
                st.error("🚨 Rate limit exceeded. Please wait a moment and try again. The app is caching data to reduce API calls.")
                st.info("💡 **Tip**: Data is cached for 60 seconds. If you just searched this ticker, wait a moment before searching again.")
            else:
                st.error(f"🚨 Error fetching data: {e}")

elif page == "Portfolio Tracker":
    st.title("💼 Portfolio Tracker & Growth")

    st.info("💡 Tip: Enter buy price to track growth! Format: `TICKER=QTY@PRICE` (e.g., `AAPL=10@150`)")
    portfolio_input = st.text_area("Holdings:", "AAPL=10@150, TSLA=5@200, BTC-USD=0.5@30000")
    
    if st.button("Analyze Portfolio"):
        holdings = parse_holdings(portfolio_input)
        if holdings:
            try:
                with st.spinner("Analyzing portfolio..."):
                    portfolio_data, summary = calculate_portfolio_value(holdings)
                
                # Summary Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Value", f"${summary['total_value']:,.2f}", f"{summary['total_daily_change']:,.2f} (Day)")
                
                c2.metric("Total Cost", f"${summary['total_cost']:,.2f}")
                c3.metric("Total Growth", f"${summary['total_growth_val']:,.2f}", f"{summary['total_growth_pct']:.2f}%")

                st.divider()
                
                # Detailed Breakdown
                st.subheader("📊 Asset Breakdown")
                df = pd.DataFrame(portfolio_data)
                st.dataframe(df, use_container_width=True)
                
                # Charts
                if not df.empty:
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        fig_alloc = px.pie(df, values='Market Value', names='Ticker', title='Portfolio Allocation')
                        st.plotly_chart(fig_alloc, use_container_width=True)
                        
                    with col_chart2:
                        # Filter for items with growth data
                        growth_df = df[df['Total Return ($)'] != "N/A"]
                        if not growth_df.empty:
                            fig_growth = px.bar(growth_df, x='Ticker', y='Total Return ($)', title='Profit/Loss by Asset', color='Total Return ($)', color_continuous_scale=['#FF6B6B', '#51CF66'])
                            st.plotly_chart(fig_growth, use_container_width=True)
            
            except Exception as e:
                st.error(f"🚨 Error analyzing portfolio: {e}")
        else:
            st.warning("⚠️ Please enter valid holdings.")
