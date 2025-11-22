try:
    import streamlit
    print("streamlit: OK")
except ImportError:
    print("streamlit: MISSING")

try:
    import yfinance
    print("yfinance: OK")
except ImportError:
    print("yfinance: MISSING")

try:
    import plotly
    print("plotly: OK")
except ImportError:
    print("plotly: MISSING")

try:
    import feedparser
    print("feedparser: OK")
except ImportError:
    print("feedparser: MISSING")
