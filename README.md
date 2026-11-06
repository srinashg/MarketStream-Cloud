# MarketStream Cloud

A cloud-based market intelligence platform that helps users decide which stocks to buy/sell.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / FastAPI |
| Frontend | Angular + Chart.js |
| Database | NoSQL (future milestone) |
| Deployment | Google Cloud Run |
| Testing | pytest, FastAPI TestClient, Angular runner, Playwright |

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Development Process

This project follows strict TDD:
1. **RED** – Write a failing test
2. **GREEN** – Write the minimum code to pass
3. **REFACTOR** – Clean up without breaking tests

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for milestone details.