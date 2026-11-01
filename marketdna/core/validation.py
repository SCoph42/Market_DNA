"""Reusable market-aware input validation helpers.

Do not apply universal positivity rules to prices: rare instruments and
markets can permit zero or negative prices. The caller must specify policy.
"""

import math
from numbers import Real
from typing import Optional

from .exceptions import DataValidationError


def require_finite_number(value: Real, field: str, *, allow_negative: bool = True,
                          allow_zero: bool = True) -> float:
    """Validate a finite real number; return its float representation."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise DataValidationError(f"{field} must be a real number")
    try:
        numeric = float(value)
    except (ValueError, OverflowError) as exc:
        raise DataValidationError(f"{field} must be finite") from exc
    if not math.isfinite(numeric):
        raise DataValidationError(f"{field} must be finite")
    if not allow_negative and numeric < 0:
        raise DataValidationError(f"{field} must not be negative")
    if not allow_zero and numeric == 0:
        raise DataValidationError(f"{field} must not be zero")
    return numeric


def validate_probability(value: Optional[Real], field: str = "probability") -> None:
    """Validate a probability in [0, 1], allowing None for unavailable."""
    if value is None:
        return
    numeric = require_finite_number(value, field)
    if not 0 <= numeric <= 1:
        raise DataValidationError(f"{field} must be between 0 and 1")


def validate_sample_count(count: Optional[int]) -> None:
    """Validate optional nonnegative observation count."""
    if count is not None and (type(count) is not int or count < 0):
        raise DataValidationError("sample_count must be a nonnegative integer")


def validate_ohlcv(open_price: Real, high: Real, low: Real,
                   close: Real, volume: Real, *, allow_nonpositive_prices: bool = False) -> None:
    """Check bar relationships and volume; price sign policy is explicit.

    This validates numerical consistency, not timestamps, market sessions,
    tick size, or whether a particular feed's volume units are meaningful.
    """
    prices = {
        "open": open_price, "high": high, "low": low, "close": close
    }
    converted = {
        name: require_finite_number(value, name,
                                    allow_negative=allow_nonpositive_prices,
                                    allow_zero=allow_nonpositive_prices)
        for name, value in prices.items()
    }
    require_finite_number(volume, "volume", allow_negative=False)
    if converted["high"] < max(converted["open"], converted["low"], converted["close"]):
        raise DataValidationError("high must be >= open, low, and close")
    if converted["low"] > min(converted["open"], converted["high"], converted["close"]):
        raise DataValidationError("low must be <= open, high, and close")
