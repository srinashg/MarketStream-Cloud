"""
TDD - Unit tests for MarketNews feature.
Tests written FIRST (RED phase) before implementation.
"""
import pytest
from app.services.market_news import (
    NewsArticle,
    NewsAnalysis,
    parse_news_article,
    analyze_sentiment,
    Sentiment,
    extract_stock_mentions,
    aggregate_news_for_stock,
)


class TestNewsArticle:
    def test_article_has_title(self):
        article = NewsArticle(
            title="NVIDIA Reports Record Revenue",
            source="Reuters",
            content="NVIDIA announced record quarterly revenue...",
            url="https://reuters.com/article/nvda",
        )
        assert article.title == "NVIDIA Reports Record Revenue"

    def test_article_has_source(self):
        article = NewsArticle(
            title="Market Update",
            source="Bloomberg",
            content="Markets rose today...",
            url="https://bloomberg.com/article/1",
        )
        assert article.source == "Bloomberg"

    def test_article_url_must_not_be_empty(self):
        with pytest.raises(ValueError, match="URL cannot be empty"):
            NewsArticle(title="Test", source="Test", content="Test", url="")


class TestAnalyzeSentiment:
    def test_positive_content_returns_positive_sentiment(self):
        content = "Stock surges to record high on strong earnings beat"
        sentiment = analyze_sentiment(content)
        assert sentiment == Sentiment.POSITIVE

    def test_negative_content_returns_negative_sentiment(self):
        content = "Stock plunges amid fears of recession and poor outlook"
        sentiment = analyze_sentiment(content)
        assert sentiment == Sentiment.NEGATIVE

    def test_neutral_content_returns_neutral_sentiment(self):
        content = "Company reports earnings in line with analyst expectations"
        sentiment = analyze_sentiment(content)
        assert sentiment == Sentiment.NEUTRAL

    def test_returns_sentiment_enum_instance(self):
        result = analyze_sentiment("Market is open today")
        assert isinstance(result, Sentiment)


class TestExtractStockMentions:
    def test_extracts_known_ticker_from_content(self):
        content = "AAPL and NVDA both gained today while MSFT remained flat."
        mentions = extract_stock_mentions(content)
        assert "AAPL" in mentions
        assert "NVDA" in mentions
        assert "MSFT" in mentions

    def test_returns_empty_list_for_no_mentions(self):
        content = "The weather was sunny today in California."
        mentions = extract_stock_mentions(content)
        assert mentions == []

    def test_no_duplicate_tickers(self):
        content = "AAPL is up. AAPL continues to climb. AAPL hits record."
        mentions = extract_stock_mentions(content)
        assert mentions.count("AAPL") == 1


class TestAggregateNewsForStock:
    def test_aggregation_returns_news_analysis(self):
        articles = [
            NewsArticle(
                title="NVDA up 5%",
                source="Reuters",
                content="NVDA surges on AI demand",
                url="https://reuters.com/1",
            ),
            NewsArticle(
                title="NVDA outlook positive",
                source="CNBC",
                content="Analysts raise NVDA price target",
                url="https://cnbc.com/1",
            ),
        ]
        analysis = aggregate_news_for_stock("NVDA", articles)
        assert isinstance(analysis, NewsAnalysis)

    def test_aggregation_includes_overall_sentiment(self):
        articles = [
            NewsArticle(
                title="NVDA up",
                source="Reuters",
                content="NVDA surges to all-time high",
                url="https://reuters.com/1",
            ),
        ]
        analysis = aggregate_news_for_stock("NVDA", articles)
        assert analysis.overall_sentiment in list(Sentiment)

    def test_aggregation_includes_article_count(self):
        articles = [
            NewsArticle(title="A", source="S", content="NVDA rises", url="https://s.com/1"),
            NewsArticle(title="B", source="S", content="NVDA grows", url="https://s.com/2"),
        ]
        analysis = aggregate_news_for_stock("NVDA", articles)
        assert analysis.article_count == 2
