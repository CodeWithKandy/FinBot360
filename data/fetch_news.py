import feedparser

def get_finance_news(ticker="AAPL"):
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(rss_url)
    return [(entry.title, entry.link) for entry in feed.entries[:5]]  # Get the top 5 news articles

if __name__ == "__main__":
    for title, link in get_finance_news():
        print(f"Title: {title}\nLink: {link}\n")
# This code fetches the latest finance news articles from Yahoo Finance using RSS feeds.