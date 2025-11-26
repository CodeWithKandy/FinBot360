
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render_header():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0;">
                <span class="gradient-text">FinBot360</span> <span style="font-weight: 300;">Pro</span>
            </h1>
            <p style="color: #888; font-size: 1.1rem;">Advanced Market Analytics & Portfolio Tracking</p>
        </div>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, delta=None, prefix="", suffix="", help_text=None):
    st.metric(
        label=label,
        value=f"{prefix}{value}{suffix}",
        delta=delta,
        help=help_text
    )

def plot_price_chart(data, ticker, show_sma_20=True, show_sma_50=True):
    if data.empty or 'Close' not in data.columns:
        st.error("No data available for chart.")
        return

    fig = go.Figure()

    # Candlestick if OHLC available, else Line
    if all(col in data.columns for col in ['Open', 'High', 'Low']):
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=data['Close'], 
            mode='lines', 
            name='Close',
            line=dict(color='#4F8BF9', width=2)
        ))

    # SMAs
    if show_sma_20 and 'SMA_20' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=data['SMA_20'], 
            mode='lines', 
            name='SMA 20', 
            line=dict(color='#FFD700', width=1.5)
        ))
        
    if show_sma_50 and 'SMA_50' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=data['SMA_50'], 
            mode='lines', 
            name='SMA 50', 
            line=dict(color='#FF6B6B', width=1.5)
        ))

    fig.update_layout(
        title=dict(text=f"{ticker} Price Action", font=dict(size=20, color="white")),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_portfolio_allocation(df):
    if df.empty:
        return
        
    fig = px.pie(
        df, 
        values='Market Value', 
        names='Ticker', 
        title='Asset Allocation',
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit"),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
