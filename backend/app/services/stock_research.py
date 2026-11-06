"""Stock research service: recommendations, ranking, risk filtering, and summaries."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class RiskTolerance(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


@dataclass
class StockRecommendation:
    symbol: str
    score: float
    reasoning: str
    volatility: str = "moderate"

    def __post_init__(self) -> None:
        if not (0 <= self.score <= 10):
            raise ValueError("Score must be between 0 and 10")


@dataclass
class ResearchSummary:
    top_picks: List[StockRecommendation]
    budget: float


# Curated baseline recommendations used when no external data is available.
_BASELINE_RECOMMENDATIONS: List[StockRecommendation] = [
    StockRecommendation(symbol="NVDA", score=9.5, reasoning="Dominant AI chip supplier; data-centre demand growing 3× YoY", volatility="high"),
    StockRecommendation(symbol="MSFT", score=9.0, reasoning="Azure + Copilot integration driving enterprise cloud adoption", volatility="low"),
    StockRecommendation(symbol="AAPL", score=8.5, reasoning="Strong ecosystem loyalty and services revenue expansion", volatility="low"),
    StockRecommendation(symbol="AMZN", score=8.2, reasoning="AWS market leadership and logistics automation", volatility="moderate"),
    StockRecommendation(symbol="GOOGL", score=8.0, reasoning="AI search dominance and YouTube monetisation growth", volatility="moderate"),
    StockRecommendation(symbol="TSLA", score=7.5, reasoning="EV market leader with energy storage growth potential", volatility="high"),
    StockRecommendation(symbol="AMD", score=7.8, reasoning="GPU/CPU gains in AI inference and data-centre workloads", volatility="high"),
    StockRecommendation(symbol="JNJ", score=7.0, reasoning="Defensive healthcare giant with consistent dividend history", volatility="low"),
]


def rank_stocks(stocks: List[StockRecommendation]) -> List[StockRecommendation]:
    """Return stocks sorted by score descending."""
    return sorted(stocks, key=lambda s: s.score, reverse=True)


def filter_stocks_by_risk(
    stocks: List[StockRecommendation], risk: RiskTolerance
) -> List[StockRecommendation]:
    """Keep only stocks whose volatility matches the investor's risk tolerance."""
    if risk == RiskTolerance.LOW:
        return [s for s in stocks if s.volatility == "low"]
    if risk == RiskTolerance.MODERATE:
        return [s for s in stocks if s.volatility in ("low", "moderate")]
    return stocks  # HIGH risk — no filter


def build_research_summary(
    stocks: List[StockRecommendation], budget: float
) -> ResearchSummary:
    """Rank and package stocks into a ResearchSummary."""
    return ResearchSummary(top_picks=rank_stocks(stocks), budget=budget)


def get_recommendations(budget: float, risk_tolerance: RiskTolerance) -> List[StockRecommendation]:
    """Return baseline recommendations filtered and ranked for the given profile."""
    filtered = filter_stocks_by_risk(_BASELINE_RECOMMENDATIONS, risk_tolerance)
    return rank_stocks(filtered)
