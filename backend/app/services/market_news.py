"""Market news service: article parsing, sentiment analysis, and aggregation."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List

# Well-known tickers the extractor recognises.
_KNOWN_TICKERS: set[str] = {
    "AAPL", "NVDA", "MSFT", "TSLA", "GOOGL", "AMZN", "META", "NFLX",
    "AMD", "INTC", "JNJ", "BRK", "V", "JPM", "UNH", "BAC", "KO",
    "NEE", "ENPH", "FSLR", "GM", "F", "NIO", "ABB", "SPCE",
}

_POSITIVE_WORDS: set[str] = {
    "surge", "surges", "gains", "rises", "record", "beat", "beats",
    "strong", "high", "up", "growth", "profit", "positive", "bullish",
    "rally", "climb", "gain", "raise", "raised", "target", "soar",
    "soars", "outperform", "upgrade", "upgraded", "exceeds", "tops",
}
_NEGATIVE_WORDS: set[str] = {
    "plunge", "plunges", "falls", "drops", "recession", "fear", "fears",
    "poor", "loss", "negative", "bearish", "crash", "decline", "weak",
    "miss", "missed", "cut", "down", "downgrade", "downgraded",
    "disappoints", "disappointing", "slump", "slumps", "risks",
}

# Stub news used by the API when no live feed is configured.
_STUB_ARTICLES: dict[str, List[dict]] = {
    "AAPL": [
        {"title": "Apple Services Revenue Surges", "source": "Reuters", "content": "Apple services segment record high on strong subscription growth", "url": "https://reuters.com/aapl/1"},
        {"title": "iPhone Sales Beat Expectations", "source": "CNBC", "content": "iPhone sales beat analyst targets driven by emerging market gains", "url": "https://cnbc.com/aapl/2"},
    ],
    "NVDA": [
        {"title": "NVIDIA Revenue Soars on AI Demand", "source": "Bloomberg", "content": "NVDA surges to record high after data-centre revenue beats expectations", "url": "https://bloomberg.com/nvda/1"},
        {"title": "NVIDIA Raises Guidance", "source": "WSJ", "content": "NVDA raises full-year outlook; bullish on AI chip demand growth", "url": "https://wsj.com/nvda/2"},
    ],
}
_DEFAULT_STUB = [
    {"title": "Markets Steady", "source": "Reuters", "content": "Company reports earnings in line with analyst expectations", "url": "https://reuters.com/default/1"},
]


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class NewsArticle:
    title: str
    source: str
    content: str
    url: str

    def __post_init__(self) -> None:
        if not self.url:
            raise ValueError("URL cannot be empty")


@dataclass
class NewsAnalysis:
    symbol: str
    overall_sentiment: Sentiment
    article_count: int
    articles: List[NewsArticle] = field(default_factory=list)


def parse_news_article(raw: dict) -> NewsArticle:
    return NewsArticle(
        title=raw["title"],
        source=raw["source"],
        content=raw["content"],
        url=raw["url"],
    )


def analyze_sentiment(content: str) -> Sentiment:
    """Score content with keyword matching and return a Sentiment enum."""
    words = set(content.lower().split())
    pos_score = len(words & _POSITIVE_WORDS)
    neg_score = len(words & _NEGATIVE_WORDS)
    if pos_score > neg_score:
        return Sentiment.POSITIVE
    if neg_score > pos_score:
        return Sentiment.NEGATIVE
    return Sentiment.NEUTRAL


def extract_stock_mentions(content: str) -> List[str]:
    """Return unique ticker symbols found in content."""
    seen: List[str] = []
    for word in content.split():
        ticker = word.strip(".,!?;:")
        if ticker in _KNOWN_TICKERS and ticker not in seen:
            seen.append(ticker)
    return seen


def aggregate_news_for_stock(symbol: str, articles: List[NewsArticle]) -> NewsAnalysis:
    """Aggregate sentiment across articles for a given stock symbol."""
    sentiments = [analyze_sentiment(a.content) for a in articles]
    pos = sentiments.count(Sentiment.POSITIVE)
    neg = sentiments.count(Sentiment.NEGATIVE)
    if pos > neg:
        overall = Sentiment.POSITIVE
    elif neg > pos:
        overall = Sentiment.NEGATIVE
    else:
        overall = Sentiment.NEUTRAL
    return NewsAnalysis(symbol=symbol, overall_sentiment=overall, article_count=len(articles), articles=articles)


def get_news_for_symbol(symbol: str) -> NewsAnalysis:
    """Return a NewsAnalysis using stub data (real feed wired in a later milestone)."""
    raw_articles = _STUB_ARTICLES.get(symbol.upper(), _DEFAULT_STUB)
    articles = [parse_news_article(r) for r in raw_articles]
    return aggregate_news_for_stock(symbol.upper(), articles)
