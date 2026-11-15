from typing import Dict, Any, List
try:
    from ..models.provenance import Provenanced, ProvenanceMetadata
except (ImportError, ValueError):
    from models.provenance import Provenanced, ProvenanceMetadata


class SmartSprayingEngine:
    """
    Intelligent Weather-Based Spraying Advisory System adhering strictly to
    Central Insecticides Board & Registration Committee (CIBRC) & Integrated Pest Management (IPM).
    Evaluates: Wind Speed, Rainfall Probability, Ambient Temperature, Relative Humidity,
    Chemical Rainfastness, Droplet Drift Risk, and Pre-Harvest Interval (PHI).
    """

    @classmethod
    def evaluate_spraying_conditions(
        cls,
        crop: str = "chickpea",
        target_pest_or_disease: str = "pod_borer",
        wind_speed_kmh: float = 8.5,
        rain_prob_next_24h_pct: int = 5,
        temp_c: float = 28.5,
        humidity_pct: float = 55.0
    ) -> Provenanced[Dict[str, Any]]:
        warnings = []
        is_suitable = True
        risk_score = "LOW"  # LOW, MODERATE, HIGH, HAZARDOUS

        # 1. Wind Analysis (Drift Hazard)
        if wind_speed_kmh > 15.0:
            is_suitable = False
            risk_score = "HAZARDOUS"
            warnings.append(
                f"Wind speed ({wind_speed_kmh} km/h) exceeds safe threshold of 15 km/h. "
                "CRITICAL DRIFT HAZARD: Spray droplets will drift off-target, damaging beneficial pollinators and wasting costly chemical."
            )
        elif wind_speed_kmh > 10.0:
            warnings.append(
                f"Wind speed ({wind_speed_kmh} km/h) is moderate. Use low-drift air-induction nozzles and keep spray boom 50cm above crop canopy."
            )

        # 2. Precipitation & Rainfastness Analysis
        if rain_prob_next_24h_pct > 35:
            is_suitable = False
            risk_score = "HAZARDOUS"
            warnings.append(
                f"Rain probability ({rain_prob_next_24h_pct}%) within 24h is elevated. "
                "RAIN WASHOFF RISK: Most standard contact and biological sprays require at least 4 to 6 hours of clear rainfast period."
            )

        # 3. Thermal & Evaporation Analysis
        if temp_c > 33.0:
            warnings.append(
                f"High temperature ({temp_c}°C) accelerates water droplet evaporation before reaching target leaves, causing chemical scorching (phytotoxicity)."
            )
            if is_suitable:
                risk_score = "MODERATE"

        # 4. Fungal Risk (High Humidity + Warm Temps)
        fungal_spore_risk = (humidity_pct > 75.0 and 20.0 <= temp_c <= 28.0)
        if fungal_spore_risk:
            warnings.append(
                "Microclimate warning: Relative humidity > 75% with temperatures 20-28°C creates ideal conditions for fungal spore germination (Ascochyta blight / Rust)."
            )

        # Recommended Hours
        recommended_windows = [
            {"time_window": "06:30 AM – 09:30 AM", "condition": "Calm morning winds, high relative humidity, closed stomata on weeds, no thermal updrafts."},
            {"time_window": "04:30 PM – 06:30 PM", "condition": "Declining solar radiation, cooler leaf surface temperatures, minimal pollinator activity."}
        ]

        # Approved CIBRC & Organic IPM chemical/biological choices
        pest_advisories = {
            "pod_borer": {
                "name": "Chickpea Pod Borer (Helicoverpa armigera)",
                "etl_threshold": "1 larva per meter row or 5% pod damage",
                "organic_bio_first_line": "Spray 5% NSKE (Neem Seed Kernel Extract) or HaNPV @ 250 LE/ha or Bacillus thuringiensis (Bt) @ 1.0 kg/ha.",
                "chemical_approved": "Emamectin Benzoate 5% SG @ 4g/10L water OR Chlorantraniliprole 18.5% SC @ 3ml/10L water.",
                "pre_harvest_interval_days": 11,
                "dosage_water_per_acre": "150–200 Litres clean water"
            },
            "wilt": {
                "name": "Fusarium Wilt / Root Rot",
                "etl_threshold": "Seedling damping-off / yellowing of lower leaves",
                "organic_bio_first_line": "Soil drenching with Trichoderma viride / T. harzianum @ 10g/L water around affected plant roots.",
                "chemical_approved": "Carbendazim 50% WP @ 1g/L water (Strict seed/root drench only; avoid indiscriminate foliar spray).",
                "pre_harvest_interval_days": 21,
                "dosage_water_per_acre": "200 Litres clean water"
            },
            "sucking_pests": {
                "name": "Aphids / Thrips / Whiteflies",
                "etl_threshold": "5-10 nymphs per leaf",
                "organic_bio_first_line": "Neem Oil 10,000 ppm @ 2ml/L water + Verticillium lecanii @ 5g/L water.",
                "chemical_approved": "Thiamethoxam 25% WG @ 2g/10L water OR Acetamiprid 20% SP @ 2g/10L water.",
                "pre_harvest_interval_days": 15,
                "dosage_water_per_acre": "150 Litres clean water"
            }
        }

        selected_pest_info = pest_advisories.get(target_pest_or_disease, pest_advisories["pod_borer"])

        return Provenanced(
            value={
                "crop": crop,
                "target_pest": selected_pest_info["name"],
                "is_suitable_now": is_suitable,
                "risk_rating": risk_score,
                "current_weather": {
                    "wind_speed_kmh": wind_speed_kmh,
                    "rain_prob_pct": rain_prob_next_24h_pct,
                    "temp_c": temp_c,
                    "humidity_pct": humidity_pct
                },
                "warnings": warnings if warnings else ["All meteorological parameters (wind, rain probability, temp) are within the safe spraying envelope."],
                "recommended_spray_windows": recommended_windows,
                "safety_guidelines": [
                    "Always wear Personal Protective Equipment (PPE): mask, rubber gloves, and eye goggles.",
                    "Spray with the wind at your back; NEVER walk into the chemical mist.",
                    "Calibrate knapsack sprayer to deliver 150-200 Litres of spray solution per acre.",
                    "Adhere strictly to the Pre-Harvest Interval (PHI) before picking or harvesting crops for human/animal consumption."
                ],
                "approved_remedy": selected_pest_info
            },
            provenance=ProvenanceMetadata(
                source="CIBRC & Dr. PDKV Akola IPM Division",
                dataset="Central Insecticides Board & Registration Committee Advisory",
                kind="ai_estimate",
                mode="live",
                spatialResolution="Nagpur Field-Level Weather Window",
                notes="Decision support algorithm enforcing CIBRC approved label dosages and weather safety constraints.",
                url="https://cibrc.nic.in"
            )
        )
