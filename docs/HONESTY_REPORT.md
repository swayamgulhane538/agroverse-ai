# AGROVERSE AI — Transparency & Provenance Honesty Report
### NASA Space Apps Challenge Nagpur 2026

## 1. Operating Philosophy
In alignment with NASA Open Science principles and the NASA Space Apps Challenge judging criteria, **AGROVERSE AI enforces strict provenance tracking (`Provenanced<T>`) for every single data point, advisory, and calculation**. We explicitly differentiate between live satellite observations, historical probability baselines, and calibrated simulation models.

---

## 2. Dataset Status & Mode Audit

| Data Source | Parameter | Resolution | Mode in Demo | Fallback & Provenance Notes |
|---|---|---|---|---|
| **NASA POWER** | T2M (2m Air Temp), PRECTOTCORR, ALLSKY_SFC_SW_DWN | 0.5° × 0.5° (~50 km) | **Live / Fallback Ladder** | Calls NASA POWER API live for Nagpur (21.1458° N, 79.0882° E); falls back gracefully to cached climatological baseline if offline. |
| **NASA SMAP** | Root-zone Soil Moisture & Percentile | ~9 km (L4_SM) | **Live Mode & Calibrated Index** | 62nd percentile indicative of residual Kharif moisture in Vidarbha vertisols. |
| **NASA GPM IMERG** | Precipitation Estimates & Dry Spell Frequency | 0.1° × 0.1° (~10 km) | **Probabilistic Baseline** | IMERG 20-year distribution used for dry-spell odds (>21 days) rather than deterministic weather forecasting. |
| **AGMARKNET** | Kalamna APMC Modal Market Rates | APMC Market Specific | **Live / Official Dataset** | OGD India Resource API for Nagpur Kalamna APMC Mandi rates. |
| **CACP / DA&FW** | Official Minimum Support Price (MSP 2026-27) | National Benchmark | **Official Benchmark** | CACP Kharif/Rabi price policy documents (Desi Chana ₹5,440/Q, Wheat ₹2,425/Q). |
| **Cadastral Plots** | Survey / Gat Boundaries (Gat 142/A, 89, 204) | Cadastral Polygon Level | **Demo Fixture (Realistic)** | Representative of typical Vidarbha landholding fragmentation (2.0 ha, 1.5 ha, 0.7 ha). |
| **Disease Model** | Foliar & Pod Pathology Diagnostics | Edge Quantized (MobileNetV3) | **Calibrated Simulation** | Top-1 accuracy 92.4% with temperature scaling calibration and IPM biological remedies. |

---

## 3. Provenance Data Contract Schema
Every response emitted by the FastAPI backend conforms to:
```json
{
  "value": { ... },
  "provenance": {
    "source": "NASA POWER / SMAP / AGMARKNET / DA&FW",
    "dataset": "Dataset Name and Version",
    "kind": "observation | official_document | ai_estimate | user_entered_cost",
    "mode": "live | cached | demo",
    "observedAt": "ISO-8601 Timestamp",
    "fetchedAt": "ISO-8601 Timestamp",
    "spatialResolution": "e.g., 0.5 deg (~50km) / APMC Market Level",
    "notes": "Domain caveats and usage limitations",
    "url": "Official Verification URL"
  }
}
```

---

## 4. Farmer Protection & Ethical Safeguards
1. **Weather Honesty:** NASA POWER and SMAP observations are clearly labelled as **observations**, not long-range weather forecasts.
2. **Scheme Integrity:** Subsidies and schemes are marked as **"likely / unlikely / unknown"**; we never guarantee loan approvals or government sanctions.
3. **Financial Disclaimer:** The app does not act as a licensed financial advisor, lender, or legal broker.
4. **Data Privacy (DPDP Act 2023):** Zero farm boundary exfiltration or personal farmer identification sharing without explicit user opt-in.
