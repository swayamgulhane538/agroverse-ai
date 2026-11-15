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

    def test_fertilizer_engine(self):
        from services.api.engines.fertilizer import SmartFertilizerEngine
        rec = SmartFertilizerEngine.calculate_recommendation(crop_id="chickpea", field_size_acres=2.5)
        self.assertEqual(rec.value["crop_id"], "chickpea")
        self.assertGreater(rec.value["commercial_bag_recommendation"]["dap_50kg_bags"], 0)
        self.assertIn("jeevamrut", rec.value["organic_alternatives"])
        self.assertIn("title", rec.value["diy_preparation_guide"])

    def test_spraying_advisory(self):
        from services.api.engines.spraying import SmartSprayingEngine
        # Calm conditions -> suitable
        calm = SmartSprayingEngine.evaluate_spraying_conditions(wind_speed_kmh=8.0, rain_prob_next_24h_pct=5)
        self.assertTrue(calm.value["is_suitable_now"])
        # High wind -> hazard
        windy = SmartSprayingEngine.evaluate_spraying_conditions(wind_speed_kmh=22.0)
        self.assertFalse(windy.value["is_suitable_now"])
        self.assertEqual(windy.value["risk_rating"], "HAZARDOUS")

    def test_disease_engine(self):
        from services.api.engines.disease import PlantDiseaseEngine
        diag = PlantDiseaseEngine.diagnose_image(filename="chickpea_pod_borer.jpg", crop_hint="chickpea")
        self.assertEqual(diag.value["crop_species"], "Chickpea (Chana)")
        self.assertIn("Gram Pod Borer", diag.value["diagnosis"])
        self.assertGreaterEqual(diag.value["confidence_score_pct"], 80.0)
        self.assertIn("NSKE", diag.value["organic_biological_treatments"][0])

    def test_optimizer_engine(self):
        from services.api.engines.optimizer import FarmerIncomeOptimizerEngine
        opt = FarmerIncomeOptimizerEngine.calculate_custom_income(land_area_ha=2.0, crop_id="chickpea")
        self.assertEqual(opt.value["land_area_ha"], 2.0)
        self.assertGreater(opt.value["financial_metrics"]["gross_revenue_inr"], 0)
        self.assertGreater(opt.value["financial_metrics"]["net_profit_inr"], 0)
        self.assertEqual(len(opt.value["comparative_ranking"]), 4)

    def test_earth_obs_adapter(self):
        from services.api.nasa.earth_obs import NasaEarthObsAdapter
        eo = NasaEarthObsAdapter.get_soil_moisture_and_precipitation()
        self.assertEqual(eo.value["smap_soil_moisture"]["sensor"], "NASA SMAP L4_SM Global Soil Moisture")
        self.assertGreater(eo.value["smap_soil_moisture"]["rootzone_sm_0_100cm_m3_m3"], 0.20)
        self.assertIn("past_30d_cumulative_mm", eo.value["gpm_precipitation"])

if __name__ == "__main__":
    unittest.main()

