"""MarketStream Cloud FastAPI application entry point."""
from fastapi import FastAPI

app = FastAPI(
    title="MarketStream Cloud",
    description="Cloud-based market intelligence platform",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
