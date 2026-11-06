"""
TDD - Unit tests for StockResearch feature.
Tests written FIRST (RED phase) before implementation.
"""
import pytest
from app.services.stock_research import (
    StockRecommendation,
    ResearchSummary,
    rank_stocks,
    build_research_summary,
    filter_stocks_by_risk,
    RiskTolerance,
)


class TestStockRecommendation:
    def test_recommendation_has_symbol(self):
        rec = StockRecommendation(
            symbol="AAPL",
            score=8.5,
            reasoning="Strong fundamentals and AI growth",
        )
        assert rec.symbol == "AAPL"

    def test_recommendation_has_score(self):
        rec = StockRecommendation(
            symbol="NVDA",
            score=9.2,
            reasoning="Leading AI chip manufacturer",
        )
        assert rec.score == 9.2

    def test_recommendation_has_reasoning(self):
        rec = StockRecommendation(
            symbol="TSLA",
            score=7.0,
            reasoning="EV market leader with energy storage growth",
        )
        assert rec.reasoning != ""

    def test_score_must_be_between_0_and_10(self):
        with pytest.raises(ValueError, match="Score must be between 0 and 10"):
            StockRecommendation(symbol="AAPL", score=11.0, reasoning="test")

    def test_negative_score_raises_value_error(self):
        with pytest.raises(ValueError, match="Score must be between 0 and 10"):
            StockRecommendation(symbol="AAPL", score=-1.0, reasoning="test")


class TestRankStocks:
    def test_rank_stocks_returns_sorted_list(self):
        stocks = [
            StockRecommendation(symbol="MSFT", score=7.0, reasoning="Cloud growth"),
            StockRecommendation(symbol="NVDA", score=9.5, reasoning="AI dominance"),
            StockRecommendation(symbol="AAPL", score=8.0, reasoning="Ecosystem"),
        ]
        ranked = rank_stocks(stocks)
        assert ranked[0].symbol == "NVDA"
        assert ranked[1].symbol == "AAPL"
        assert ranked[2].symbol == "MSFT"

    def test_rank_stocks_empty_list_returns_empty(self):
        assert rank_stocks([]) == []

    def test_rank_stocks_single_item_returns_same(self):
        stocks = [StockRecommendation(symbol="AAPL", score=8.0, reasoning="test")]
        ranked = rank_stocks(stocks)
        assert len(ranked) == 1
        assert ranked[0].symbol == "AAPL"


class TestFilterStocksByRisk:
    def test_low_risk_returns_only_low_volatility_stocks(self):
        stocks = [
            StockRecommendation(symbol="JNJ", score=7.0, reasoning="Defensive", volatility="low"),
            StockRecommendation(symbol="NVDA", score=9.0, reasoning="Growth", volatility="high"),
        ]
        filtered = filter_stocks_by_risk(stocks, RiskTolerance.LOW)
        assert all(s.symbol == "JNJ" for s in filtered)

    def test_high_risk_returns_all_stocks(self):
        stocks = [
            StockRecommendation(symbol="JNJ", score=7.0, reasoning="Defensive", volatility="low"),
            StockRecommendation(symbol="NVDA", score=9.0, reasoning="Growth", volatility="high"),
        ]
        filtered = filter_stocks_by_risk(stocks, RiskTolerance.HIGH)
        assert len(filtered) == 2


class TestBuildResearchSummary:
    def test_summary_contains_top_picks(self):
        stocks = [
            StockRecommendation(symbol="NVDA", score=9.5, reasoning="AI dominance"),
            StockRecommendation(symbol="AAPL", score=8.0, reasoning="Ecosystem"),
        ]
        summary = build_research_summary(stocks, budget=1500.0)
        assert isinstance(summary, ResearchSummary)
        assert len(summary.top_picks) > 0

    def test_summary_includes_budget(self):
        stocks = [StockRecommendation(symbol="AAPL", score=8.0, reasoning="test")]
        summary = build_research_summary(stocks, budget=1500.0)
        assert summary.budget == 1500.0
