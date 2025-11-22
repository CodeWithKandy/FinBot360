# 📈 FinBot360 - AI-Powered Financial Trading Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**FinBot360** is a comprehensive financial trading assistant that combines real-time market data, portfolio tracking, and AI-powered analysis. It features both a Telegram bot for quick market updates and a Streamlit dashboard for advanced analytics.

🔗 **Repository**: [https://github.com/CodeWithKandy/FinBot360](https://github.com/CodeWithKandy/FinBot360)

---

## ✨ Features

### 🤖 Telegram Bot
- **Real-time Price Monitoring**: Track stocks and cryptocurrencies with automatic price updates
- **Watchlist Management**: Add/remove stocks and crypto from your personal watchlist
- **Instant Notifications**: Get price alerts every 60 seconds for your watched assets
- **Multi-user Support**: Each user has their own personalized watchlist

### 📊 Streamlit Dashboard
- **Advanced Market Analysis**: 
  - Real-time stock and crypto price data
  - Technical indicators (SMA 20/50, RSI)
  - Interactive charts with Plotly
  - Latest financial news integration
- **Portfolio Tracker**:
  - Track multiple assets with buy prices
  - Calculate total portfolio value and growth
  - Visual allocation charts
  - Profit/loss analysis

### 🧠 AI & ML Capabilities
- Reinforcement Learning trading agents (PPO)
- Risk analysis tools
- Market watch agents
- Portfolio management automation
- Financial RAG (Retrieval-Augmented Generation) for intelligent queries

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (for bot functionality)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodeWithKandy/FinBot360.git
   cd FinBot360
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   TG_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here  # Optional, for AI features
   ```

---

## 📖 Usage

### Running the Telegram Bot

```bash
python main.py --mode bot
```

Or directly:
```bash
python bot.py
```

**Bot Commands:**
- `/start` - Welcome message and instructions
- `/watch_stock TSLA` - Add a stock to your watchlist
- `/watch_crypto bitcoin` - Add a cryptocurrency to your watchlist
- `/list` - View your current watchlist

### Running the Streamlit Dashboard

```bash
python main.py --mode dashboard
```

Or directly:
```bash
streamlit run ui/dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

**Dashboard Features:**
1. **Market Analysis Tab**: Enter any ticker symbol (e.g., AAPL, TSLA, BTC-USD) to view:
   - Current price and market metrics
   - Interactive price charts with technical indicators
   - Latest news articles

2. **Portfolio Tracker Tab**: Enter holdings in format:
   ```
   AAPL=10@150, TSLA=5@200, BTC-USD=0.5@30000
   ```
   This tracks your portfolio value, growth, and allocation.

---

## 📁 Project Structure

```
FinBot360/
├── agents/              # AI agents for trading and analysis
│   ├── market_watch.py
│   ├── portfolio_manager.py
│   ├── risk_analyst.py
│   └── rl_trader.py
├── data/                # Data fetching and processing
│   ├── fetch_market_data.py
│   ├── fetch_news.py
│   ├── historical_charts.py
│   ├── parser.py
│   └── portfolio_simulator.py
├── rag/                 # RAG system for financial queries
│   └── financial_rag.py
├── rl_models/           # Reinforcement Learning models
│   └── ppo_trading_agent.py
├── ui/                  # Streamlit dashboard
│   └── dashboard.py
├── utils/               # Utility functions
│   └── state.py
├── bot.py               # Telegram bot implementation
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🔧 Configuration

### Telegram Bot Setup

1. Create a bot with [@BotFather](https://t.me/botfather) on Telegram
2. Get your bot token
3. Set it as an environment variable:
   ```bash
   # Windows
   set TG_BOT_TOKEN=your_token_here
   
   # macOS/Linux
   export TG_BOT_TOKEN=your_token_here
   ```

### Optional: OpenAI API (for AI features)

If you want to use AI-powered features, set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub (already done if you cloned from the repo)
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click **"New app"**
5. Select repository: `CodeWithKandy/FinBot360`
6. Main file path: `ui/dashboard.py`
7. Click **"Deploy!"**

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

### Deploy Telegram Bot

The bot can be deployed on any cloud platform that supports Python:
- **Heroku**: Use the included `procfile`
- **Railway**: Connect your GitHub repo
- **AWS EC2**: Run as a background service
- **DigitalOcean**: Use a Droplet with systemd service

---

## 📦 Dependencies

Key dependencies include:
- `streamlit` - Web dashboard framework
- `python-telegram-bot` - Telegram bot API
- `yfinance` - Stock market data
- `pycoingecko` - Cryptocurrency data
- `plotly` - Interactive charts
- `pandas-ta` - Technical analysis indicators
- `feedparser` - RSS feed parsing
- `stable-baselines3` - Reinforcement Learning
- `langchain` - AI/LLM integration

See [requirements.txt](requirements.txt) for the complete list.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🐛 Troubleshooting

### Bot not responding?
- Check that `TG_BOT_TOKEN` is set correctly
- Verify your internet connection
- Check bot logs for error messages

### Dashboard not loading?
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 8501 is not in use
- Verify yfinance is working: `python test_yfinance.py`

### Getting "429 Too Many Requests" error?
- **This is a rate limiting issue from Yahoo Finance API**
- The app now includes automatic rate limiting, caching, and retry logic
- Data is cached for 60 seconds to reduce API calls
- If you see this error:
  1. Wait 1-2 minutes before trying again
  2. The app will automatically retry with exponential backoff
  3. Try searching different tickers instead of repeatedly searching the same one
  4. The cache helps - if you just searched a ticker, wait before searching it again

### Import errors?
- Make sure you're in the project root directory
- Activate your virtual environment
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/CodeWithKandy/FinBot360/issues)
- **Repository**: [https://github.com/CodeWithKandy/FinBot360](https://github.com/CodeWithKandy/FinBot360)

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Market data from [Yahoo Finance](https://finance.yahoo.com/) via yfinance
- Crypto data from [CoinGecko](https://www.coingecko.com/)
- Telegram Bot API via [python-telegram-bot](https://python-telegram-bot.org/)

---

**Made with ❤️ by CodeWithKandy**
