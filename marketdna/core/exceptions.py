"""Shared exception types for MarketDNA.

Use exceptions for invalid inputs and operational failures. Expected analytical
outcomes (such as too few pattern matches) can instead use a diagnostic result.
"""


class MarketDNAError(Exception):
    """Base class for application-specific errors."""


class DataValidationError(MarketDNAError, ValueError):
    """An input observation or data structure violates a validation rule."""


class DataProviderError(MarketDNAError):
    """A market data provider could not supply requested data."""


class ConfigurationError(MarketDNAError, ValueError):
    """A configuration parameter is invalid or unsupported."""


class AnalysisError(MarketDNAError):
    """An analysis module could not complete its calculation."""


class InsufficientDataError(MarketDNAError):
    """A requested operation requires more usable observations."""
