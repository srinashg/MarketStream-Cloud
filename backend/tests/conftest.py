"""Pytest configuration and shared fixtures for MarketStream Cloud tests."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Provide a shared FastAPI TestClient for the session."""
    return TestClient(app)


@pytest.fixture
def sample_budget() -> float:
    return 1500.0


@pytest.fixture
def sample_investment_payload() -> dict:
    return {
        "budget": 1500.0,
        "risk_tolerance": "moderate",
        "horizon": "medium_term",
        "short_term_goals": [],
        "long_term_goals": ["retirement"],
    }


@pytest.fixture
def sample_stocks() -> list:
    return [
        {"symbol": "AAPL", "weight": 0.4},
        {"symbol": "NVDA", "weight": 0.4},
        {"symbol": "MSFT", "weight": 0.2},
    ]
