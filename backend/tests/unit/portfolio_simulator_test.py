"""
TDD - Unit tests for PortfolioSimulator feature.
Tests written FIRST (RED phase) before implementation.
"""
import pytest
from app.services.portfolio_simulator import (
    simulate_portfolio,
    PortfolioAllocation,
    SimulationResult,
    calculate_projected_return,
)


class TestPortfolioAllocation:
    def test_allocate_budget_across_stocks(self):
        stocks = [
            {"symbol": "AAPL", "weight": 0.5},
            {"symbol": "NVDA", "weight": 0.3},
            {"symbol": "MSFT", "weight": 0.2},
        ]
        allocation = PortfolioAllocation(budget=1500.0, stocks=stocks)
        assert allocation.get_amount("AAPL") == pytest.approx(750.0)
        assert allocation.get_amount("NVDA") == pytest.approx(450.0)
        assert allocation.get_amount("MSFT") == pytest.approx(300.0)

    def test_weights_must_sum_to_one(self):
        stocks = [
            {"symbol": "AAPL", "weight": 0.6},
            {"symbol": "NVDA", "weight": 0.6},
        ]
        with pytest.raises(ValueError, match="Weights must sum to 1.0"):
            PortfolioAllocation(budget=1000.0, stocks=stocks)

    def test_empty_stock_list_raises_value_error(self):
        with pytest.raises(ValueError, match="Stock list cannot be empty"):
            PortfolioAllocation(budget=1000.0, stocks=[])

    def test_negative_weight_raises_value_error(self):
        stocks = [{"symbol": "AAPL", "weight": -0.5}, {"symbol": "NVDA", "weight": 1.5}]
        with pytest.raises(ValueError, match="Weights must be non-negative"):
            PortfolioAllocation(budget=1000.0, stocks=stocks)


class TestSimulatePortfolio:
    def test_simulation_returns_simulation_result(self):
        stocks = [{"symbol": "AAPL", "weight": 1.0}]
        result = simulate_portfolio(budget=1000.0, stocks=stocks, years=1)
        assert isinstance(result, SimulationResult)

    def test_simulation_result_has_projected_value(self):
        stocks = [{"symbol": "AAPL", "weight": 1.0}]
        result = simulate_portfolio(budget=1000.0, stocks=stocks, years=1)
        assert result.projected_value > 0

    def test_simulation_result_has_scenario_breakdown(self):
        stocks = [{"symbol": "AAPL", "weight": 1.0}]
        result = simulate_portfolio(budget=1000.0, stocks=stocks, years=1)
        assert "optimistic" in result.scenarios
        assert "base" in result.scenarios
        assert "pessimistic" in result.scenarios

    def test_longer_horizon_produces_higher_optimistic_value(self):
        stocks = [{"symbol": "AAPL", "weight": 1.0}]
        result_1yr = simulate_portfolio(budget=1000.0, stocks=stocks, years=1)
        result_10yr = simulate_portfolio(budget=1000.0, stocks=stocks, years=10)
        assert result_10yr.scenarios["optimistic"] > result_1yr.scenarios["optimistic"]

    def test_simulation_with_zero_years_raises_value_error(self):
        stocks = [{"symbol": "AAPL", "weight": 1.0}]
        with pytest.raises(ValueError, match="Years must be greater than zero"):
            simulate_portfolio(budget=1000.0, stocks=stocks, years=0)


class TestCalculateProjectedReturn:
    def test_positive_return_rate_grows_investment(self):
        result = calculate_projected_return(principal=1000.0, annual_rate=0.10, years=1)
        assert result == pytest.approx(1100.0)

    def test_compound_growth_over_multiple_years(self):
        result = calculate_projected_return(principal=1000.0, annual_rate=0.10, years=2)
        assert result == pytest.approx(1210.0)

    def test_zero_rate_returns_principal(self):
        result = calculate_projected_return(principal=1000.0, annual_rate=0.0, years=5)
        assert result == pytest.approx(1000.0)
