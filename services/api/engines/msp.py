import re
from datetime import datetime
from typing import Dict, Any, List, Optional
try:
    from ..data_loader import get_msp_table
    from ..models.provenance import Provenanced, ProvenanceMetadata
except (ImportError, ValueError):
    from data_loader import get_msp_table
    from models.provenance import Provenanced, ProvenanceMetadata


# Canonical Multilingual Alias Mapping for Agmarknet Commodities
COMMODITY_ALIASES: Dict[str, Dict[str, Any]] = {
    "chickpea": {
        "canonical_name": "Gram (Chickpea / Chana)",
        "hindi_name": "चना / चना दाल",
        "marathi_name": "हरभरा (चना)",
        "crop_type": "rabi",
        "aliases": [
            "chickpea", "gram", "chana", "bengal gram", "bengal gram(gram)(whole)",
            "desi chana", "kabuli chana", "चना", "हरभरा", "गावरान हरभरा"
        ]
    },
    "wheat": {
        "canonical_name": "Wheat",
        "hindi_name": "गेहूं",
        "marathi_name": "गहू",
        "crop_type": "rabi",
        "aliases": [
            "wheat", "gehun", "gahu", "lokwan", "sharbati", "गेहूं", "गहू",
            "dara wheat", "wheat(husked)"
        ]
    },
    "soybean": {
        "canonical_name": "Soybean (Yellow)",
        "hindi_name": "सोयाबीन (पीला)",
        "marathi_name": "सोयाबीन",
        "crop_type": "kharif",
        "aliases": [
            "soybean", "soyabean", "yellow soybean", "soya", "सोयाबीन"
        ]
    },
    "cotton": {
        "canonical_name": "Cotton (Medium Staple)",
        "hindi_name": "कपास",
        "marathi_name": "कापूस",
        "crop_type": "kharif",
        "aliases": [
            "cotton", "kapas", "raw cotton", "cotton(unginned)", "कपास", "कापूस"
        ]
    },
    "tur": {
        "canonical_name": "Tur / Arhar (Pigeon Pea)",
        "hindi_name": "अरहर / तूर",
        "marathi_name": "तूर",
        "crop_type": "kharif",
        "aliases": [
            "tur", "arhar", "pigeon pea", "red gram", "अरहर", "तूर"
        ]
    },
    "safflower": {
        "canonical_name": "Safflower (Kardi)",
        "hindi_name": "कुसुम",
        "marathi_name": "करडई",
        "crop_type": "rabi",
        "aliases": [
            "safflower", "kardi", "kusum", "करडई", "कुसुम"
        ]
    },
    "mustard": {
        "canonical_name": "Mustard / Rapeseed",
        "hindi_name": "सरसों / राई",
        "marathi_name": "मोहरी",
        "crop_type": "rabi",
        "aliases": [
            "mustard", "sarson", "rai", "rapeseed", "toria", "मोहरी", "सरसों"
        ]
    },
    "maize": {
        "canonical_name": "Maize (Corn)",
        "hindi_name": "मक्का",
        "marathi_name": "मका",
        "crop_type": "kharif",
        "aliases": [
            "maize", "corn", "makka", "maka", "मक्का", "मका"
        ]
    }
}


