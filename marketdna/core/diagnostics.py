"""Structured, serializable diagnostics for MarketDNA components."""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Optional


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Diagnostic:
    """A machine-readable observation about analysis or data quality.

    `timestamp` is a UTC Unix timestamp in milliseconds, if supplied.
    `instrument` is an optional market-qualified identifier.
    """

    code: str
    severity: Severity
    message: str
    module: str
    instrument: Optional[str] = None
    timestamp: Optional[int] = None

    def __post_init__(self) -> None:
        for name in ("code", "message", "module"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.severity, Severity):
            raise ValueError("severity must be a Severity member")
        if self.timestamp is not None and (type(self.timestamp) is not int or self.timestamp < 0):
            raise ValueError("timestamp must be a non-negative Unix millisecond integer")

    def to_dict(self) -> Dict[str, Any]:
        """Produce JSON-compatible primitive fields."""
        return asdict(self)
