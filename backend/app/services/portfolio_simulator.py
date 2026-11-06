"""Portfolio simulator: allocation, compound growth, and scenario modelling."""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SimulationResult:
    projected_value: float
    scenarios: Dict[str, float]


class PortfolioAllocation:
    """Distributes a budget across stocks according to their weights."""

    def __init__(self, budget: float, stocks: List[Dict]) -> None:
        if not stocks:
            raise ValueError("Stock list cannot be empty")
        for stock in stocks:
            if stock["weight"] < 0:
                raise ValueError("Weights must be non-negative")
        total = sum(s["weight"] for s in stocks)
        if abs(total - 1.0) > 1e-9:
            raise ValueError("Weights must sum to 1.0")
        self.budget = budget
        self._amounts: Dict[str, float] = {s["symbol"]: budget * s["weight"] for s in stocks}

    def get_amount(self, symbol: str) -> float:
        return self._amounts[symbol]


def calculate_projected_return(principal: float, annual_rate: float, years: int) -> float:
    """Compound growth formula: P * (1 + r)^n."""
    return principal * (1 + annual_rate) ** years


def simulate_portfolio(budget: float, stocks: List[Dict], years: int) -> SimulationResult:
    """Run optimistic / base / pessimistic scenario simulation."""
    if years <= 0:
        raise ValueError("Years must be greater than zero")

    base = calculate_projected_return(budget, 0.10, years)
    optimistic = calculate_projected_return(budget, 0.20, years)
    pessimistic = calculate_projected_return(budget, -0.05, years)

    return SimulationResult(
        projected_value=base,
        scenarios={"base": base, "optimistic": optimistic, "pessimistic": pessimistic},
    )
