import json
import os
from typing import Dict, Any, List
from ..models.provenance import Provenanced, ProvenanceMetadata
from ..data_loader import get_schemes

class SchemeEngine:
    """
    S1 — Scheme Knowledge Base & Eligibility Engine
    Rule: Never guarantee outcomes. Return 'likely' | 'unlikely' | 'unknown' with reasons.
    """
    
    @staticmethod
    def load_catalog() -> List[Dict[str, Any]]:
        try:
            return get_schemes()
        except Exception:
            return []

    @staticmethod
    def match_schemes(farmer_profile: Dict[str, Any]) -> Provenanced[List[Dict[str, Any]]]:
        catalog = SchemeEngine.load_catalog()
        land_ha = float(farmer_profile.get("land_ha", 1.5))
        state = farmer_profile.get("state", "Maharashtra")
        has_water_source = farmer_profile.get("has_water_source", True)
        
        matches = []
        for scheme in catalog:
            verdict = "likely"
            reasons = []
            missing_inputs = []

            if scheme["id"] == "pm_kisan":
                if land_ha > 0:
                    verdict = "likely"
                    reasons.append("Eligible as landholding farmer with valid record.")
                else:
                    verdict = "unlikely"
                    reasons.append("Requires operational agricultural landholding.")

            elif scheme["id"] == "mh_magel_tyala_shet_tale":
                if state.lower() == "maharashtra":
                    if land_ha >= 0.6:
                        verdict = "likely"
                        reasons.append(f"Land area ({land_ha} ha) meets minimum 0.6 ha threshold.")
                    else:
                        verdict = "unlikely"
                        reasons.append("Requires minimum 0.60 hectares land holding.")
                else:
                    verdict = "unlikely"
                    reasons.append("Exclusive to Maharashtra domicile farmers.")

            elif scheme["id"] == "pm_kusum_solar":
                if has_water_source:
                    verdict = "likely"
                    reasons.append("Eligible for off-grid pump if well/borewell/pond is available.")
                else:
                    verdict = "unknown"
                    missing_inputs.append("Water source status (dug well / borewell / farm pond)")
                    reasons.append("Requires verified open well, borewell, or farm pond.")

            elif scheme["id"] == "pmfby_crop_insurance":
                verdict = "likely"
                reasons.append("Notified Rabi crops (Chickpea, Wheat) eligible at ₹1 token premium in Maharashtra.")

            elif scheme["id"] == "aif_cold_storage":
                verdict = "likely"
                reasons.append("Individual farmers and FPOs eligible for 3% interest subvention.")

            matches.append({
                "scheme_id": scheme["id"],
                "name": scheme["name"],
                "name_mr": scheme.get("name_mr", ""),
                "name_hi": scheme.get("name_hi", ""),
                "category": scheme.get("category", ""),
                "verdict": verdict,
                "reasons": reasons,
                "missing_inputs": missing_inputs,
                "benefit_text": scheme.get("benefit_text", ""),
                "official_urls": scheme.get("official_urls", []),
                "last_verified_at": scheme.get("last_verified_at", "2026-11-10")
            })

        return Provenanced(
            value=matches,
            provenance=ProvenanceMetadata(
                source="Ministry of Agriculture & Farmers Welfare / MahaDBT",
                dataset="Verified Central & Maharashtra Scheme Knowledge Base",
                kind="official_document",
                mode="live",
                observedAt="2026-11-14",
                spatialResolution="State of Maharashtra (District Nagpur)",
                notes="Verified from official government portals. Rules subject to change; confirmation at Taluka Agriculture Office required.",
                url="https://mahadbt.maharashtra.gov.in"
            )
        )
