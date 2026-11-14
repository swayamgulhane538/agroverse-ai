import unittest
from services.api.engines.calculators import AgriCalculators
from services.api.engines.crop_calendar import SmartCalendarEngine
from services.api.engines.schemes import SchemeEngine

class TestAgriEngines(unittest.TestCase):

    def test_net_mandi_realization(self):
        res = AgriCalculators.calculate_net_mandi_realization(
            gross_mandi_price_q=4980.0,
            distance_km=12.0,
            freight_rate_per_km_q=2.5,
            loading_unloading_q=25.0,
            mandi_cess_pct=1.05,
            expected_spoilage_pct=0.5
        )
        self.assertEqual(res["gross_mandi_price"], 4980.0)
        self.assertEqual(res["transport_cost"], 30.0) # 12 * 2.5
        self.assertLess(res["net_realized_price_q"], 4980.0)
        self.assertGreater(res["net_realized_price_q"], 4800.0)

    def test_store_vs_sell(self):
        res = AgriCalculators.calculate_store_vs_sell(
            current_mandi_price_q=4980.0,
            storage_months=3,
            monthly_storage_rent_q=35.0,
            monthly_interest_rate_pct=0.8,
            shrinkage_weight_loss_pct=2.0,
            loading_handling_q=20.0
        )
        self.assertEqual(res["current_price_q"], 4980.0)
        self.assertEqual(res["storage_months"], 3)
        self.assertEqual(res["total_storage_rent"], 105.0) # 3 * 35
        self.assertGreater(res["breakeven_future_price_q"], res["current_price_q"])
        self.assertGreater(res["required_price_rise_pct"], 0)

    def test_fragmentation_index(self):
        # Single parcel should have 0 fragmentation
        res_single = AgriCalculators.calculate_fragmentation_index([3.5])
        self.assertEqual(res_single["fragmentation_index"], 0.0)

        # Three fragmented parcels
        res_frag = AgriCalculators.calculate_fragmentation_index([2.0, 1.5, 0.7])
        self.assertEqual(res_frag["num_parcels"], 3)
        self.assertEqual(res_frag["total_area_ha"], 4.2)
        self.assertGreater(res_frag["fragmentation_index"], 0.5)

    def test_calendar_engine(self):
        schedule = SmartCalendarEngine.generate_rabi_schedule(crop_id="chickpea", sowing_date="2026-11-15")
        self.assertEqual(schedule.provenance.source, "ICAR / Dr. PDKV Akola Agronomic Package")
        self.assertEqual(len(schedule.value), 5)
        self.assertEqual(schedule.value[1]["stage"], "Optimal Sowing Window")

    def test_scheme_matching(self):
        profile = {
            "land_ha": 2.0,
            "state": "Maharashtra",
            "has_water_source": True
        }
        matched = SchemeEngine.match_schemes(profile)
        self.assertGreaterEqual(len(matched.value), 5)
        
        # Check PM-KISAN
        pm_kisan = next(s for s in matched.value if s["scheme_id"] == "pm_kisan")
        self.assertEqual(pm_kisan["verdict"], "likely")
        
        # Check Farm Pond
        pond = next(s for s in matched.value if s["scheme_id"] == "mh_magel_tyala_shet_tale")
        self.assertEqual(pond["verdict"], "likely")

if __name__ == "__main__":
    unittest.main()
