"""
Sentiment Surfer - Step 1: Ticker Finder
Scans text for stock tickers and counts how often each one is mentioned.
Later, the text will come from Reddit. For now, it uses sample posts.
"""

import re
from collections import Counter

# A small starter list of real tickers. Later we'll load full lists
# from the TSX, NYSE and Nasdaq.
KNOWN_TICKERS = {
    # US
    "AAPL", "TSLA", "NVDA", "AMD", "MSFT", "AMZN", "META", "GOOGL", "PLTR", "GME",
    # Canada (TSX)
    "SHOP", "RY", "TD", "ENB", "CNQ", "SU", "BNS", "BMO", "AC", "WEED",
}

# Words that look like tickers but usually aren't, unless written with a $.
FALSE_MATCHES = {
    "IT", "ALL", "CEO", "DD", "YOLO", "USA", "CAD", "USD", "EPS", "IMO",
    "ATH", "TD", "SU", "AC", "RY", "ON", "A", "I",
}

# $TSLA, $shop, or SHOP.TO style
CASHTAG = re.compile(r"\$([A-Za-z]{1,5})(?:\.TO)?\b")
PLAIN = re.compile(r"\b([A-Z]{1,5})(?:\.TO)?\b")


def find_tickers(text):
    """Return a list of tickers mentioned in one post or comment."""
    found = []

    # Cashtags are the most reliable, so they always count.
    for match in CASHTAG.findall(text):
        ticker = match.upper()
        if ticker in KNOWN_TICKERS:
            found.append(ticker)

    # Plain uppercase words only count if they aren't common false matches.
    for match in PLAIN.findall(text):
        if match in KNOWN_TICKERS and match not in FALSE_MATCHES:
            found.append(match)

    # Count each ticker once per post, so one person spamming it doesn't skew things.
    return list(set(found))


def count_mentions(posts):
    """Count how many posts mention each ticker."""
    counts = Counter()
    for post in posts:
        counts.update(find_tickers(post))
    return counts


if __name__ == "__main__":
    sample_posts = [
        "Loading up on $TSLA before earnings, IT could rip",
        "NVDA and AMD both looking strong this week",
        "Anyone else holding SHOP.TO? Canadian tech is back",
        "$RY dividend is solid, boring but reliable",
        "TSLA TSLA TSLA to the moon",
        "My CEO said ALL hands meeting tomorrow, no stocks talk",
        "Thinking about $ENB and CNQ for my TFSA",
        "PLTR is overvalued imo, but NVDA is fine",
    ]

    results = count_mentions(sample_posts)

    print("\nSentiment Surfer - Mention Count")
    print("-" * 32)
    for ticker, count in results.most_common():
        print(f"{ticker:<8} {count} mention(s)")
    print()
