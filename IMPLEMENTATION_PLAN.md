# MarketStream Cloud – Implementation Plan

## Milestone 1: Backend (TDD)

### Step 1 – Tests First ✅
Write all pytest tests before any implementation (RED phase).

**Unit tests** (`backend/tests/unit/`):
- `investment_profile_test.py` – budget, risk tolerance, investment horizon, goals
- `portfolio_simulator_test.py` – portfolio allocation, projected returns, scenario modelling
- `stock_research_test.py` – recommendations, ranking, risk filtering
- `market_news_test.py` – article parsing, sentiment analysis, stock mention extraction
- `investor_tracker_test.py` – notable investor positions (Buffett, Musk, Jensen Huang)
- `tech_trends_test.py` – sector trends (AI, robotics/actuators, EV, cloud, energy)

**Integration tests** (`backend/tests/integration/`):
- `api_integration_test.py` – all FastAPI endpoint contracts

### Step 2 – Backend Development (next)
Implement services using RED → GREEN → REFACTOR:

| Service | Module |
|---------|--------|
| Investment profile | `app/services/investment_profile.py` |
| Portfolio simulator | `app/services/portfolio_simulator.py` |
| Stock research | `app/services/stock_research.py` |
| Market news | `app/services/market_news.py` |
| Investor tracker | `app/services/investor_tracker.py` |
| Tech trends | `app/services/tech_trends.py` |

API routes wired in `app/api/` and exposed via `app/main.py`.

### Step 3 – Integration Testing
Verify endpoint contracts and wire external financial APIs.

### Step 4 – Frontend Development
Angular + Chart.js UI with Playwright end-to-end tests.

### Step 5 – Google Cloud Deployment
Deploy to Cloud Run, configure CI/CD, run smoke tests.
