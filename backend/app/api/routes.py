"""API v1 router — wires all feature endpoints."""
import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    InvestmentProfileRequest,
    InvestmentProfileResponse,
    InvestorPositionResponse,
    InvestorProfileResponse,
    NewsAnalysisResponse,
    SimulationRequest,
    SimulationResponse,
    StockRecommendationResponse,
    TrendSignalResponse,
)
from app.services import investment_profile as ip_svc
from app.services import investor_tracker as inv_svc
from app.services import market_news as news_svc
from app.services import portfolio_simulator as port_svc
from app.services import stock_research as sr_svc
from app.services import tech_trends as tt_svc

router = APIRouter(prefix="/api/v1")


# ── Investment Profile ────────────────────────────────────────────────────────

@router.post("/investment-profile", response_model=InvestmentProfileResponse, status_code=201)
def create_investment_profile(body: InvestmentProfileRequest) -> InvestmentProfileResponse:
    try:
        risk = ip_svc.RiskTolerance(body.risk_tolerance)
        horizon = ip_svc.InvestmentHorizon(body.horizon)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    profile = ip_svc.create_investment_profile(
        budget=body.budget,
        risk_tolerance=risk,
        horizon=horizon,
        short_term_goals=body.short_term_goals,
        long_term_goals=body.long_term_goals,
    )
    return InvestmentProfileResponse(
        id=str(uuid.uuid4()),
        budget=profile.budget,
        risk_tolerance=profile.risk_tolerance.value,
        horizon=profile.horizon.value,
        short_term_goals=profile.short_term_goals,
        long_term_goals=profile.long_term_goals,
    )


# ── Stock Recommendations ─────────────────────────────────────────────────────

@router.get("/recommendations", response_model=List[StockRecommendationResponse])
def get_recommendations(budget: float, risk_tolerance: str) -> List[StockRecommendationResponse]:
    try:
        risk = sr_svc.RiskTolerance(risk_tolerance)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    recs = sr_svc.get_recommendations(budget=budget, risk_tolerance=risk)
    return [
        StockRecommendationResponse(
            symbol=r.symbol, score=r.score, reasoning=r.reasoning, volatility=r.volatility
        )
        for r in recs
    ]


# ── Portfolio Simulation ──────────────────────────────────────────────────────

@router.post("/portfolio/simulate", response_model=SimulationResponse)
def simulate_portfolio(body: SimulationRequest) -> SimulationResponse:
    stocks = [{"symbol": s.symbol, "weight": s.weight} for s in body.stocks]
    try:
        result = port_svc.simulate_portfolio(
            budget=body.budget, stocks=stocks, years=body.years
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return SimulationResponse(projected_value=result.projected_value, scenarios=result.scenarios)


# ── Market News ───────────────────────────────────────────────────────────────

@router.get("/news/{symbol}", response_model=NewsAnalysisResponse)
def get_news(symbol: str) -> NewsAnalysisResponse:
    analysis = news_svc.get_news_for_symbol(symbol)
    return NewsAnalysisResponse(
        symbol=analysis.symbol,
        overall_sentiment=analysis.overall_sentiment.value,
        article_count=analysis.article_count,
    )


# ── Investor Tracker ──────────────────────────────────────────────────────────

@router.get("/investors", response_model=List[InvestorProfileResponse])
def list_investors() -> List[InvestorProfileResponse]:
    return [
        InvestorProfileResponse(
            name=i.name, organization=i.organization, known_strategy=i.known_strategy
        )
        for i in inv_svc.NOTABLE_INVESTORS
    ]


@router.get("/investors/{investor_name}/positions", response_model=List[InvestorPositionResponse])
def get_investor_positions(investor_name: str) -> List[InvestorPositionResponse]:
    try:
        positions = inv_svc.get_investor_positions(investor_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [
        InvestorPositionResponse(
            investor_name=p.investor_name, symbol=p.symbol, action=p.action
        )
        for p in positions
    ]


# ── Tech Trends ───────────────────────────────────────────────────────────────

@router.get("/trends", response_model=List[TrendSignalResponse])
def get_trends() -> List[TrendSignalResponse]:
    signals = tt_svc.get_trending_sectors()
    return [
        TrendSignalResponse(
            category=s.category.value, strength=s.strength, description=s.description
        )
        for s in signals
    ]
