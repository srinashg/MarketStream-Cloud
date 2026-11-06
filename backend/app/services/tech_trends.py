"""Tech trends service: sector signals and stock mapping."""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class TrendCategory(str, Enum):
    AI = "ai"
    ROBOTICS_AND_ACTUATORS = "robotics_and_actuators"
    ELECTRIC_VEHICLES = "electric_vehicles"
    CLOUD_COMPUTING = "cloud_computing"
    ENERGY = "energy"


@dataclass
class TrendSignal:
    category: TrendCategory
    strength: float
    description: str

    def __post_init__(self) -> None:
        if not (0 <= self.strength <= 10):
            raise ValueError("Strength must be between 0 and 10")


@dataclass
class TrendReport:
    signals: List[TrendSignal]

    @property
    def top_signal(self) -> TrendSignal:
        return max(self.signals, key=lambda s: s.strength)


_TREND_DATA: Dict[TrendCategory, TrendSignal] = {
    TrendCategory.AI: TrendSignal(
        category=TrendCategory.AI,
        strength=9.5,
        description="AI infrastructure spend accelerating globally; hyperscalers doubling GPU capacity",
    ),
    TrendCategory.CLOUD_COMPUTING: TrendSignal(
        category=TrendCategory.CLOUD_COMPUTING,
        strength=8.5,
        description="Cloud migration and AI workloads driving hyperscaler revenue growth",
    ),
    TrendCategory.ROBOTICS_AND_ACTUATORS: TrendSignal(
        category=TrendCategory.ROBOTICS_AND_ACTUATORS,
        strength=8.0,
        description="Humanoid robots and high-torque actuator demand entering production scale",
    ),
    TrendCategory.ELECTRIC_VEHICLES: TrendSignal(
        category=TrendCategory.ELECTRIC_VEHICLES,
        strength=7.5,
        description="EV adoption growing steadily as battery costs continue to fall",
    ),
    TrendCategory.ENERGY: TrendSignal(
        category=TrendCategory.ENERGY,
        strength=7.0,
        description="Renewable energy and grid modernisation attracting major capital inflows",
    ),
}

_TREND_TO_STOCKS: Dict[TrendCategory, List[str]] = {
    TrendCategory.AI: ["NVDA", "AMD", "MSFT", "GOOGL"],
    TrendCategory.CLOUD_COMPUTING: ["MSFT", "AMZN", "GOOGL"],
    TrendCategory.ROBOTICS_AND_ACTUATORS: ["TSLA", "ABB", "FANUC"],
    TrendCategory.ELECTRIC_VEHICLES: ["TSLA", "GM", "F", "NIO"],
    TrendCategory.ENERGY: ["NEE", "ENPH", "FSLR"],
}


def analyze_trend(category: TrendCategory) -> TrendSignal:
    return _TREND_DATA[category]


def get_trending_sectors() -> List[TrendSignal]:
    """Return all trend signals sorted by strength descending."""
    return sorted(_TREND_DATA.values(), key=lambda s: s.strength, reverse=True)


def map_trends_to_stocks(signals: List[TrendSignal]) -> List[str]:
    """Map a list of TrendSignals to unique stock tickers."""
    result: List[str] = []
    for signal in signals:
        for ticker in _TREND_TO_STOCKS.get(signal.category, []):
            if ticker not in result:
                result.append(ticker)
    return result
