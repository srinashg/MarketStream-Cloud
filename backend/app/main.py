"""MarketStream Cloud FastAPI application entry point."""
from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="MarketStream Cloud",
    description="Cloud-based market intelligence platform",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
