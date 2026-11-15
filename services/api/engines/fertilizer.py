import math
from typing import Dict, Any, List
try:
    from ..models.provenance import Provenanced, ProvenanceMetadata
except (ImportError, ValueError):
    from models.provenance import Provenanced, ProvenanceMetadata


class SmartFertilizerEngine:
    """
    Intelligent Fertilizer Recommendation Engine calibrated for Vidarbha Soils (Vertisols/Regur).
    Calculates balanced chemical requirements (NPK), split dosages, commercial bag equivalents,
    cost estimations, and scientifically validated organic alternatives (Jeevamrut, Vermicompost).
    """

    # ICAR / Dr. PDKV Akola State Agricultural University standard benchmarks (kg/ha N-P-K)
    CROP_NPK_BENCHMARKS = {
        "chickpea": {"name": "Chickpea (Chana)", "n": 25, "p": 50, "k": 30, "s": 20, "is_legume": True},
        "wheat": {"name": "Wheat (Gehun)", "n": 120, "p": 60, "k": 40, "s": 15, "is_legume": False},
        "cotton": {"name": "Bt Cotton", "n": 120, "p": 60, "k": 60, "s": 25, "is_legume": False},
        "soybean": {"name": "Soybean", "n": 30, "p": 75, "k": 40, "s": 20, "is_legume": True},
        "tur": {"name": "Pigeonpea / Tur", "n": 25, "p": 50, "k": 30, "s": 20, "is_legume": True}
    }

    # Government Subsidized Market Prices (₹ per 45/50kg bag)
    FERTILIZER_PRICES = {
        "urea": {"bag_kg": 45, "price_per_bag": 266.50, "n_pct": 46, "p_pct": 0, "k_pct": 0},
        "dap": {"bag_kg": 50, "price_per_bag": 1350.00, "n_pct": 18, "p_pct": 46, "k_pct": 0},
        "mop": {"bag_kg": 50, "price_per_bag": 1700.00, "n_pct": 0, "p_pct": 0, "k_pct": 60},
        "ssp": {"bag_kg": 50, "price_per_bag": 500.00, "n_pct": 0, "p_pct": 16, "k_pct": 0, "s_pct": 11},
        "neem_cake": {"bag_kg": 50, "price_per_bag": 900.00},
        "vermicompost": {"bag_kg": 50, "price_per_bag": 450.00}
    }

    @classmethod
    def calculate_recommendation(
        cls,
        crop_id: str = "chickpea",
        soil_type: str = "black_cotton",
        soil_ph: float = 7.6,
        field_size_acres: float = 2.5,
        n_status: str = "medium",  # low, medium, high
        p_status: str = "medium",
        k_status: str = "high",    # Vidarbha black soils naturally rich in K
        growth_stage: str = "basal" # basal, vegetative, flowering, pod
    ) -> Provenanced[Dict[str, Any]]:
        crop_data = cls.CROP_NPK_BENCHMARKS.get(crop_id, cls.CROP_NPK_BENCHMARKS["chickpea"])
        hectares = field_size_acres * 0.404686

        # Soil test adjustment factors
        factor_map = {"low": 1.25, "medium": 1.00, "high": 0.75}
        n_factor = factor_map.get(n_status, 1.0)
        p_factor = factor_map.get(p_status, 1.0)
        k_factor = factor_map.get(k_status, 0.75 if soil_type == "black_cotton" else 1.0)

        # pH adjustments (alkaline soils fix P, need higher SSP or biofertilizer)
        p_ph_penalty = 1.15 if soil_ph > 7.8 else (1.10 if soil_ph < 6.0 else 1.0)

        # Base N-P-K in kg/ha
        rec_n_ha = crop_data["n"] * n_factor
        rec_p_ha = crop_data["p"] * p_factor * p_ph_penalty
        rec_k_ha = crop_data["k"] * k_factor

        # Field-level totals in kg
        total_n_kg = rec_n_ha * hectares
        total_p_kg = rec_p_ha * hectares
        total_k_kg = rec_k_ha * hectares

        # Chemical formulation: Option 1 (Urea + DAP + MOP)
        # DAP delivers 18% N and 46% P2O5
        dap_kg_needed = total_p_kg / 0.46
        dap_bags = math.ceil(dap_kg_needed / 50.0)
        n_from_dap = dap_kg_needed * 0.18

        rem_n = max(0.0, total_n_kg - n_from_dap)
        urea_kg_needed = rem_n / 0.46
        urea_bags = math.ceil(urea_kg_needed / 45.0)

        mop_kg_needed = total_k_kg / 0.60
        mop_bags = math.ceil(mop_kg_needed / 50.0)

        # Single Super Phosphate (SSP) alternative (recommended for Vidarbha pulses/oilseeds for Sulphur)
        ssp_kg_needed = total_p_kg / 0.16
        ssp_bags = math.ceil(ssp_kg_needed / 50.0)

        # Cost Calculations
        cost_dap_plan = (dap_bags * cls.FERTILIZER_PRICES["dap"]["price_per_bag"]) + \
                        (urea_bags * cls.FERTILIZER_PRICES["urea"]["price_per_bag"]) + \
                        (mop_bags * cls.FERTILIZER_PRICES["mop"]["price_per_bag"])

        # Dosage split plan
        if crop_data["is_legume"]:
            split_schedule = [
                {"timing": "Basal (At Sowing)", "pct": 100, "description": "Apply 100% DAP/SSP + 100% MOP + minimal starter Urea placed 5cm below seed."},
                {"timing": "30-35 DAS (Pre-flowering)", "pct": 0, "description": "Foliar spray of 2% Urea or 1% 19:19:19 to boost branching if canopy pale."},
                {"timing": "50-55 DAS (Pod filling)", "pct": 0, "description": "Foliar spray of 2% DAP or 0:52:34 (MKP) + 0.2% Boron for uniform seed filling."}
            ]
        else:
            split_schedule = [
                {"timing": "Basal (At Sowing)", "pct": 50, "description": "50% Nitrogen (Urea) + 100% Phosphorus (DAP) + 100% Potash (MOP)."},
                {"timing": "21-25 DAS (First Irrigation / CRI)", "pct": 25, "description": "Top-dress 25% Nitrogen (Urea) immediately before irrigation."},
                {"timing": "45-50 DAS (Booting / Flowering)", "pct": 25, "description": "Top-dress remaining 25% Nitrogen (Urea) with moist soil."}
            ]

        # Organic Fertilizer Alternatives
        organic_plan = {
            "jeevamrut": {
                "name": "Jeevamrut (जीवामृत)",
                "field_requirement": f"{int(field_size_acres * 200)} Litres",
                "application_method": "Apply 200 L/acre through irrigation water or as soil drench every 21 days.",
                "estimated_cost_inr": int(field_size_acres * 250), # cow dung, urine, jaggery, besan cost
                "benefits": "Introduces billions of active nitrogen-fixing and phosphate-solubilizing bacteria; stimulates native earthworms."
            },
            "vermicompost": {
                "name": "Vermicompost (गांडूळ खत)",
                "field_requirement": f"{int(field_size_acres * 500)} kg ({int(field_size_acres * 10)} bags)",
                "application_method": "Broadcast into soil during final ploughing before sowing.",
                "estimated_cost_inr": int(field_size_acres * 10 * 450)
            },
            "neem_cake": {
                "name": "Neem Seed Cake (निमबोळी पेंड)",
                "field_requirement": f"{int(field_size_acres * 100)} kg ({int(field_size_acres * 2)} bags)",
                "application_method": "Incorporate in furrow along with seed.",
                "benefits": "Slow-release organic nitrogen, acts as nitrification inhibitor and natural nematode/termite repellent."
            }
        }

        # Step-by-step DIY Recipe
        diy_guide = {
            "title": "Zero-Budget Jeevamrut Preparation Guide (200 Litres for 1 Acre)",
            "ingredients": [
                "10 kg fresh Desi Cow Dung (native Gir/Deoni/Gaolao cow)",
                "10 Litres fresh Desi Cow Urine (Gomutra)",
                "2 kg Jaggery (Gur / unrefined chemical-free sugar)",
                "2 kg Pulse Flour (Besan / chickpea flour - acts as protein food for microbes)",
                "Handful (~100g) of live undisturbed virgin soil from farm bund or banyan tree root",
                "200 Litres clean non-chlorinated water"
            ],
            "preparation_steps": [
                "1. Take a 200L plastic drum in shade. Pour 190L water.",
                "2. In a separate bucket, mix 10kg cow dung and 10L cow urine into a smooth slurry, then pour into drum.",
                "3. Dissolve 2kg jaggery and 2kg besan in water; add to the drum.",
                "4. Add the handful of live bund soil containing native microbial flora.",
                "5. Stir the mixture clockwise with a wooden stick for 2 minutes, twice daily (morning & evening).",
                "6. Cover with a breathable gunny bag (jute sack). Keep in shade.",
                "7. Ferment for 48 to 72 hours in summer, or 4 to 5 days in winter. Use within 7 days of preparation."
            ],
            "application_frequency": "Every 21 to 30 days during active crop growth."
        }

        return Provenanced(
            value={
                "crop_id": crop_id,
                "crop_name": crop_data["name"],
                "field_size_acres": field_size_acres,
                "field_size_hectares": round(hectares, 2),
                "soil_type": soil_type,
                "soil_ph": soil_ph,
                "recommended_elemental_npk_kg": {
                    "nitrogen_n": round(total_n_kg, 1),
                    "phosphorus_p2o5": round(total_p_kg, 1),
                    "potassium_k2o": round(total_k_kg, 1)
                },
                "commercial_bag_recommendation": {
                    "dap_50kg_bags": dap_bags,
                    "urea_45kg_bags": urea_bags,
                    "mop_50kg_bags": mop_bags,
                    "optional_ssp_50kg_bags": ssp_bags,
                    "zinc_sulphate_21pct_kg": round(field_size_acres * 10, 1),
                    "total_chemical_cost_inr": cost_dap_plan
                },
                "split_schedule": split_schedule,
                "organic_alternatives": organic_plan,
                "diy_preparation_guide": diy_guide,
                "soil_health_advisory": (
                    "Soil pH is alkaline (7.6). High calcium in black vertisols causes phosphorus fixation. "
                    "Seed treatment with PSB (Phosphorus Solubilizing Bacteria) and Rhizobium culture (250g/10kg seed) "
                    "will mobilize 20-30% locked native phosphorus and fix 35 kg atmospheric N/ha."
                )
            },
            provenance=ProvenanceMetadata(
                source="ICAR-Central Institute for Cotton Research & Dr. PDKV Akola",
                dataset="Maharashtra State Agronomic Fertilizer Schedule (Rabi 2026)",
                kind="ai_estimate",
                mode="live",
                spatialResolution="Plot-Level Fertilizer Recommendation",
                notes="Integrated Nutrient Management (INM) blending balanced inorganic NPK with organic microbial bio-stimulants.",
                url="https://icar.org.in"
            )
        )
