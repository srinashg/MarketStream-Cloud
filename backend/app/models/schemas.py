"""Pydantic request and response models for the MarketStream Cloud API."""
from typing import Dict, List
from pydantic import BaseModel, field_validator, model_validator


class InvestmentProfileRequest(BaseModel):
    budget: float
    risk_tolerance: str
    horizon: str
    short_term_goals: List[str] = []
    long_term_goals: List[str] = []

    @field_validator("budget")
    @classmethod
    def budget_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Budget must be greater than zero")
        return v


class InvestmentProfileResponse(BaseModel):
    id: str
    budget: float
    risk_tolerance: str
    horizon: str
    short_term_goals: List[str]
    long_term_goals: List[str]


class StockWeightItem(BaseModel):
    symbol: str
    weight: float


class SimulationRequest(BaseModel):
    budget: float
    stocks: List[StockWeightItem]
    years: int

    @model_validator(mode="after")
    def weights_must_sum_to_one(self) -> "SimulationRequest":
        total = sum(s.weight for s in self.stocks)
        if abs(total - 1.0) > 0.001:
            raise ValueError("Weights must sum to 1.0")
        return self


class SimulationResponse(BaseModel):
    projected_value: float
    scenarios: Dict[str, float]


class StockRecommendationResponse(BaseModel):
    symbol: str
    score: float
    reasoning: str
    volatility: str


class NewsAnalysisResponse(BaseModel):
    symbol: str
    overall_sentiment: str
    article_count: int


class InvestorProfileResponse(BaseModel):
    name: str
    organization: str
    known_strategy: str


class InvestorPositionResponse(BaseModel):
    investor_name: str
    symbol: str
    action: str


class TrendSignalResponse(BaseModel):
    category: str
    strength: float
    description: str
