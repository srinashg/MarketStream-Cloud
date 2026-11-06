"""
TDD - Unit tests for TechTrends feature.
Tests written FIRST (RED phase) before implementation.

Analyzes technology and market trends (AI, actuators, EVs, etc.)
to identify high-growth investment opportunities.
"""
import pytest
from app.services.tech_trends import (
    TrendCategory,
    TrendSignal,
    TrendReport,
    analyze_trend,
    get_trending_sectors,
    map_trends_to_stocks,
)


class TestTrendCategory:
    def test_trend_category_has_ai(self):
        assert TrendCategory.AI is not None

    def test_trend_category_has_robotics_and_actuators(self):
        assert TrendCategory.ROBOTICS_AND_ACTUATORS is not None

    def test_trend_category_has_ev(self):
        assert TrendCategory.ELECTRIC_VEHICLES is not None

    def test_trend_category_has_cloud(self):
        assert TrendCategory.CLOUD_COMPUTING is not None

    def test_trend_category_has_energy(self):
        assert TrendCategory.ENERGY is not None


class TestTrendSignal:
    def test_signal_has_category(self):
        signal = TrendSignal(
            category=TrendCategory.AI,
            strength=8.5,
            description="AI infrastructure spend accelerating",
        )
        assert signal.category == TrendCategory.AI

    def test_signal_has_strength(self):
        signal = TrendSignal(
            category=TrendCategory.ROBOTICS_AND_ACTUATORS,
            strength=7.0,
            description="Humanoid robots entering production",
        )
        assert signal.strength == 7.0

    def test_strength_must_be_between_0_and_10(self):
        with pytest.raises(ValueError, match="Strength must be between 0 and 10"):
            TrendSignal(category=TrendCategory.AI, strength=11.0, description="test")

    def test_negative_strength_raises_value_error(self):
        with pytest.raises(ValueError, match="Strength must be between 0 and 10"):
            TrendSignal(category=TrendCategory.AI, strength=-1.0, description="test")


class TestAnalyzeTrend:
    def test_returns_trend_signal(self):
        signal = analyze_trend(TrendCategory.AI)
        assert isinstance(signal, TrendSignal)

    def test_signal_matches_requested_category(self):
        signal = analyze_trend(TrendCategory.ELECTRIC_VEHICLES)
        assert signal.category == TrendCategory.ELECTRIC_VEHICLES

    def test_signal_strength_is_valid_range(self):
        signal = analyze_trend(TrendCategory.CLOUD_COMPUTING)
        assert 0.0 <= signal.strength <= 10.0


class TestGetTrendingSectors:
    def test_returns_list_of_trend_signals(self):
        signals = get_trending_sectors()
        assert isinstance(signals, list)
        assert len(signals) > 0

    def test_signals_sorted_by_strength_descending(self):
        signals = get_trending_sectors()
        strengths = [s.strength for s in signals]
        assert strengths == sorted(strengths, reverse=True)

    def test_returns_trend_signal_instances(self):
        signals = get_trending_sectors()
        for signal in signals:
            assert isinstance(signal, TrendSignal)


class TestMapTrendsToStocks:
    def test_ai_trend_maps_to_nvda(self):
        signal = TrendSignal(
            category=TrendCategory.AI,
            strength=9.0,
            description="AI boom",
        )
        stocks = map_trends_to_stocks([signal])
        assert "NVDA" in stocks

    def test_empty_trends_returns_empty_list(self):
        stocks = map_trends_to_stocks([])
        assert stocks == []

    def test_returns_list_of_strings(self):
        signal = TrendSignal(
            category=TrendCategory.CLOUD_COMPUTING,
            strength=8.0,
            description="Cloud growth",
        )
        stocks = map_trends_to_stocks([signal])
        assert all(isinstance(s, str) for s in stocks)

    def test_no_duplicate_stocks(self):
        signals = [
            TrendSignal(category=TrendCategory.AI, strength=9.0, description="AI"),
            TrendSignal(category=TrendCategory.AI, strength=8.0, description="AI 2"),
        ]
        stocks = map_trends_to_stocks(signals)
        assert len(stocks) == len(set(stocks))
