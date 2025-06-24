import os
import logging
import threading
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yfinance as yf
from pycoingecko import CoinGeckoAPI
import requests

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Telegram token securely from env
TOKEN = os.getenv("TG_BOT_TOKEN")
if not TOKEN:
    logger.error("TG_BOT_TOKEN environment variable is missing.")
    exit(1)

# Initialize Telegram bot
app = ApplicationBuilder().token(TOKEN).build()

# In-memory watchlist storage: {user: {"stocks": [...], "crypto": [...]}}
watchlists = {}

# YFinance & CoinGecko clients
cg = CoinGeckoAPI()

def get_stock_price(symbol: str):
    data = yf.Ticker(symbol).history(period="1d", interval="1m")
    if not data.empty:
        return float(data['Close'][-1])
    return None

def get_crypto_price(symbol: str):
    coin = symbol.lower()
    data = cg.get_price(ids=coin, vs_currencies='eur')
    return data.get(coin, {}).get('eur')

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to TradeBrokerAI!\n"
        "Use /watch_stock TSLA, /watch_crypto bitcoin\n"
        "Use /list to view watchlist."
    )

async def watch_stock(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_chat.id
    symbol = ctx.args[0].upper() if ctx.args else None
    if not symbol:
        return await update.message.reply_text("Usage: /watch_stock TSLA")
    watchlists.setdefault(user, {"stocks": [], "crypto": []})
    watchlists[user]["stocks"].append(symbol)
    await update.message.reply_text(f"Added {symbol} to your stock watchlist.")

async def watch_crypto(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_chat.id
    symbol = " ".join(ctx.args).lower() if ctx.args else None
    if not symbol:
        return await update.message.reply_text("Usage: /watch_crypto bitcoin")
    watchlists.setdefault(user, {"stocks": [], "crypto": []})
    watchlists[user]["crypto"].append(symbol)
    await update.message.reply_text(f"Added {symbol} to your crypto watchlist.")

async def list_watchlist(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_chat.id
    wl = watchlists.get(user, {"stocks": [], "crypto": []})
    msg = "Your watchlist:\n"
    msg += "\n".join([f"📈 {s}" for s in wl["stocks"]] + [f"💱 {c}" for c in wl["crypto"]]) or "—Empty—"
    await update.message.reply_text(msg)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("watch_stock", watch_stock))
app.add_handler(CommandHandler("watch_crypto", watch_crypto))
app.add_handler(CommandHandler("list", list_watchlist))

# Background monitoring
def monitor():
    while True:
        for user, wl in watchlists.items():
            for symbol in wl["stocks"]:
                price = get_stock_price(symbol)
                if price:
                    app.bot.send_message(user, f"📈 {symbol}: €{price:.2f}")
            for coin in wl["crypto"]:
                price = get_crypto_price(coin)
                if price:
                    app.bot.send_message(user, f"💱 {coin.capitalize()}: €{price:.2f}")
        time.sleep(60)

threading.Thread(target=monitor, daemon=True).start()

if __name__ == "__main__":
    app.run_polling()
