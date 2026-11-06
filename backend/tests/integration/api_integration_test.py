"""
Step 3 - Integration Testing.
Verify FastAPI endpoints, business logic, and API contracts end-to-end.
Tests run against the live FastAPI application via TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ══════════════════════════════════════════════════════════════════════════════
# Health
# ══════════════════════════════════════════════════════════════════════════════

class TestHealthEndpoint:
    def test_health_check_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_ok_status(self):
        response = client.get("/health")
        assert response.json()["status"] == "ok"

    def test_health_check_returns_json(self):
        response = client.get("/health")
        assert response.headers["content-type"].startswith("application/json")


# ══════════════════════════════════════════════════════════════════════════════
# Investment Profile
# ══════════════════════════════════════════════════════════════════════════════

class TestInvestmentProfileEndpoint:
    _VALID_PAYLOAD = {
        "budget": 1500.0,
        "risk_tolerance": "moderate",
        "horizon": "medium_term",
        "short_term_goals": [],
        "long_term_goals": ["retirement"],
    }

    def test_create_profile_returns_201(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        assert response.status_code == 201

    def test_create_profile_returns_profile_id(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        assert "id" in response.json()

    def test_create_profile_id_is_non_empty_string(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        assert isinstance(response.json()["id"], str)
        assert len(response.json()["id"]) > 0

    def test_create_profile_response_echoes_budget(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        assert response.json()["budget"] == 1500.0

    def test_create_profile_response_echoes_risk_tolerance(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        assert response.json()["risk_tolerance"] == "moderate"

    def test_create_profile_response_echoes_horizon(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        assert response.json()["horizon"] == "medium_term"

    def test_create_profile_response_echoes_long_term_goals(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        assert "retirement" in response.json()["long_term_goals"]

    def test_create_profile_response_has_all_required_fields(self):
        response = client.post("/api/v1/investment-profile", json=self._VALID_PAYLOAD)
        data = response.json()
        for field in ("id", "budget", "risk_tolerance", "horizon", "short_term_goals", "long_term_goals"):
            assert field in data, f"Missing field: {field}"

    def test_create_profile_with_short_term_goals(self):
        payload = {**self._VALID_PAYLOAD, "short_term_goals": ["emergency_fund", "car_payment"]}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 201
        assert "emergency_fund" in response.json()["short_term_goals"]

    def test_create_profile_low_risk_short_term(self):
        payload = {
            "budget": 500.0,
            "risk_tolerance": "low",
            "horizon": "short_term",
            "short_term_goals": ["wedding"],
            "long_term_goals": [],
        }
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 201
        assert response.json()["risk_tolerance"] == "low"

    def test_create_profile_high_risk_long_term(self):
        payload = {
            "budget": 50000.0,
            "risk_tolerance": "high",
            "horizon": "long_term",
            "short_term_goals": [],
            "long_term_goals": ["generational_wealth"],
        }
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 201

    # ── Validation errors ────────────────────────────────────────────────────

    def test_missing_budget_returns_422(self):
        payload = {"risk_tolerance": "moderate", "horizon": "medium_term"}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 422

    def test_negative_budget_returns_422(self):
        payload = {**self._VALID_PAYLOAD, "budget": -100.0}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 422

    def test_zero_budget_returns_422(self):
        payload = {**self._VALID_PAYLOAD, "budget": 0.0}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 422

    def test_missing_risk_tolerance_returns_422(self):
        payload = {"budget": 1500.0, "horizon": "medium_term"}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 422

    def test_missing_horizon_returns_422(self):
        payload = {"budget": 1500.0, "risk_tolerance": "moderate"}
        response = client.post("/api/v1/investment-profile", json=payload)
        assert response.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# Stock Recommendations
# ══════════════════════════════════════════════════════════════════════════════

class TestStockRecommendationsEndpoint:
    def test_get_recommendations_returns_200(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        assert response.status_code == 200

    def test_get_recommendations_returns_list(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        assert isinstance(response.json(), list)

    def test_get_recommendations_list_is_not_empty(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        assert len(response.json()) > 0

    def test_recommendation_items_have_required_fields(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        for item in response.json():
            assert "symbol" in item
            assert "score" in item
            assert "reasoning" in item
            assert "volatility" in item

    def test_recommendations_scores_are_valid_range(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        for item in response.json():
            assert 0 <= item["score"] <= 10

    def test_recommendations_sorted_by_score_descending(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        scores = [item["score"] for item in response.json()]
        assert scores == sorted(scores, reverse=True)

    def test_low_risk_excludes_high_volatility_stocks(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=low")
        for item in response.json():
            assert item["volatility"] != "high"

    def test_high_risk_includes_all_volatility_levels(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=high")
        volatilities = {item["volatility"] for item in response.json()}
        assert "high" in volatilities
        assert "low" in volatilities

    def test_moderate_risk_excludes_high_volatility(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=moderate")
        for item in response.json():
            assert item["volatility"] in ("low", "moderate")

    def test_missing_budget_returns_422(self):
        response = client.get("/api/v1/recommendations?risk_tolerance=moderate")
        assert response.status_code == 422

    def test_missing_risk_tolerance_returns_422(self):
        response = client.get("/api/v1/recommendations?budget=1500")
        assert response.status_code == 422

    def test_reasoning_is_non_empty_string(self):
        response = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=high")
        for item in response.json():
            assert isinstance(item["reasoning"], str)
            assert len(item["reasoning"]) > 0


# ══════════════════════════════════════════════════════════════════════════════
# Portfolio Simulation
# ══════════════════════════════════════════════════════════════════════════════

class TestPortfolioSimulationEndpoint:
    _VALID_PAYLOAD = {
        "budget": 1500.0,
        "stocks": [{"symbol": "AAPL", "weight": 0.6}, {"symbol": "NVDA", "weight": 0.4}],
        "years": 5,
    }

    def test_simulate_returns_200(self):
        response = client.post("/api/v1/portfolio/simulate", json=self._VALID_PAYLOAD)
        assert response.status_code == 200

    def test_simulate_returns_projected_value(self):
        response = client.post("/api/v1/portfolio/simulate", json=self._VALID_PAYLOAD)
        assert "projected_value" in response.json()

    def test_simulate_projected_value_is_positive(self):
        response = client.post("/api/v1/portfolio/simulate", json=self._VALID_PAYLOAD)
        assert response.json()["projected_value"] > 0

    def test_simulate_response_has_scenarios(self):
        response = client.post("/api/v1/portfolio/simulate", json=self._VALID_PAYLOAD)
        scenarios = response.json()["scenarios"]
        assert "optimistic" in scenarios
        assert "base" in scenarios
        assert "pessimistic" in scenarios

    def test_optimistic_greater_than_base(self):
        response = client.post("/api/v1/portfolio/simulate", json=self._VALID_PAYLOAD)
        scenarios = response.json()["scenarios"]
        assert scenarios["optimistic"] > scenarios["base"]

    def test_base_greater_than_pessimistic(self):
        response = client.post("/api/v1/portfolio/simulate", json=self._VALID_PAYLOAD)
        scenarios = response.json()["scenarios"]
        assert scenarios["base"] > scenarios["pessimistic"]

    def test_longer_horizon_yields_higher_optimistic(self):
        payload_1yr = {**self._VALID_PAYLOAD, "years": 1}
        payload_10yr = {**self._VALID_PAYLOAD, "years": 10}
        result_1yr = client.post("/api/v1/portfolio/simulate", json=payload_1yr).json()
        result_10yr = client.post("/api/v1/portfolio/simulate", json=payload_10yr).json()
        assert result_10yr["scenarios"]["optimistic"] > result_1yr["scenarios"]["optimistic"]

    def test_larger_budget_yields_proportionally_larger_projected_value(self):
        payload_low = {**self._VALID_PAYLOAD, "budget": 1000.0}
        payload_high = {**self._VALID_PAYLOAD, "budget": 2000.0}
        result_low = client.post("/api/v1/portfolio/simulate", json=payload_low).json()
        result_high = client.post("/api/v1/portfolio/simulate", json=payload_high).json()
        assert result_high["projected_value"] == pytest.approx(result_low["projected_value"] * 2, rel=1e-6)

    def test_single_stock_full_weight_accepted(self):
        payload = {"budget": 1000.0, "stocks": [{"symbol": "AAPL", "weight": 1.0}], "years": 1}
        response = client.post("/api/v1/portfolio/simulate", json=payload)
        assert response.status_code == 200

    def test_weights_not_summing_to_one_returns_422(self):
        payload = {
            "budget": 1500.0,
            "stocks": [{"symbol": "AAPL", "weight": 0.6}, {"symbol": "NVDA", "weight": 0.6}],
            "years": 5,
        }
        response = client.post("/api/v1/portfolio/simulate", json=payload)
        assert response.status_code == 422

    def test_missing_budget_returns_422(self):
        payload = {"stocks": [{"symbol": "AAPL", "weight": 1.0}], "years": 1}
        response = client.post("/api/v1/portfolio/simulate", json=payload)
        assert response.status_code == 422

    def test_missing_years_returns_422(self):
        payload = {"budget": 1000.0, "stocks": [{"symbol": "AAPL", "weight": 1.0}]}
        response = client.post("/api/v1/portfolio/simulate", json=payload)
        assert response.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# Market News
# ══════════════════════════════════════════════════════════════════════════════

class TestMarketNewsEndpoint:
    def test_get_news_for_aapl_returns_200(self):
        response = client.get("/api/v1/news/AAPL")
        assert response.status_code == 200

    def test_get_news_for_nvda_returns_200(self):
        response = client.get("/api/v1/news/NVDA")
        assert response.status_code == 200

    def test_get_news_for_unknown_symbol_returns_200(self):
        # Stub data falls back to default article set — always 200.
        response = client.get("/api/v1/news/XYZ")
        assert response.status_code == 200

    def test_news_response_has_overall_sentiment(self):
        response = client.get("/api/v1/news/NVDA")
        assert "overall_sentiment" in response.json()

    def test_news_response_has_article_count(self):
        response = client.get("/api/v1/news/NVDA")
        assert "article_count" in response.json()

    def test_news_response_has_symbol(self):
        response = client.get("/api/v1/news/AAPL")
        assert response.json()["symbol"] == "AAPL"

    def test_news_sentiment_is_valid_value(self):
        response = client.get("/api/v1/news/NVDA")
        assert response.json()["overall_sentiment"] in ("positive", "negative", "neutral")

    def test_news_article_count_is_non_negative_integer(self):
        response = client.get("/api/v1/news/AAPL")
        count = response.json()["article_count"]
        assert isinstance(count, int)
        assert count >= 0

    def test_nvda_news_has_at_least_one_article(self):
        response = client.get("/api/v1/news/NVDA")
        assert response.json()["article_count"] >= 1

    def test_known_symbols_return_positive_sentiment(self):
        """AAPL and NVDA stub articles are bullish — expect positive sentiment."""
        for symbol in ("AAPL", "NVDA"):
            response = client.get(f"/api/v1/news/{symbol}")
            assert response.json()["overall_sentiment"] == "positive", (
                f"Expected positive sentiment for {symbol}"
            )

    def test_symbol_is_uppercased_in_response(self):
        response = client.get("/api/v1/news/aapl")
        assert response.json()["symbol"] == "AAPL"


# ══════════════════════════════════════════════════════════════════════════════
# Investor Tracker
# ══════════════════════════════════════════════════════════════════════════════

class TestInvestorTrackerEndpoint:
    def test_list_investors_returns_200(self):
        response = client.get("/api/v1/investors")
        assert response.status_code == 200

    def test_list_investors_returns_list(self):
        response = client.get("/api/v1/investors")
        assert isinstance(response.json(), list)

    def test_list_investors_is_not_empty(self):
        response = client.get("/api/v1/investors")
        assert len(response.json()) >= 3

    def test_investor_items_have_required_fields(self):
        response = client.get("/api/v1/investors")
        for investor in response.json():
            assert "name" in investor
            assert "organization" in investor
            assert "known_strategy" in investor

    def test_warren_buffett_is_in_investor_list(self):
        response = client.get("/api/v1/investors")
        names = [i["name"] for i in response.json()]
        assert "Warren Buffett" in names

    def test_elon_musk_is_in_investor_list(self):
        response = client.get("/api/v1/investors")
        names = [i["name"] for i in response.json()]
        assert "Elon Musk" in names

    def test_jensen_huang_is_in_investor_list(self):
        response = client.get("/api/v1/investors")
        names = [i["name"] for i in response.json()]
        assert "Jensen Huang" in names

    def test_get_warren_buffett_positions_returns_200(self):
        response = client.get("/api/v1/investors/Warren Buffett/positions")
        assert response.status_code == 200

    def test_get_elon_musk_positions_returns_200(self):
        response = client.get("/api/v1/investors/Elon Musk/positions")
        assert response.status_code == 200

    def test_positions_have_required_fields(self):
        response = client.get("/api/v1/investors/Warren Buffett/positions")
        for pos in response.json():
            assert "investor_name" in pos
            assert "symbol" in pos
            assert "action" in pos

    def test_positions_all_belong_to_requested_investor(self):
        response = client.get("/api/v1/investors/Warren Buffett/positions")
        for pos in response.json():
            assert pos["investor_name"] == "Warren Buffett"

    def test_position_actions_are_valid(self):
        response = client.get("/api/v1/investors/Warren Buffett/positions")
        for pos in response.json():
            assert pos["action"] in ("buy", "sell", "hold")

    def test_buffett_holds_aapl(self):
        response = client.get("/api/v1/investors/Warren Buffett/positions")
        symbols = [p["symbol"] for p in response.json()]
        assert "AAPL" in symbols

    def test_unknown_investor_returns_404(self):
        response = client.get("/api/v1/investors/Unknown Person XYZ/positions")
        assert response.status_code == 404

    def test_jensen_huang_holds_nvda(self):
        response = client.get("/api/v1/investors/Jensen Huang/positions")
        symbols = [p["symbol"] for p in response.json()]
        assert "NVDA" in symbols


# ══════════════════════════════════════════════════════════════════════════════
# Tech Trends
# ══════════════════════════════════════════════════════════════════════════════

class TestTechTrendsEndpoint:
    def test_get_trends_returns_200(self):
        response = client.get("/api/v1/trends")
        assert response.status_code == 200

    def test_get_trends_returns_list(self):
        response = client.get("/api/v1/trends")
        assert isinstance(response.json(), list)

    def test_get_trends_list_is_not_empty(self):
        response = client.get("/api/v1/trends")
        assert len(response.json()) > 0

    def test_trend_items_have_required_fields(self):
        response = client.get("/api/v1/trends")
        for trend in response.json():
            assert "category" in trend
            assert "strength" in trend
            assert "description" in trend

    def test_trend_strengths_are_valid_range(self):
        response = client.get("/api/v1/trends")
        for trend in response.json():
            assert 0 <= trend["strength"] <= 10

    def test_trends_sorted_by_strength_descending(self):
        response = client.get("/api/v1/trends")
        strengths = [t["strength"] for t in response.json()]
        assert strengths == sorted(strengths, reverse=True)

    def test_ai_category_is_present(self):
        response = client.get("/api/v1/trends")
        categories = [t["category"] for t in response.json()]
        assert "ai" in categories

    def test_robotics_and_actuators_category_is_present(self):
        response = client.get("/api/v1/trends")
        categories = [t["category"] for t in response.json()]
        assert "robotics_and_actuators" in categories

    def test_all_five_categories_are_present(self):
        response = client.get("/api/v1/trends")
        categories = {t["category"] for t in response.json()}
        expected = {"ai", "robotics_and_actuators", "electric_vehicles", "cloud_computing", "energy"}
        assert expected == categories

    def test_ai_has_highest_strength(self):
        response = client.get("/api/v1/trends")
        trends = response.json()
        assert trends[0]["category"] == "ai"

    def test_descriptions_are_non_empty(self):
        response = client.get("/api/v1/trends")
        for trend in response.json():
            assert isinstance(trend["description"], str)
            assert len(trend["description"]) > 0


# ══════════════════════════════════════════════════════════════════════════════
# End-to-End Scenario: Create Profile → Recommend → Simulate
# ══════════════════════════════════════════════════════════════════════════════

class TestEndToEndInvestmentScenario:
    """
    Chained scenario that mirrors a real user journey:
    1. Create an investment profile
    2. Fetch stock recommendations matching that profile
    3. Simulate a portfolio built from those recommendations
    """

    def test_full_moderate_investor_flow(self):
        # Step 1 — create profile
        profile_resp = client.post(
            "/api/v1/investment-profile",
            json={
                "budget": 1500.0,
                "risk_tolerance": "moderate",
                "horizon": "medium_term",
                "short_term_goals": [],
                "long_term_goals": ["retirement"],
            },
        )
        assert profile_resp.status_code == 201
        profile = profile_resp.json()

        # Step 2 — get recommendations for this profile
        recs_resp = client.get(
            f"/api/v1/recommendations?budget={profile['budget']}&risk_tolerance={profile['risk_tolerance']}"
        )
        assert recs_resp.status_code == 200
        recs = recs_resp.json()
        assert len(recs) > 0

        # Recommendations must not contain high-volatility stocks (moderate filter)
        for rec in recs:
            assert rec["volatility"] in ("low", "moderate")

        # Step 3 — simulate a portfolio from the top two recommendations
        top_two = recs[:2]
        total_weight = sum(r["score"] for r in top_two)
        stocks = [
            {"symbol": r["symbol"], "weight": round(r["score"] / total_weight, 10)}
            for r in top_two
        ]
        # Normalise to exactly 1.0
        stocks[-1]["weight"] = round(1.0 - sum(s["weight"] for s in stocks[:-1]), 10)

        sim_resp = client.post(
            "/api/v1/portfolio/simulate",
            json={"budget": profile["budget"], "stocks": stocks, "years": 5},
        )
        assert sim_resp.status_code == 200
        sim = sim_resp.json()
        assert sim["projected_value"] > profile["budget"]  # expect growth

    def test_full_conservative_investor_flow(self):
        profile_resp = client.post(
            "/api/v1/investment-profile",
            json={
                "budget": 500.0,
                "risk_tolerance": "low",
                "horizon": "short_term",
                "short_term_goals": ["emergency_fund"],
                "long_term_goals": [],
            },
        )
        assert profile_resp.status_code == 201

        recs_resp = client.get("/api/v1/recommendations?budget=500&risk_tolerance=low")
        assert recs_resp.status_code == 200
        recs = recs_resp.json()

        # Low-risk investor should only see low-volatility picks
        for rec in recs:
            assert rec["volatility"] == "low"

    def test_news_and_trends_enrich_recommendations(self):
        """Verify that news and trend endpoints return consistent data for recommended symbols."""
        recs_resp = client.get("/api/v1/recommendations?budget=1500&risk_tolerance=high")
        assert recs_resp.status_code == 200
        recs = recs_resp.json()

        # Fetch news for each recommended symbol that has stub data
        for rec in recs[:3]:
            news_resp = client.get(f"/api/v1/news/{rec['symbol']}")
            assert news_resp.status_code == 200
            assert "overall_sentiment" in news_resp.json()

        # Trends should include AI, which drives many high-score recommendations
        trends_resp = client.get("/api/v1/trends")
        assert trends_resp.status_code == 200
        categories = [t["category"] for t in trends_resp.json()]
        assert "ai" in categories

