
import sys
import os
import streamlit as st
import pandas as pd

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.styles import apply_styles
from ui.components import render_header, render_metric_card, plot_price_chart, plot_portfolio_allocation
from data.portfolio_simulator import PortfolioManager
from data.historical_charts import get_historical_data
from data.fetch_news import get_finance_news
from utils.yfinance_helper import get_ticker_info, clear_cache

# Page Config
st.set_page_config(page_title="FinBot360 Pro", page_icon="📈", layout="wide")

# Apply Premium Styles
apply_styles()

def main():
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Market Analysis", "Portfolio Tracker"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Clear Cache"):
        clear_cache()
        st.sidebar.success("Cache cleared!")

    # Main Header
    render_header()

    if page == "Market Analysis":
        render_market_analysis()
    elif page == "Portfolio Tracker":
        render_portfolio_tracker()

def render_market_analysis():
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker = st.text_input("Search Ticker", "AAPL", help="Enter stock or crypto symbol (e.g., AAPL, BTC-USD)").upper()
    
    if ticker:
        try:
            with st.spinner(f"Analyzing {ticker}..."):
                info = get_ticker_info(ticker)
                
                if info:
                    # Top Metrics Row
                    m1, m2, m3, m4 = st.columns(4)
                    
                    price = info.get('currentPrice') or info.get('regularMarketPrice')
                    prev = info.get('previousClose')
                    
                    if price and prev:
                        delta = price - prev
                        delta_pct = (delta / prev) * 100
                        with m1:
                            render_metric_card("Price", f"${price:,.2f}", f"{delta:+.2f} ({delta_pct:+.2f}%)")
                    
                    with m2:
                        mkt_cap = info.get('marketCap')
                        val = f"${mkt_cap/1e9:.2f}B" if mkt_cap else "N/A"
                        render_metric_card("Market Cap", val)
                        
                    with m3:
                        pe = info.get('trailingPE')
                        render_metric_card("P/E Ratio", f"{pe:.2f}" if pe else "N/A")
                        
                    with m4:
                        vol = info.get('volume')
                        val = f"{vol/1e6:.1f}M" if vol else "N/A"
                        render_metric_card("Volume", val)

                    # Tabs for Chart and News
                    tab1, tab2 = st.tabs(["Technical Chart", "Latest News"])
                    
                    with tab1:
                        period = st.select_slider("Period", options=["1mo", "3mo", "6mo", "1y", "5y"], value="6mo")
                        hist_data = get_historical_data(ticker, period=period)
                        plot_price_chart(hist_data, ticker)
                        
                    with tab2:
                        news = get_finance_news(ticker)
                        if news:
                            for title, link in news:
                                st.markdown(f"""
                                <div class="glass-card" style="margin-bottom: 10px; padding: 15px;">
                                    <a href="{link}" target="_blank" style="text-decoration: none; color: white; font-weight: 500;">
                                        📰 {title}
                                    </a>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No news found.")
                else:
                    st.warning(f"No data available for {ticker}. Please check the ticker symbol.")

        except Exception as e:
            st.error(f"Error analyzing {ticker}: {e}")

def render_portfolio_tracker():
    st.subheader("Your Portfolio")
    
    # Initialize session state for portfolio if not exists
    if 'portfolio_df' not in st.session_state:
        st.session_state.portfolio_df = PortfolioManager.get_default_portfolio()

    # Editable Data Table
    edited_df = st.data_editor(
        st.session_state.portfolio_df,
        num_rows="dynamic",
        column_config={
            "Ticker": st.column_config.TextColumn("Ticker", required=True),
            "Quantity": st.column_config.NumberColumn("Quantity", min_value=0, required=True),
            "Avg Cost": st.column_config.NumberColumn("Avg Cost ($)", min_value=0, required=True),
        },
        use_container_width=True
    )
    
    # Update session state
    st.session_state.portfolio_df = edited_df

    if st.button("Analyze Portfolio", type="primary"):
        if not edited_df.empty:
            pm = PortfolioManager()
            with st.spinner("Calculating portfolio performance..."):
                results, summary = pm.calculate_portfolio(edited_df)
            
            # Summary Cards
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                render_metric_card("Total Value", f"${summary['total_value']:,.2f}")
            with c2:
                render_metric_card("Total Cost", f"${summary['total_cost']:,.2f}")
            with c3:
                render_metric_card("Total Return", f"${summary['total_return']:,.2f}", f"{summary['total_return_pct']:+.2f}%")
            with c4:
                render_metric_card("Daily Change", f"${summary['daily_change']:,.2f}")

            st.divider()
            
            # Charts
            col_chart1, col_chart2 = st.columns(2)
            
            results_df = pd.DataFrame(results)
            
            with col_chart1:
                plot_portfolio_allocation(results_df)
                
            with col_chart2:
                if not results_df.empty:
                    st.dataframe(
                        results_df[['Ticker', 'Current Price', 'Market Value', 'Total Return (%)']],
                        use_container_width=True,
                        hide_index=True
                    )

if __name__ == "__main__":
    main()
