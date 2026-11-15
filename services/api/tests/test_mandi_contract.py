import unittest
import json
from pathlib import Path
from services.api.engines.msp import MSPEngine
from services.api.market.agmarknet import AgmarknetAdapter

class TestMandiContractAndE2E(unittest.TestCase):
    """
    Contract & E2E Tests:
    - Validates schema contract against real/recorded Agmarknet fixtures.
    - E2E: Changing crop/district updates list, chart, and MSP.
    - Setting alert and evaluating against fixture data.
    """

    def setUp(self):
        fixture_path = Path(__file__).resolve().parent / "fixtures" / "agmarknet_fixture.json"
        self.assertTrue(fixture_path.exists(), f"Fixture missing: {fixture_path}")
        with open(fixture_path, "r", encoding="utf-8") as f:
            self.fixture = json.load(f)

    def test_agmarknet_fixture_contract(self):
        records = self.fixture.get("records", [])
        self.assertGreaterEqual(len(records), 4)

        for r in records:
            # Contract assertions for Agmarknet schema
            self.assertIn("market", r)
            self.assertIn("commodity", r)
            self.assertIn("variety", r)
            self.assertIn("arrival_date", r)
            self.assertIn("min_price", r)
            self.assertIn("max_price", r)
            self.assertIn("modal_price", r)

            # Normalization contract
            norm_id = MSPEngine.normalize_commodity_name(r["commodity"])
            self.assertIn(norm_id, ["chickpea", "soybean", "wheat"])

    def test_e2e_crop_and_district_switch(self):
        # 1. Query Chickpea in Nagpur
        res_chana = AgmarknetAdapter.get_mandi_rates(commodity="chickpea", district="Nagpur")
        self.assertEqual(res_chana.value["commodity_info"]["commodity_id"], "chickpea")
        self.assertGreaterEqual(len(res_chana.value["mandi_records"]), 1)
        self.assertEqual(res_chana.value["msp_benchmark"]["marketing_season"], "RMS 2027-28")
        self.assertEqual(res_chana.value["msp_benchmark"]["msp_inr_quintal"], 5958)

        # 2. Switch to Soybean in Wardha
        res_soya = AgmarknetAdapter.get_mandi_rates(commodity="soybean", district="Wardha")
        self.assertEqual(res_soya.value["commodity_info"]["commodity_id"], "soybean")
        self.assertEqual(res_soya.value["msp_benchmark"]["marketing_season"], "KMS 2026-27")
        self.assertEqual(res_soya.value["msp_benchmark"]["msp_inr_quintal"], 5708)

        # 3. Switch to Wheat
        res_wheat = AgmarknetAdapter.get_mandi_rates(commodity="wheat")
        self.assertEqual(res_wheat.value["commodity_info"]["commodity_id"], "wheat")
        self.assertEqual(res_wheat.value["msp_benchmark"]["marketing_season"], "RMS 2027-28")
        self.assertEqual(res_wheat.value["msp_benchmark"]["msp_inr_quintal"], 2610)

    def test_e2e_alert_fires_in_fixture_test(self):
        # Set an alert for Soybean >= 5600 at Kalamna
        alert = AgmarknetAdapter.set_price_alert(
            commodity="soybean",
            target_price_q=5600.0,
            condition="gte",
            market="kalamna",
            user_id="test_farmer"
        )
        self.assertEqual(alert["commodity_id"], "soybean")

        # Parse fixture records into normalized live feed format
        live_feed = []
        for r in self.fixture["records"]:
            norm_id = MSPEngine.normalize_commodity_name(r["commodity"])
            live_feed.append({
                "commodity_id": norm_id,
                "market_id": r["market"].lower(),
                "market": r["market"] + " APMC",
                "modal_price": float(r["modal_price"]),
                "arrival_date": r["arrival_date"]
            })

        # Evaluate against live fixture (is_demo=False simulating live arrival)
        triggered = AgmarknetAdapter.evaluate_price_alerts(live_feed, is_demo=False)
        self.assertTrue(any(a["commodity"] == "Soybean (Yellow)" for a in triggered))

        # Cleanup alert
        AgmarknetAdapter.delete_price_alert(alert["alert_id"])

if __name__ == "__main__":
    unittest.main()
