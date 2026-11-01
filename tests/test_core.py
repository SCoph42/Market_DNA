"""Standard-library unit tests; run with python3 -m unittest discover."""

import unittest

from marketdna.core.diagnostics import Diagnostic, Severity
from marketdna.core.exceptions import DataValidationError, MarketDNAError
from marketdna.core.validation import (
    require_finite_number, validate_ohlcv, validate_probability,
    validate_sample_count,
)


class TestValidation(unittest.TestCase):
    def test_valid_bar(self):
        validate_ohlcv(100, 105, 98, 102, 250)

    def test_invalid_bar_bounds(self):
        with self.assertRaises(DataValidationError):
            validate_ohlcv(100, 99, 98, 102, 250)
        with self.assertRaises(DataValidationError):
            validate_ohlcv(100, 105, 101, 102, 250)

    def test_negative_volume_and_nonfinite(self):
        with self.assertRaises(DataValidationError):
            validate_ohlcv(100, 105, 98, 102, -1)
        with self.assertRaises(DataValidationError):
            require_finite_number(float("nan"), "price")
        with self.assertRaises(DataValidationError):
            validate_ohlcv(100, float("inf"), 98, 102, 100)

    def test_explicit_nonpositive_price_policy(self):
        with self.assertRaises(DataValidationError):
            validate_ohlcv(-1, 1, -3, 0, 12)
        validate_ohlcv(-1, 1, -3, 0, 12, allow_nonpositive_prices=True)

    def test_probability_and_count(self):
        validate_probability(0)
        validate_probability(1)
        validate_probability(None)
        validate_sample_count(0)
        with self.assertRaises(DataValidationError):
            validate_probability(1.01)
        with self.assertRaises(DataValidationError):
            validate_probability(float("nan"))
        with self.assertRaises(DataValidationError):
            validate_sample_count(-1)
        with self.assertRaises(DataValidationError):
            validate_sample_count(True)

    def test_exception_hierarchy(self):
        self.assertTrue(issubclass(DataValidationError, MarketDNAError))


class TestDiagnostics(unittest.TestCase):
    def test_serializable_diagnostic(self):
        diagnostic = Diagnostic(
            code="DATA_GAP_DETECTED", severity=Severity.WARNING,
            message="Missing expected bars", module="data.validation",
            instrument="MES", timestamp=1793404800000,
        )
        self.assertEqual(diagnostic.to_dict()["severity"], "warning")

    def test_invalid_diagnostic(self):
        with self.assertRaises(ValueError):
            Diagnostic(code="", severity=Severity.ERROR, message="test", module="data")
        with self.assertRaises(ValueError):
            Diagnostic(code="ERR", severity="error", message="test", module="data")


if __name__ == "__main__":
    unittest.main()
