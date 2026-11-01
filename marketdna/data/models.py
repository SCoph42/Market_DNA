from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

@dataclass
class Instrument:
    symbol: str
    exchange: str
    market_type: str  # e.g., 'futures', 'crypto'
    tick_size: Optional[float] = None
    contract_multiplier: Optional[float] = None

@dataclass
class OHLCVBar:
    timestamp: int  # Unix timestamp in milliseconds
    open: float
    high: float
    low: float
    close: float
    volume: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketMetadata:
    min_tick: Optional[float] = None
    trading_session: Optional[str] = None  # e.g., 'continuous', 'daily'
    contract_expiry: Optional[str] = None

@dataclass
class AnalysisResult:
    evidence: Dict[str, Any]
    probability: Optional[float] = None
    sample_count: Optional[int] = None
    status: str = 'pending'  # 'pending', 'completed', 'error'

@dataclass
class BotConfig:
    instruments: List[Instrument]
    risk_limit: float  # Maximum capital at risk per trade
    capital_allocation: float  # Percentage of portfolio allocated
    broker_connection: Dict[str, Any] = field(default_factory=dict)

from abc import ABC, abstractmethod

class AnalysisModule(ABC):
    @abstractmethod
    def analyze(self, data: List[OHLCVBar]) -> AnalysisResult:
        pass

class MarketDataProvider(ABC):
    @abstractmethod
    def get_ohlcv(self, instrument: Instrument, timeframe: str) -> List[OHLCVBar]:
        pass

class StrategyEvaluator(ABC):
    @abstractmethod
    def evaluate(self, analysis_result: AnalysisResult) -> str:
        # Returns 'buy', 'sell', 'neutral'
        pass
