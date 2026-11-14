import math
from typing import Dict, Any

class AgriCalculators:
    """
    S4 — Money calculators library (pure functions, unit-tested)
    """

    @staticmethod
    def calculate_net_mandi_realization(
        gross_mandi_price_q: float,
        distance_km: float,
        freight_rate_per_km_q: float = 2.5,
        loading_unloading_q: float = 25.0,
        mandi_cess_pct: float = 1.05,
        expected_spoilage_pct: float = 0.5
    ) -> Dict[str, Any]:
        """
        M16 — Net price realized per quintal across mandis after all logistics costs.
        """
        transport_cost = distance_km * freight_rate_per_km_q
        cess_cost = gross_mandi_price_q * (mandi_cess_pct / 100.0)
        spoilage_cost = gross_mandi_price_q * (expected_spoilage_pct / 100.0)
        
        total_deductions = transport_cost + loading_unloading_q + cess_cost + spoilage_cost
        net_realized_price = gross_mandi_price_q - total_deductions

        return {
            "gross_mandi_price": round(gross_mandi_price_q, 2),
            "distance_km": distance_km,
            "transport_cost": round(transport_cost, 2),
            "handling_cost": round(loading_unloading_q, 2),
            "cess_and_taxes": round(cess_cost, 2),
            "spoilage_allowance": round(spoilage_cost, 2),
            "total_deductions_q": round(total_deductions, 2),
            "net_realized_price_q": round(net_realized_price, 2)
        }

    @staticmethod
    def calculate_store_vs_sell(
        current_mandi_price_q: float,
        storage_months: int,
        monthly_storage_rent_q: float = 35.0,
        monthly_interest_rate_pct: float = 0.8, # typical bank pledge loan / opportunity cost
        shrinkage_weight_loss_pct: float = 2.0,
        loading_handling_q: float = 20.0
    ) -> Dict[str, Any]:
        """
        M15 — Deterministic break-even future price for cold storage / warehouse:
        P_f = (P_now + storage + handling + interest) / (1 - shrinkage)
        """
        storage_cost = storage_months * monthly_storage_rent_q
        interest_cost = current_mandi_price_q * (monthly_interest_rate_pct / 100.0) * storage_months
        total_carrying_cost = storage_cost + loading_handling_q + interest_cost

        # Shrinkage fraction
        shrinkage_factor = 1.0 - (shrinkage_weight_loss_pct / 100.0)
        
        breakeven_future_price = (current_mandi_price_q + total_carrying_cost) / max(0.01, shrinkage_factor)
        required_price_rise = breakeven_future_price - current_mandi_price_q
        required_pct_rise = (required_price_rise / current_mandi_price_q) * 100.0

        return {
            "current_price_q": current_mandi_price_q,
            "storage_months": storage_months,
            "total_storage_rent": round(storage_cost, 2),
            "total_interest_cost": round(interest_cost, 2),
            "handling_cost": round(loading_handling_q, 2),
            "shrinkage_loss_pct": shrinkage_weight_loss_pct,
            "breakeven_future_price_q": round(breakeven_future_price, 2),
            "required_price_rise_inr": round(required_price_rise, 2),
            "required_price_rise_pct": round(required_pct_rise, 2)
        }

    @staticmethod
    def calculate_fragmentation_index(parcel_areas_ha: list) -> Dict[str, Any]:
        """
        M10 — Simpson-style land fragmentation index: 1 - sum(a_i / A)^2
        """
        if not parcel_areas_ha or sum(parcel_areas_ha) == 0:
            return {"index": 0.0, "classification": "Single Parcel"}

        total_area = sum(parcel_areas_ha)
        simpson_sum = sum((a / total_area) ** 2 for a in parcel_areas_ha)
        frag_index = 1.0 - simpson_sum

        classification = "Low Fragmentation"
        if frag_index > 0.65:
            classification = "Severe Fragmentation (High Logistics Burden)"
        elif frag_index > 0.4:
            classification = "Moderate Fragmentation"

        return {
            "num_parcels": len(parcel_areas_ha),
            "total_area_ha": round(total_area, 2),
            "fragmentation_index": round(frag_index, 3),
            "classification": classification
        }
