# MarketStream Cloud — Database Schema

> **Engine:** Google Cloud Firestore (NoSQL document store)  
> Schema derived from `backend/app/models/schemas.py` and the six service layers.

---

## Entity Relationship Overview

```
investment_profiles ──< portfolio_simulations
investment_profiles ──< stock_recommendations
                        news_analyses          (keyed by symbol)
investor_profiles   ──< investor_positions
                        trend_signals          (keyed by category)
```

---

## Collections

### 1. `investment_profiles`

Stores a user's budget, risk preferences, investment horizon, and goals.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | `string` | PK, UUID v4 | Auto-generated |
| `budget` | `number` | > 0 | Investment amount in USD |
| `risk_tolerance` | `string` | `low` \| `moderate` \| `high` | Maps to `RiskTolerance` enum |
| `horizon` | `string` | `short_term` \| `medium_term` \| `long_term` | Maps to `InvestmentHorizon` enum |
| `short_term_goals` | `string[]` | — | e.g. `["emergency_fund", "car_payment"]` |
| `long_term_goals` | `string[]` | — | e.g. `["retirement", "home_buying"]` |
| `created_at` | `timestamp` | — | Server-side UTC timestamp |

**Example document**
```json
{
  "id": "a1b2c3d4-...",
  "budget": 1500.00,
  "risk_tolerance": "moderate",
  "horizon": "medium_term",
  "short_term_goals": [],
  "long_term_goals": ["retirement"],
  "created_at": "2026-11-06T22:00:00Z"
}
```

---

### 2. `portfolio_simulations`

Stores the inputs and results of each portfolio simulation run.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | `string` | PK, UUID v4 | Auto-generated |
| `profile_id` | `string` | FK → `investment_profiles.id` | Optional; null for guest runs |
| `budget` | `number` | > 0 | Simulation budget in USD |
| `stocks` | `object[]` | weights sum to 1.0 | Array of `{symbol: string, weight: number}` |
| `years` | `integer` | > 0 | Investment horizon in years |
| `projected_value` | `number` | — | Base-scenario projected value |
| `scenarios` | `object` | keys: `optimistic`, `base`, `pessimistic` | Each value is a projected USD amount |
| `simulated_at` | `timestamp` | — | Server-side UTC timestamp |

**`stocks` sub-document**
```json
{ "symbol": "NVDA", "weight": 0.4 }
```

**Example document**
```json
{
  "id": "b2c3d4e5-...",
  "profile_id": "a1b2c3d4-...",
  "budget": 1500.00,
  "stocks": [
    { "symbol": "AAPL", "weight": 0.6 },
    { "symbol": "NVDA", "weight": 0.4 }
  ],
  "years": 5,
  "projected_value": 2415.77,
  "scenarios": {
    "optimistic": 3732.35,
    "base": 2415.77,
    "pessimistic": 1172.09
  },
  "simulated_at": "2026-11-06T22:05:00Z"
}
```

---

### 3. `stock_recommendations`

Stores recommendation snapshots generated for a given budget and risk profile.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | `string` | PK, UUID v4 | Auto-generated |
| `profile_id` | `string` | FK → `investment_profiles.id` | Optional |
| `budget` | `number` | > 0 | — |
| `risk_tolerance` | `string` | `low` \| `moderate` \| `high` | — |
| `recommendations` | `object[]` | — | Ordered by `score` desc |
| `generated_at` | `timestamp` | — | Server-side UTC timestamp |

**`recommendations` sub-document**
```json
{
  "symbol": "NVDA",
  "score": 9.5,
  "reasoning": "Dominant AI chip supplier; data-centre demand growing 3× YoY",
  "volatility": "high"
}
```

---

### 4. `news_analyses`

Stores sentiment analysis snapshots per stock symbol.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | `string` | PK, UUID v4 | — |
| `symbol` | `string` | Uppercase ticker | e.g. `"NVDA"` |
| `overall_sentiment` | `string` | `positive` \| `negative` \| `neutral` | Aggregated |
| `article_count` | `integer` | ≥ 0 | — |
| `articles` | `object[]` | — | Individual article documents |
| `analysed_at` | `timestamp` | — | Server-side UTC timestamp |

**`articles` sub-document**
```json
{
  "title": "NVIDIA Revenue Soars on AI Demand",
  "source": "Bloomberg",
  "url": "https://bloomberg.com/nvda/1",
  "sentiment": "positive"
}
```

---

### 5. `investor_profiles`

Master record for each tracked notable investor.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | `string` | PK, UUID v4 | — |
| `name` | `string` | Unique | Full name, used as lookup key |
| `organization` | `string` | — | Primary firm |
| `known_strategy` | `string` | — | Plain-language strategy summary |

---

### 6. `investor_positions`

Tracks the latest known holdings per notable investor.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | `string` | PK, UUID v4 | — |
| `investor_name` | `string` | FK → `investor_profiles.name` | — |
| `symbol` | `string` | Uppercase ticker | — |
| `action` | `string` | `buy` \| `sell` \| `hold` | Most recent position action |
| `recorded_at` | `timestamp` | — | When the position was recorded |

---

### 7. `trend_signals`

Snapshots of sector trend analysis (refreshed periodically).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | `string` | PK, UUID v4 | — |
| `category` | `string` | Enum — see below | Trend category key |
| `strength` | `number` | 0.0 – 10.0 | Signal strength score |
| `description` | `string` | — | Human-readable rationale |
| `mapped_stocks` | `string[]` | — | Tickers associated with this trend |
| `analysed_at` | `timestamp` | — | Server-side UTC timestamp |

**`category` allowed values**

| Value | Label |
|-------|-------|
| `ai` | Artificial Intelligence |
| `robotics_and_actuators` | Robotics & Actuators |
| `electric_vehicles` | Electric Vehicles |
| `cloud_computing` | Cloud Computing |
| `energy` | Renewable Energy |

---

## Indexes

| Collection | Field(s) | Type | Purpose |
|------------|----------|------|---------|
| `investment_profiles` | `created_at` | Ascending | Pagination |
| `portfolio_simulations` | `profile_id`, `simulated_at` | Composite | Per-profile history |
| `stock_recommendations` | `risk_tolerance`, `generated_at` | Composite | Filtered lookup |
| `news_analyses` | `symbol`, `analysed_at` | Composite | Latest news per symbol |
| `investor_positions` | `investor_name`, `symbol` | Composite | Dedup + lookup |
| `trend_signals` | `category`, `analysed_at` | Composite | Latest signal per category |

---

## Data Flow

```
User Input
    │
    ▼
POST /api/v1/investment-profile
    │  writes → investment_profiles
    │
    ├──► GET /api/v1/recommendations?budget=&risk_tolerance=
    │         reads  → stock_recommendations (cache / on-demand)
    │
    ├──► POST /api/v1/portfolio/simulate
    │         writes → portfolio_simulations
    │
    ├──► GET /api/v1/news/{symbol}
    │         reads  → news_analyses (cache / on-demand)
    │
    ├──► GET /api/v1/investors
    │         reads  → investor_profiles
    │
    ├──► GET /api/v1/investors/{name}/positions
    │         reads  → investor_positions
    │
    └──► GET /api/v1/trends
              reads  → trend_signals
```
