"""
Firestore document models for MarketStream Cloud.

These Pydantic models represent the shape of documents stored in each
Firestore collection.  They are intentionally separate from the API
request/response schemas in schemas.py so the persistence layer can
evolve independently of the API contract.
"""
from datetime import datetime, timezone
from typing import Dict, List, Literal
import uuid

from pydantic import BaseModel, Field, field_validator


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


# ── Shared sub-documents ──────────────────────────────────────────────────────

class StockWeightDocument(BaseModel):
    symbol: str
    weight: float


class RecommendationDocument(BaseModel):
    symbol: str
    score: float
    reasoning: str
    volatility: str


class NewsArticleDocument(BaseModel):
    title: str
    source: str
    url: str
    sentiment: Literal["positive", "negative", "neutral"]


# ── Collection documents ──────────────────────────────────────────────────────

class InvestmentProfileDocument(BaseModel):
    """Firestore: investment_profiles/{id}"""

    id: str = Field(default_factory=_new_id)
    budget: float
    risk_tolerance: Literal["low", "moderate", "high"]
    horizon: Literal["short_term", "medium_term", "long_term"]
    short_term_goals: List[str] = []
    long_term_goals: List[str] = []
    created_at: datetime = Field(default_factory=_now_utc)

    @field_validator("budget")
    @classmethod
    def budget_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Budget must be greater than zero")
        return v


class PortfolioSimulationDocument(BaseModel):
    """Firestore: portfolio_simulations/{id}"""

    id: str = Field(default_factory=_new_id)
    profile_id: str | None = None
    budget: float
    stocks: List[StockWeightDocument]
    years: int
    projected_value: float
    scenarios: Dict[Literal["optimistic", "base", "pessimistic"], float]
    simulated_at: datetime = Field(default_factory=_now_utc)


class StockRecommendationDocument(BaseModel):
    """Firestore: stock_recommendations/{id}"""

    id: str = Field(default_factory=_new_id)
    profile_id: str | None = None
    budget: float
    risk_tolerance: Literal["low", "moderate", "high"]
    recommendations: List[RecommendationDocument]
    generated_at: datetime = Field(default_factory=_now_utc)


class NewsAnalysisDocument(BaseModel):
    """Firestore: news_analyses/{id}"""

    id: str = Field(default_factory=_new_id)
    symbol: str
    overall_sentiment: Literal["positive", "negative", "neutral"]
    article_count: int
    articles: List[NewsArticleDocument] = []
    analysed_at: datetime = Field(default_factory=_now_utc)


class InvestorProfileDocument(BaseModel):
    """Firestore: investor_profiles/{id}"""

    id: str = Field(default_factory=_new_id)
    name: str
    organization: str
    known_strategy: str


class InvestorPositionDocument(BaseModel):
    """Firestore: investor_positions/{id}"""

    id: str = Field(default_factory=_new_id)
    investor_name: str
    symbol: str
    action: Literal["buy", "sell", "hold"]
    recorded_at: datetime = Field(default_factory=_now_utc)


class TrendSignalDocument(BaseModel):
    """Firestore: trend_signals/{id}"""

    id: str = Field(default_factory=_new_id)
    category: Literal[
        "ai",
        "robotics_and_actuators",
        "electric_vehicles",
        "cloud_computing",
        "energy",
    ]
    strength: float
    description: str
    mapped_stocks: List[str] = []
    analysed_at: datetime = Field(default_factory=_now_utc)

    @field_validator("strength")
    @classmethod
    def strength_in_range(cls, v: float) -> float:
        if not (0 <= v <= 10):
            raise ValueError("Strength must be between 0 and 10")
        return v
