
import unittest

from marketdna.data.models import (
    Instrument,
    OHLCVBar,
    AnalysisResult,
    AnalysisModule,
    MarketDataProvider,
    StrategyEvaluator,
)


class TestMarketDNAModels(unittest.TestCase):

    def test_instrument_initialization(self):
        instrument = Instrument(
            symbol="ES",
            exchange="CME",
            market_type="futures",
        )

        self.assertEqual(instrument.symbol, "ES")
        self.assertEqual(instrument.exchange, "CME")
        self.assertEqual(instrument.market_type, "futures")

    def test_ohlcv_bar_initialization(self):
        bar = OHLCVBar(
            timestamp=1700000000,
            open=4500.0,
            high=4510.0,
            low=4495.0,
            close=4505.0,
            volume=1000.0,
        )

        self.assertEqual(bar.timestamp, 1700000000)
        self.assertEqual(bar.open, 4500.0)
        self.assertEqual(bar.high, 4510.0)
        self.assertEqual(bar.low, 4495.0)
        self.assertEqual(bar.close, 4505.0)
        self.assertEqual(bar.volume, 1000.0)

    def test_analysis_result_initialization(self):
        result = AnalysisResult(
            evidence={"pattern": "5-bar rise"},
            probability=0.85,
            sample_count=120,
        )

        self.assertEqual(result.evidence, {"pattern": "5-bar rise"})
        self.assertEqual(result.probability, 0.85)
        self.assertEqual(result.sample_count, 120)

    def test_abstract_classes_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            AnalysisModule()

        with self.assertRaises(TypeError):
            MarketDataProvider()

        with self.assertRaises(TypeError):
            StrategyEvaluator()


if __name__ == "__main__":
    unittest.main()
