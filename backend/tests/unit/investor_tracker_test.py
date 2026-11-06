"""
TDD - Unit tests for InvestorTracker feature.
Tests written FIRST (RED phase) before implementation.

Tracks notable investor positions (Warren Buffett, Elon Musk, Jensen Huang, etc.)
to surface insight-driven stock recommendations.
"""
import pytest
from app.services.investor_tracker import (
    InvestorProfile,
    InvestorPosition,
    get_investor_positions,
    get_top_investor_picks,
    NOTABLE_INVESTORS,
)


class TestInvestorProfile:
    def test_investor_profile_has_name(self):
        investor = InvestorProfile(
            name="Warren Buffett",
            organization="Berkshire Hathaway",
            known_strategy="Value investing",
        )
        assert investor.name == "Warren Buffett"

    def test_investor_profile_has_organization(self):
        investor = InvestorProfile(
            name="Warren Buffett",
            organization="Berkshire Hathaway",
            known_strategy="Value investing",
        )
        assert investor.organization == "Berkshire Hathaway"

    def test_investor_profile_has_known_strategy(self):
        investor = InvestorProfile(
            name="Elon Musk",
            organization="Tesla / SpaceX",
            known_strategy="Disruptive technology",
        )
        assert investor.known_strategy == "Disruptive technology"


class TestNotableInvestors:
    def test_notable_investors_contains_warren_buffett(self):
        names = [i.name for i in NOTABLE_INVESTORS]
        assert "Warren Buffett" in names

    def test_notable_investors_contains_elon_musk(self):
        names = [i.name for i in NOTABLE_INVESTORS]
        assert "Elon Musk" in names

    def test_notable_investors_contains_jensen_huang(self):
        names = [i.name for i in NOTABLE_INVESTORS]
        assert "Jensen Huang" in names

    def test_notable_investors_list_is_not_empty(self):
        assert len(NOTABLE_INVESTORS) >= 3


class TestInvestorPosition:
    def test_position_has_symbol(self):
        pos = InvestorPosition(investor_name="Warren Buffett", symbol="AAPL", action="buy")
        assert pos.symbol == "AAPL"

    def test_position_has_action(self):
        pos = InvestorPosition(investor_name="Warren Buffett", symbol="AAPL", action="buy")
        assert pos.action in ("buy", "sell", "hold")

    def test_invalid_action_raises_value_error(self):
        with pytest.raises(ValueError, match="Action must be buy, sell, or hold"):
            InvestorPosition(investor_name="Warren Buffett", symbol="AAPL", action="unknown")


class TestGetInvestorPositions:
    def test_returns_list_of_investor_positions(self):
        positions = get_investor_positions("Warren Buffett")
        assert isinstance(positions, list)

    def test_all_positions_belong_to_requested_investor(self):
        positions = get_investor_positions("Warren Buffett")
        for pos in positions:
            assert pos.investor_name == "Warren Buffett"

    def test_unknown_investor_raises_value_error(self):
        with pytest.raises(ValueError, match="Investor not found"):
            get_investor_positions("Unknown Person XYZ")


class TestGetTopInvestorPicks:
    def test_returns_list_of_symbols(self):
        picks = get_top_investor_picks(top_n=5)
        assert isinstance(picks, list)

    def test_picks_count_does_not_exceed_top_n(self):
        picks = get_top_investor_picks(top_n=3)
        assert len(picks) <= 3

    def test_picks_are_unique_symbols(self):
        picks = get_top_investor_picks(top_n=10)
        assert len(picks) == len(set(picks))