class MSPEngine:
    """
    Verified Minimum Support Price (MSP) Intelligence Engine.
    Auto-picks marketing season based on agronomic cycle (RMS vs KMS),
    verifies against CCEA/PIB gazette benchmarks, and computes neutral
    gap analysis with PM-AASHA procurement explanations.
    """

    @classmethod
    def normalize_commodity_name(cls, raw_query: str) -> str:
        """
        Normalizes any commodity query, Hindi/Marathi name, or Agmarknet string
        to its canonical commodity_id (e.g. 'bengal gram(gram)(whole)' -> 'chickpea').
        """
        if not raw_query:
            return "chickpea"
        clean = raw_query.strip().lower()

        for comm_id, details in COMMODITY_ALIASES.items():
            if comm_id == clean:
                return comm_id
            if details["canonical_name"].lower() == clean:
                return comm_id
            for alias in details.get("aliases", []):
                if alias in clean or clean in alias:
                    return comm_id

        # Return sanitized fallback identifier
        return re.sub(r'[^a-z0-9_]', '_', clean)

    @classmethod
    def get_commodity_metadata(cls, comm_id: str) -> Dict[str, Any]:
        """Returns multilingual names and crop season type for a canonical commodity_id."""
        normalized = cls.normalize_commodity_name(comm_id)
        if normalized in COMMODITY_ALIASES:
            meta = COMMODITY_ALIASES[normalized]
            return {
                "commodity_id": normalized,
                "canonical_name": meta["canonical_name"],
                "hindi_name": meta["hindi_name"],
                "marathi_name": meta["marathi_name"],
                "crop_type": meta["crop_type"]
            }
        return {
            "commodity_id": comm_id,
            "canonical_name": comm_id.replace('_', ' ').title(),
            "hindi_name": comm_id,
            "marathi_name": comm_id,
            "crop_type": "unknown"
        }

    @classmethod
    def auto_pick_marketing_season(
        cls,
        crop_type: str,
        reference_date_str: str = "2026-11-15"
    ) -> str:
        """
        Auto-picks official marketing season:
        - Rabi crop being sown in Oct-Dec 2026 is marketed in 2027 -> RMS 2027-28.
        - Kharif crop being harvested/sold in Oct-Dec 2026 -> KMS 2026-27.
        """
        try:
            ref_dt = datetime.strptime(reference_date_str, "%Y-%m-%d")
        except ValueError:
            ref_dt = datetime(2026, 11, 15)

        year = ref_dt.year
        month = ref_dt.month

        if crop_type == "rabi":
            # Rabi sowing happens Sep-Dec of year Y; marketing season is RMS (Y+1)-(Y+2)
            # When sown in Nov 2026, marketed in 2027 -> RMS 2027-28
            if month >= 9:
                return f"RMS {year + 1}-{str(year + 2)[-2:]}"
            else:
                return f"RMS {year}-{str(year + 1)[-2:]}"
        elif crop_type == "kharif":
            # Kharif sowing happens Jun-Jul; marketing starts Oct of year Y -> KMS Y-(Y+1)
            return f"KMS {year}-{str(year + 1)[-2:]}"
        else:
            return f"RMS {year + 1}-{str(year + 2)[-2:]}"

    @classmethod
    def get_msp_for_commodity(
        cls,
        commodity_query: str,
        marketing_season: Optional[str] = None,
        reference_date_str: str = "2026-11-15"
    ) -> Dict[str, Any]:
        """
        Retrieves official CCEA verified MSP from versioned msp_table.
        If no marketing_season is supplied, auto-picks according to the crop cycle.
        Returns status 'verified' with source URL, or 'unverified' if missing.
        """
        comm_id = cls.normalize_commodity_name(commodity_query)
        meta = cls.get_commodity_metadata(comm_id)
        crop_type = meta.get("crop_type", "rabi")

        if not marketing_season:
            marketing_season = cls.auto_pick_marketing_season(crop_type, reference_date_str)

        msp_table = get_msp_table()
        matched_entry = next((item for item in msp_table if item.get("commodity_id") == comm_id), None)

        if matched_entry:
            seasons_dict = matched_entry.get("seasons", {})
            if marketing_season in seasons_dict:
                season_data = seasons_dict[marketing_season]
                return {
                    "commodity_id": comm_id,
                    "commodity_name": matched_entry.get("commodity_name", meta["canonical_name"]),
                    "hindi_name": matched_entry.get("hindi_name", meta["hindi_name"]),
                    "marathi_name": matched_entry.get("marathi_name", meta["marathi_name"]),
                    "crop_type": crop_type,
                    "marketing_season": marketing_season,
                    "msp_inr_quintal": season_data["msp_inr_quintal"],
                    "effective_date": season_data.get("effective_date"),
                    "retrieved_date": season_data.get("retrieved_date"),
                    "status": "verified",
                    "source": season_data.get("source", "CCEA / PIB Gazette"),
                    "source_url": season_data.get("source_url", "https://pib.gov.in")
                }
            elif matched_entry.get("default_active_season") in seasons_dict:
                fallback_season = matched_entry.get("default_active_season")
                season_data = seasons_dict[fallback_season]
                return {
                    "commodity_id": comm_id,
                    "commodity_name": matched_entry.get("commodity_name", meta["canonical_name"]),
                    "hindi_name": matched_entry.get("hindi_name", meta["hindi_name"]),
                    "marathi_name": matched_entry.get("marathi_name", meta["marathi_name"]),
                    "crop_type": crop_type,
                    "marketing_season": fallback_season,
                    "msp_inr_quintal": season_data["msp_inr_quintal"],
                    "effective_date": season_data.get("effective_date"),
                    "retrieved_date": season_data.get("retrieved_date"),
                    "status": "verified",
                    "source": season_data.get("source", "CCEA / PIB Gazette"),
                    "source_url": season_data.get("source_url", "https://pib.gov.in")
                }

        # Unverified fallback
        return {
            "commodity_id": comm_id,
            "commodity_name": meta["canonical_name"],
            "hindi_name": meta["hindi_name"],
            "marathi_name": meta["marathi_name"],
            "crop_type": crop_type,
            "marketing_season": marketing_season,
            "msp_inr_quintal": None,
            "effective_date": None,
            "retrieved_date": None,
            "status": "unverified",
            "source": "Government Gazette",
            "source_url": None,
            "notes": "MSP not verified for this crop and season. Check official CACP notifications."
        }

    @classmethod
    def calculate_msp_gap(
        cls,
        modal_price: float,
        msp_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Computes gap between market modal price and MSP.
        Provides a neutral, factual explanation if price is below MSP.
        """
        msp_val = msp_data.get("msp_inr_quintal")
        season_label = msp_data.get("marketing_season", "Current Season")

        if msp_val is None or msp_data.get("status") != "verified":
            return {
                "has_msp": False,
                "msp_inr_quintal": None,
                "marketing_season": season_label,
                "gap_inr": None,
                "gap_pct": None,
                "status_badge": "MSP Not Verified",
                "badge_color": "gray",
                "explanation": "Official MSP benchmark is not verified for this specific commodity/variety. Displaying raw open market mandi rates."
            }

        diff = float(modal_price) - float(msp_val)
        pct = (diff / float(msp_val)) * 100.0

        if diff >= 0:
            badge_text = f"+₹{int(diff)}/Q Above MSP (+{pct:.1f}%)" if diff > 0 else "At MSP Benchmark"
            badge_color = "emerald"
            explanation = (
                f"Trading above the official {season_label} MSP benchmark (₹{msp_val:,}/Q). "
                "Open market commercial demand currently outpaces the statutory floor price."
            )
        else:
            badge_text = f"-₹{abs(int(diff))}/Q Below MSP ({pct:.1f}%)"
            badge_color = "amber"
            explanation = (
                f"Modal price is ₹{abs(int(diff))}/Q below the {season_label} MSP (₹{msp_val:,}/Q). "
                "Note: MSP is an assured government floor price; commercial APMC transactions fluctuate based on "
                "daily arrival volume, grain moisture, and FAQ quality standards. Registered farmers can avail "
                "direct procurement through state nodal purchase centers (NAFED / FCI / PM-AASHA)."
            )

        return {
            "has_msp": True,
            "msp_inr_quintal": msp_val,
            "marketing_season": season_label,
            "source": msp_data.get("source"),
            "source_url": msp_data.get("source_url"),
            "gap_inr": round(diff, 2),
            "gap_pct": round(pct, 1),
            "is_above_msp": diff >= 0,
            "status_badge": badge_text,
            "badge_color": badge_color,
            "explanation": explanation
        }
