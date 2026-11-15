import os
import unittest


class TestGrepMandi(unittest.TestCase):
    """
    Grep tests asserting that no legacy hardcoded prices, legacy MSP values,
    or static mode chips exist in the codebase outside msp_table and fixtures.
    """

    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    def test_no_legacy_hardcoded_msp_values_in_ui(self):
        """Ensure legacy MSP values 5650, 2425, 4892 do not appear in index.html."""
        index_path = os.path.join(self.root_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Legacy MSP values must be absent
        self.assertNotIn("5,650", content, "Legacy Chickpea MSP 5,650 found in index.html")
        self.assertNotIn("2,425", content, "Legacy Wheat MSP 2,425 found in index.html")
        self.assertNotIn("4,892", content, "Legacy Soybean MSP 4,892 found in index.html")
        self.assertNotIn("5650", content, "Legacy Chickpea MSP 5650 found in index.html")

    def test_no_static_kalamna_live_chip(self):
        """The Kalamna APMC Live chip must be dynamic and reflect real mode, not static."""
        index_path = os.path.join(self.root_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertNotIn("Kalamna APMC Live Rates", content, "Static Kalamna live chip found in index.html")

    def test_msp_table_contains_verified_pib_benchmarks(self):
        """Verify msp_table.json has verified CCEA/PIB numbers."""
        import json
        msp_path = os.path.join(self.root_dir, "services", "api", "data", "msp_table.json")
        with open(msp_path, "r", encoding="utf-8") as f:
            table = json.load(f)

        # Check Gram RMS 2026-27 and RMS 2027-28
        gram_entry = next((r for r in table if r["commodity_id"] == "chickpea"), None)
        self.assertIsNotNone(gram_entry)
        seasons = gram_entry.get("seasons", {})
        self.assertEqual(seasons.get("RMS 2026-27", {}).get("msp_inr_quintal"), 5875)
        self.assertEqual(seasons.get("RMS 2027-28", {}).get("msp_inr_quintal"), 5958)

        # Check Wheat
        wheat_entry = next((r for r in table if r["commodity_id"] == "wheat"), None)
        self.assertIsNotNone(wheat_entry)
        w_seasons = wheat_entry.get("seasons", {})
        self.assertEqual(w_seasons.get("RMS 2026-27", {}).get("msp_inr_quintal"), 2585)
        self.assertEqual(w_seasons.get("RMS 2027-28", {}).get("msp_inr_quintal"), 2610)

        # Check Soybean
        soy_entry = next((r for r in table if r["commodity_id"] == "soybean"), None)
        self.assertIsNotNone(soy_entry)
        s_seasons = soy_entry.get("seasons", {})
        self.assertEqual(s_seasons.get("KMS 2026-27", {}).get("msp_inr_quintal"), 5708)

    def test_demo_alert_safety_rule(self):
        """Price alerts must never evaluate on demo data."""
        from services.api.market.agmarknet import AgmarknetAdapter
        adapter = AgmarknetAdapter()
        # Add test alert
        adapter.set_price_alert(
            commodity="soybean",
            target_price_q=5000.0,
            condition="gte",
            market="kalamna"
        )
        rates = [
            {
                "commodity_id": "soybean",
                "market_id": "kalamna",
                "modal_price": 5708.0
            }
        ]
        # When is_demo is True, must return 0 triggered alerts
        triggered = adapter.evaluate_price_alerts(current_rates=rates, is_demo=True)
        self.assertEqual(len(triggered), 0, "Price alerts triggered on demo data!")

        # When is_demo is False, should evaluate
        triggered_live = adapter.evaluate_price_alerts(current_rates=rates, is_demo=False)
        self.assertGreaterEqual(len(triggered_live), 1, "Price alert failed to trigger on live data")


if __name__ == "__main__":
    unittest.main()
