"""
TDD - Unit tests for InvestmentProfile feature.
Tests written FIRST (RED phase) before implementation.
"""
import pytest
from app.services.investment_profile import (
    InvestmentProfile,
    RiskTolerance,
    InvestmentHorizon,
    create_investment_profile,
    validate_budget,
)


class TestInvestmentProfileCreation:
    def test_create_profile_with_valid_budget(self):
        profile = create_investment_profile(
            budget=1500.0,
            risk_tolerance=RiskTolerance.MODERATE,
            horizon=InvestmentHorizon.MEDIUM_TERM,
        )
        assert profile.budget == 1500.0

    def test_create_profile_stores_risk_tolerance(self):
        profile = create_investment_profile(
            budget=5000.0,
            risk_tolerance=RiskTolerance.HIGH,
            horizon=InvestmentHorizon.LONG_TERM,
        )
        assert profile.risk_tolerance == RiskTolerance.HIGH

    def test_create_profile_stores_horizon(self):
        profile = create_investment_profile(
            budget=500.0,
            risk_tolerance=RiskTolerance.LOW,
            horizon=InvestmentHorizon.SHORT_TERM,
        )
        assert profile.horizon == InvestmentHorizon.SHORT_TERM

    def test_profile_has_short_term_goals_field(self):
        profile = create_investment_profile(
            budget=2000.0,
            risk_tolerance=RiskTolerance.MODERATE,
            horizon=InvestmentHorizon.SHORT_TERM,
            short_term_goals=["emergency_fund", "car_payment"],
        )
        assert "emergency_fund" in profile.short_term_goals

    def test_profile_has_long_term_goals_field(self):
        profile = create_investment_profile(
            budget=10000.0,
            risk_tolerance=RiskTolerance.MODERATE,
            horizon=InvestmentHorizon.LONG_TERM,
            long_term_goals=["retirement", "home_buying"],
        )
        assert "retirement" in profile.long_term_goals

    def test_default_goals_are_empty_lists(self):
        profile = create_investment_profile(
            budget=1000.0,
            risk_tolerance=RiskTolerance.LOW,
            horizon=InvestmentHorizon.MEDIUM_TERM,
        )
        assert profile.short_term_goals == []
        assert profile.long_term_goals == []


class TestBudgetValidation:
    def test_valid_budget_passes(self):
        assert validate_budget(1500.0) is True

    def test_zero_budget_raises_value_error(self):
        with pytest.raises(ValueError, match="Budget must be greater than zero"):
            validate_budget(0.0)

    def test_negative_budget_raises_value_error(self):
        with pytest.raises(ValueError, match="Budget must be greater than zero"):
            validate_budget(-100.0)

    def test_non_numeric_budget_raises_type_error(self):
        with pytest.raises(TypeError):
            validate_budget("1500")  # type: ignore


class TestRiskToleranceEnum:
    def test_risk_tolerance_has_low(self):
        assert RiskTolerance.LOW is not None

    def test_risk_tolerance_has_moderate(self):
        assert RiskTolerance.MODERATE is not None

    def test_risk_tolerance_has_high(self):
        assert RiskTolerance.HIGH is not None


class TestInvestmentHorizonEnum:
    def test_horizon_has_short_term(self):
        assert InvestmentHorizon.SHORT_TERM is not None

    def test_horizon_has_medium_term(self):
        assert InvestmentHorizon.MEDIUM_TERM is not None

    def test_horizon_has_long_term(self):
        assert InvestmentHorizon.LONG_TERM is not None
