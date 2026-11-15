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
        from services.api.engines.spraying import (
            SmartSprayingEngine,
            calculate_wet_bulb_stull,
            calculate_delta_t
        )
        from services.api.data_loader import get_spray_products

        # 1. Test Stull (2011) Wet Bulb and Delta-T formula
        # Known benchmark: T=20°C, RH=50% -> Tw ~ 13.7°C, Delta-T ~ 6.3°C
        tw = calculate_wet_bulb_stull(20.0, 50.0)
        self.assertAlmostEqual(tw, 13.70, delta=0.25)
        dt = calculate_delta_t(20.0, 50.0)
        self.assertAlmostEqual(dt, 6.30, delta=0.25)

        # 2. Test Hourly Suitability Rules
        # Drift hazard (> 15 km/h)
        eval_drift = SmartSprayingEngine.evaluate_hourly_suitability(
            temp_c=25.0, rh_pct=50.0, wind_kmh=18.0,
            gust_kmh=20.0, rain_prob_pct=5, precip_mm=0.0, is_day=1
        )
        self.assertEqual(eval_drift["status"], "do_not_spray")
        self.assertIn("drift", eval_drift["primary_reason"].lower())

        # Calm inversion caution (< 3 km/h)
        eval_calm = SmartSprayingEngine.evaluate_hourly_suitability(
            temp_c=22.0, rh_pct=60.0, wind_kmh=2.0,
            gust_kmh=3.0, rain_prob_pct=0, precip_mm=0.0, is_day=1
        )
        self.assertEqual(eval_calm["status"], "caution")
        self.assertIn("inversion", eval_calm["primary_reason"].lower())

        # Rain wash-off (> 35%)
        eval_rain = SmartSprayingEngine.evaluate_hourly_suitability(
            temp_c=26.0, rh_pct=60.0, wind_kmh=8.0,
            gust_kmh=10.0, rain_prob_pct=45, precip_mm=1.5, is_day=1
        )
        self.assertEqual(eval_rain["status"], "do_not_spray")
        self.assertIn("rain", eval_rain["primary_reason"].lower())

        # Extreme temperature (> 33°C) -> do_not_spray
        eval_hot = SmartSprayingEngine.evaluate_hourly_suitability(
            temp_c=35.0, rh_pct=30.0, wind_kmh=9.0,
            gust_kmh=12.0, rain_prob_pct=0, precip_mm=0.0, is_day=1
        )
        self.assertEqual(eval_hot["status"], "do_not_spray")
        self.assertIn("evaporation", eval_hot["primary_reason"].lower())

        # Elevated temperature (30-33°C) -> caution
        eval_warm = SmartSprayingEngine.evaluate_hourly_suitability(
            temp_c=31.5, rh_pct=40.0, wind_kmh=9.0,
            gust_kmh=12.0, rain_prob_pct=0, precip_mm=0.0, is_day=1
        )
        self.assertEqual(eval_warm["status"], "caution")
        self.assertIn("temperature", eval_warm["primary_reason"].lower())

        # Optimal daylight hour
        eval_opt = SmartSprayingEngine.evaluate_hourly_suitability(
            temp_c=24.0, rh_pct=55.0, wind_kmh=8.0,
            gust_kmh=10.0, rain_prob_pct=5, precip_mm=0.0, is_day=1
        )
        self.assertEqual(eval_opt["status"], "optimal")

        # 3. Test Sensitive Zone Drift check
        # Wind blowing FROM 270 (W) -> downwind heading is 90 (E).
        # Beehives at bearing 85 (E) -> within +/- 45 deg cone -> warning
        warnings = SmartSprayingEngine.check_sensitive_zone_drift(270)
        self.assertTrue(any("Beehives" in w["zone_name"] for w in warnings))

        # 4. Test Verified Product Knowledge Base
        products = get_spray_products()
        self.assertGreaterEqual(len(products), 5)
        emamectin = next(p for p in products if p.get("id") == "chickpea_pod_borer_emamectin")
        self.assertEqual(emamectin["status"], "verified")
        self.assertTrue(emamectin["cibrc_registered"])
        self.assertIsNotNone(emamectin["label_dose_ha"])
        self.assertEqual(emamectin["phi_days"], 11)

        unverified = next(p for p in products if p.get("id") == "experimental_combo_unverified")
        self.assertEqual(unverified["status"], "unverified")
        self.assertFalse(unverified["cibrc_registered"])
        self.assertIsNone(unverified["label_dose_ha"])
        self.assertIsNone(unverified["phi_days"])

        # 5. Full Automatic Advisory Integration Test
        adv = SmartSprayingEngine.get_automatic_spraying_advisory(parcel_id="p1")
        self.assertIn(adv.provenance.mode, ["live", "cached", "demo"])
        self.assertIn("spray_windows", adv.value)
        self.assertEqual(len(adv.value["hourly_evaluations_72h"]), 72)
        self.assertIn("overall_banner", adv.value)
        self.assertIn("sensitive_zone_drift", adv.value)
        self.assertIn("verified_products", adv.value)

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

    def test_mandi_and_msp(self):
        from services.api.engines.msp import MSPEngine
        from services.api.market.agmarknet import AgmarknetAdapter, calculate_haversine_distance, calculate_net_mandi_price

        # 1. Test Name Normalisation across English, Hindi, Marathi, and Agmarknet feed names
        self.assertEqual(MSPEngine.normalize_commodity_name("bengal gram(gram)(whole)"), "chickpea")
        self.assertEqual(MSPEngine.normalize_commodity_name("हरभरा"), "chickpea")
        self.assertEqual(MSPEngine.normalize_commodity_name("चना"), "chickpea")
        self.assertEqual(MSPEngine.normalize_commodity_name("Soyabean"), "soybean")
        self.assertEqual(MSPEngine.normalize_commodity_name("सोयाबीन"), "soybean")
        self.assertEqual(MSPEngine.normalize_commodity_name("Lokwan Wheat"), "wheat")
        self.assertEqual(MSPEngine.normalize_commodity_name("गहू"), "wheat")

        # 2. Test Marketing Season Selection
        # Rabi crop sown in Nov 2026 marketed in 2027 -> RMS 2027-28
        rabi_season = MSPEngine.auto_pick_marketing_season(crop_type="rabi", reference_date_str="2026-11-15")
        self.assertEqual(rabi_season, "RMS 2027-28")

        # Kharif crop sold in Nov 2026 -> KMS 2026-27
        kharif_season = MSPEngine.auto_pick_marketing_season(crop_type="kharif", reference_date_str="2026-11-15")
        self.assertEqual(kharif_season, "KMS 2026-27")

        # 3. Test Verified Seed Values from CCEA/PIB
        chickpea_msp = MSPEngine.get_msp_for_commodity("chickpea")
        self.assertEqual(chickpea_msp["status"], "verified")
        self.assertEqual(chickpea_msp["msp_inr_quintal"], 5958)
        self.assertEqual(chickpea_msp["marketing_season"], "RMS 2027-28")

        wheat_msp = MSPEngine.get_msp_for_commodity("wheat")
        self.assertEqual(wheat_msp["status"], "verified")
        self.assertEqual(wheat_msp["msp_inr_quintal"], 2610)
        self.assertEqual(wheat_msp["marketing_season"], "RMS 2027-28")

        soybean_msp = MSPEngine.get_msp_for_commodity("soybean")
        self.assertEqual(soybean_msp["status"], "verified")
        self.assertEqual(soybean_msp["msp_inr_quintal"], 5708)
        self.assertEqual(soybean_msp["marketing_season"], "KMS 2026-27")

        # 4. Test MSP Gap Calculation and Neutral Explanation
        gap_above = MSPEngine.calculate_msp_gap(6200, chickpea_msp)
        self.assertTrue(gap_above["is_above_msp"])
        self.assertGreater(gap_above["gap_inr"], 0)
        self.assertIn("Above MSP", gap_above["status_badge"])

        gap_below = MSPEngine.calculate_msp_gap(5820, chickpea_msp)
        self.assertFalse(gap_below["is_above_msp"])
        self.assertLess(gap_below["gap_inr"], 0)
        self.assertIn("Below MSP", gap_below["status_badge"])
        self.assertIn("NAFED", gap_below["explanation"])

        # 5. Test Distance & Net Mandi Price Realization
        dist = calculate_haversine_distance(21.1458, 79.0882, 21.3850, 78.9180) # Nagpur to Saoner
        self.assertGreater(dist, 25.0)
        self.assertLess(dist, 45.0)

        net_calc = calculate_net_mandi_price(gross_modal_price_q=5890.0, distance_km=32.0)
        self.assertLess(net_calc["net_realized_price_q"], 5890.0)
        self.assertGreater(net_calc["net_realized_price_q"], 5600.0)

        # 6. Test Price Alert Evaluation (Rule: Never trigger on demo data)
        AgmarknetAdapter.set_price_alert(commodity="soybean", target_price_q=5600, condition="gte", market="kalamna")
        test_prices = [{"commodity_id": "soybean", "market_id": "kalamna", "market": "Kalamna APMC", "modal_price": 5700, "arrival_date": "2026-11-15"}]

        # Must NOT trigger when is_demo is True
        alerts_demo = AgmarknetAdapter.evaluate_price_alerts(test_prices, is_demo=True)
        self.assertEqual(len(alerts_demo), 0)

        # Must trigger when is_demo is False
        alerts_live = AgmarknetAdapter.evaluate_price_alerts(test_prices, is_demo=False)
        self.assertEqual(len(alerts_live), 1)
        self.assertEqual(alerts_live[0]["price"], 5700)

        # 7. Test Historical Price Series Coverage
        hist = AgmarknetAdapter.get_historical_price_series(commodity="chickpea", interval="30D")
        self.assertEqual(len(hist["dates"]), 31)
        self.assertIn("History building since", hist["coverage_notice"])
        self.assertIn("delta_7d_inr", hist["metrics"])

if __name__ == "__main__":
    unittest.main()


