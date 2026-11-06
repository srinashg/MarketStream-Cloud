"""Investor tracker: notable investor profiles, positions, and top picks."""
from dataclasses import dataclass
from typing import List

_VALID_ACTIONS = ("buy", "sell", "hold")


@dataclass
class InvestorProfile:
    name: str
    organization: str
    known_strategy: str


@dataclass
class InvestorPosition:
    investor_name: str
    symbol: str
    action: str

    def __post_init__(self) -> None:
        if self.action not in _VALID_ACTIONS:
            raise ValueError("Action must be buy, sell, or hold")


NOTABLE_INVESTORS: List[InvestorProfile] = [
    InvestorProfile(
        name="Warren Buffett",
        organization="Berkshire Hathaway",
        known_strategy="Value investing — buy undervalued businesses with durable competitive moats",
    ),
    InvestorProfile(
        name="Elon Musk",
        organization="Tesla / SpaceX / xAI",
        known_strategy="Disruptive technology — bet on transformative industries",
    ),
    InvestorProfile(
        name="Jensen Huang",
        organization="NVIDIA",
        known_strategy="AI and semiconductor leadership — own the compute stack",
    ),
    InvestorProfile(
        name="Donald Trump",
        organization="Trump Media & Technology",
        known_strategy="Media and financial services focused on domestic markets",
    ),
]

_INVESTOR_POSITIONS: dict[str, List[InvestorPosition]] = {
    "Warren Buffett": [
        InvestorPosition(investor_name="Warren Buffett", symbol="AAPL", action="hold"),
        InvestorPosition(investor_name="Warren Buffett", symbol="BAC", action="hold"),
        InvestorPosition(investor_name="Warren Buffett", symbol="KO", action="hold"),
        InvestorPosition(investor_name="Warren Buffett", symbol="CVX", action="hold"),
        InvestorPosition(investor_name="Warren Buffett", symbol="OXY", action="buy"),
    ],
    "Elon Musk": [
        InvestorPosition(investor_name="Elon Musk", symbol="TSLA", action="hold"),
        InvestorPosition(investor_name="Elon Musk", symbol="SPCE", action="buy"),
    ],
    "Jensen Huang": [
        InvestorPosition(investor_name="Jensen Huang", symbol="NVDA", action="hold"),
    ],
    "Donald Trump": [
        InvestorPosition(investor_name="Donald Trump", symbol="DJT", action="hold"),
    ],
}


def get_investor_positions(investor_name: str) -> List[InvestorPosition]:
    if investor_name not in _INVESTOR_POSITIONS:
        raise ValueError("Investor not found")
    return _INVESTOR_POSITIONS[investor_name]


def get_top_investor_picks(top_n: int = 5) -> List[str]:
    """Return unique symbols held across all notable investors, capped at top_n."""
    seen: List[str] = []
    for positions in _INVESTOR_POSITIONS.values():
        for pos in positions:
            if pos.symbol not in seen:
                seen.append(pos.symbol)
    return seen[:top_n]
