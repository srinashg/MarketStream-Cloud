"""Investment profile service: budget, risk tolerance, horizon, and goals."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class RiskTolerance(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class InvestmentHorizon(str, Enum):
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"


@dataclass
class InvestmentProfile:
    budget: float
    risk_tolerance: RiskTolerance
    horizon: InvestmentHorizon
    short_term_goals: List[str] = field(default_factory=list)
    long_term_goals: List[str] = field(default_factory=list)


def validate_budget(budget: float) -> bool:
    if not isinstance(budget, (int, float)) or isinstance(budget, bool):
        raise TypeError("Budget must be a numeric value")
    if budget <= 0:
        raise ValueError("Budget must be greater than zero")
    return True


def create_investment_profile(
    budget: float,
    risk_tolerance: RiskTolerance,
    horizon: InvestmentHorizon,
    short_term_goals: List[str] | None = None,
    long_term_goals: List[str] | None = None,
) -> InvestmentProfile:
    validate_budget(budget)
    return InvestmentProfile(
        budget=budget,
        risk_tolerance=risk_tolerance,
        horizon=horizon,
        short_term_goals=short_term_goals or [],
        long_term_goals=long_term_goals or [],
    )
