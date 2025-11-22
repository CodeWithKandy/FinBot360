"""
Helper module for yfinance with rate limiting, caching, and error handling
"""
import time
import logging
from functools import lru_cache
from typing import Optional, Dict, Any
import yfinance as yf
import pandas as pd

logger = logging.getLogger(__name__)

# Cache for storing recent API calls to reduce rate limiting
_cache = {}
_cache_timestamps = {}
CACHE_DURATION = 60  # Cache data for 60 seconds

# Rate limiting
_last_request_time = 0
MIN_REQUEST_INTERVAL = 0.5  # Minimum 0.5 seconds between requests


def _rate_limit():
    """Enforce rate limiting between requests"""
    global _last_request_time
    current_time = time.time()
    time_since_last = current_time - _last_request_time
    
    if time_since_last < MIN_REQUEST_INTERVAL:
        sleep_time = MIN_REQUEST_INTERVAL - time_since_last
        time.sleep(sleep_time)
    
    _last_request_time = time.time()


def _get_cached_data(ticker: str, data_type: str = "info"):
    """Get cached data if available and not expired"""
    cache_key = f"{ticker}_{data_type}"
    
    if cache_key in _cache:
        timestamp = _cache_timestamps.get(cache_key, 0)
        if time.time() - timestamp < CACHE_DURATION:
            return _cache[cache_key]
        else:
            # Cache expired, remove it
            del _cache[cache_key]
            del _cache_timestamps[cache_key]
    
    return None


def _set_cached_data(ticker: str, data: Any, data_type: str = "info"):
    """Store data in cache"""
    cache_key = f"{ticker}_{data_type}"
    _cache[cache_key] = data
    _cache_timestamps[cache_key] = time.time()


def get_ticker_info(ticker: str, max_retries: int = 3) -> Optional[Dict]:
    """
    Get ticker info with rate limiting, caching, and retry logic.
    Falls back to history data if info fails.
    
    Args:
        ticker: Stock ticker symbol
        max_retries: Maximum number of retry attempts
        
    Returns:
        Dictionary with ticker info or None if failed
    """
    # Check cache first
    cached_data = _get_cached_data(ticker, "info")
    if cached_data is not None:
        return cached_data
    
    # Enforce rate limiting
    _rate_limit()
    
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if we got valid data - be more lenient with validation
            if info and isinstance(info, dict) and len(info) > 0:
                # Try to get price from multiple possible keys
                price_keys = ['currentPrice', 'regularMarketPrice', 'previousClose', 'regularMarketPreviousClose', 'ask', 'bid']
                has_price = any(info.get(key) is not None for key in price_keys)
                
                # If no price in info, try to get it from history as fallback
                if not has_price:
                    try:
                        hist = stock.history(period="1d", interval="1m")
                        if not hist.empty:
                            latest_price = float(hist['Close'].iloc[-1])
                            info['currentPrice'] = latest_price
                            info['regularMarketPrice'] = latest_price
                            if len(hist) > 1:
                                info['previousClose'] = float(hist['Close'].iloc[-2])
                            has_price = True
                    except Exception as hist_error:
                        logger.debug(f"Could not get price from history for {ticker}: {hist_error}")
                
                # Accept info if it has any useful data (name, symbol, or price)
                if has_price or info.get('longName') or info.get('shortName') or info.get('symbol'):
                    _set_cached_data(ticker, info, "info")
                    return info
                else:
                    logger.warning(f"Info for {ticker} exists but has no useful data")
                    # Still return it, let the UI handle it
                    _set_cached_data(ticker, info, "info")
                    return info
            else:
                # If info is empty, try to get basic data from history
                logger.warning(f"Empty info for {ticker}, trying history fallback")
                try:
                    hist = stock.history(period="5d", interval="1d")
                    if not hist.empty:
                        latest_price = float(hist['Close'].iloc[-1])
                        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else latest_price
                        # Create a minimal info dict from history
                        fallback_info = {
                            'currentPrice': latest_price,
                            'regularMarketPrice': latest_price,
                            'previousClose': prev_close,
                            'symbol': ticker,
                            'longName': ticker
                        }
                        _set_cached_data(ticker, fallback_info, "info")
                        return fallback_info
                except Exception as hist_error:
                    logger.debug(f"History fallback also failed for {ticker}: {hist_error}")
                
                return None
                
        except Exception as e:
            error_str = str(e)
            
            # Handle rate limiting (429 error)
            if "429" in error_str or "Too Many Requests" in error_str:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                    logger.warning(f"Rate limited for {ticker}. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Rate limited for {ticker} after {max_retries} attempts")
                    return None
            
            # Handle other errors
            logger.error(f"Error fetching info for {ticker} (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait 1 second before retry
            else:
                return None
    
    return None


def get_ticker_history(ticker: str, period: str = "5d", interval: str = "1d", max_retries: int = 3) -> pd.DataFrame:
    """
    Get ticker historical data with rate limiting, caching, and retry logic
    
    Args:
        ticker: Stock ticker symbol
        period: Period of data to fetch
        interval: Interval of data
        max_retries: Maximum number of retry attempts
        
    Returns:
        DataFrame with historical data or empty DataFrame if failed
    """
    # Check cache first
    cache_key = f"{ticker}_{period}_{interval}"
    cached_data = _get_cached_data(ticker, cache_key)
    if cached_data is not None:
        return cached_data
    
    # Enforce rate limiting
    _rate_limit()
    
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)
            
            if not hist.empty:
                _set_cached_data(ticker, hist, cache_key)
                return hist
            else:
                logger.warning(f"Empty history for {ticker}")
                return pd.DataFrame()
                
        except Exception as e:
            error_str = str(e)
            
            # Handle rate limiting (429 error)
            if "429" in error_str or "Too Many Requests" in error_str:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff
                    logger.warning(f"Rate limited for {ticker} history. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Rate limited for {ticker} history after {max_retries} attempts")
                    return pd.DataFrame()
            
            # Handle other errors
            logger.error(f"Error fetching history for {ticker} (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                return pd.DataFrame()
    
    return pd.DataFrame()


def clear_cache():
    """Clear the cache (useful for testing or forced refresh)"""
    global _cache, _cache_timestamps
    _cache.clear()
    _cache_timestamps.clear()

