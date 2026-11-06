"""
TDD - Integration tests for FastAPI endpoints.
Tests written FIRST (RED phase) before implementation.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_ok_status(self):
        response = client.get("/health")
        assert response.json()["status"] == "ok"


class TestInvestmentProfileEndpoint:
    def test_create_profile_returns_201(self):
        payload = {
            "budget": 1500.0,
            "risk_tolerance": "moderate",
            "horizon": "medium_term",
            "short_term_goals": [],
            "long_term_goals": ["retirement"],
        }
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 201

    def test_create_profile_returns_profile_id(self):
        payload = {
            "budget": 1500.0,
            "risk_tolerance": "moderate",
            "horizon": "medium_term",
        }
        response = client.post("/api/v1/investment-profile", json=payload)
        assert "id" in response.json()

    def test_create_profile_missing_budget_returns_422(self):
        payload = {"risk_tolerance": "moderate", "horizon": "medium_term"}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 422

    def test_create_profile_negative_budget_returns_422(self):
        payload = {"budget": -100.0, "risk_tolerance": "moderate", "horizon": "medium_term"}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 422


class TestStockRecommendationsEndpoint:
    def test_get_recommendations_returns_200(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        assert response.status_code == 200

    def test_get_recommendations_returns_list(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        data = response.json()
        assert isinstance(data, list)

    def test_get_recommendations_missing_budget_returns_422(self):
        response = client.get("/api/v1/recommendations?risk_tolerance=moderate")
        assert response.status_code == 422


class TestPortfolioSimulationEndpoint:
    def test_simulate_returns_200(self):
        payload = {
            "budget": 1500.0,
            "stocks": [{"symbol": "AAPL", "weight": 0.6}, {"symbol": "NVDA", "weight": 0.4}],
            "years": 5,
        }
        response = client.post("/api/v1/portfolio/simulate", json=payload)
        assert response.status_code == 200

    def test_simulate_returns_projected_value(self):
        payload = {
            "budget": 1500.0,
            "stocks": [{"symbol": "AAPL", "weight": 1.0}],
            "years": 1,
        }
        response = client.post("/api/v1/portfolio/simulate", json=payload)
        assert "projected_value" in response.json()

    def test_simulate_invalid_weights_returns_422(self):
        payload = {
            "budget": 1500.0,
            "stocks": [{"symbol": "AAPL", "weight": 0.6}, {"symbol": "NVDA", "weight": 0.6}],
            "years": 5,
        }
        response = client.post("/api/v1/portfolio/simulate", json=payload)
        assert response.status_code == 422


class TestMarketNewsEndpoint:
    def test_get_news_for_symbol_returns_200(self):
        response = client.get("/api/v1/news/AAPL")
        assert response.status_code == 200

    def test_get_news_returns_analysis(self):
        response = client.get("/api/v1/news/NVDA")
        data = response.json()
        assert "overall_sentiment" in data
        assert "article_count" in data


class TestInvestorTrackerEndpoint:
    def test_get_notable_investors_returns_200(self):
        response = client.get("/api/v1/investors")
        assert response.status_code == 200

    def test_get_notable_investors_returns_list(self):
        response = client.get("/api/v1/investors")
        assert isinstance(response.json(), list)

    def test_get_investor_positions_returns_200(self):
        response = client.get("/api/v1/investors/Warren Buffett/positions")
        assert response.status_code == 200


class TestTechTrendsEndpoint:
    def test_get_trending_sectors_returns_200(self):
        response = client.get("/api/v1/trends")
        assert response.status_code == 200

    def test_get_trending_sectors_returns_list(self):
        response = client.get("/api/v1/trends")
        assert isinstance(response.json(), list)
