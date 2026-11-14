# AGROVERSE AI 🌾🚀
### Healthy Soil. Smarter Farming. Stronger Future.

> **NASA Space Apps Challenge 2026** — *Challenge: Field Shift: Adapting Farms with NASA Data*  
> **Demo Location:** Nagpur, Maharashtra, India (21.1458° N, 79.0882° E), Vidarbha region.  
> **Target Season:** Rabi 2026–27 (Transitioning from Kharif Soybean/Cotton).

---

## 🌟 Overview
**AGROVERSE AI** is an explainable, decision-support platform designed for Indian smallholder farmers. It turns **NASA Earth Observation data** (POWER, SMAP, GPM IMERG, Landsat/HLS) and **Official Indian Mandi rates** (AGMARKNET via data.gov.in) into actionable decisions:
- **Climate Context:** Hyper-local historical precipitation, dry spells, and SMAP root-zone soil moisture percentiles.
- **Explainable Crop Rotation (M2):** Multi-criteria agronomic scoring engine for Kharif/Rabi transition.
- **Farmer Income Optimizer (M7):** Transparent production cost, revenue, and B:C ratio calculations.
- **FAO-56 Farm Climate Simulator:** What-if scenarios (-40% to +40% rainfall, +0°C to +4°C heat shock) with crop coefficient equations.
- **Multi-Parcel Cadastral Studio (M10):** Polygon parcel management by Gat and Survey numbers with NDVI honouring mixed-pixel warnings.
- **Mandi Logistics & Net Realisation (M16):** Freight, loading labor, and market cess deductions across Vidarbha APMCs.
- **Cold Storage Store-vs-Sell (M15):** Carrying costs, interest subvention, and break-even rally price calculator.
- **Govt Schemes Engine (S1):** Eligibility matching with official portals (PM-KISAN, Magel Tyala Shet-Tale, PM-KUSUM).
- **Disease Detection+ (M17):** Edge-calibrated foliar diagnostic with responsible IPM-first organic remedies.
- **Provenance on Everything (`Provenanced<T>`):** Every number shows source, observation date, fetch time, and resolution.

---

## 🏗️ Architecture & Technology Stack
- **Frontend / Web & Mobile:** HTML5, Tailwind CSS, Chart.js, FontAwesome, SVG Cadastral Polygons, Floating Bottom Pill Navigation.
- **Backend Services:** Python 3.11+, FastAPI, Pydantic v2, Uvicorn.
- **Test Coverage:** Automated unit test suite (`unittest`) verifying S4 calculators, crop calendar, and scheme matching.
- **Documentation & Judging Deliverables:**
  - `docs/ARCHITECTURE.md`: Microservices topology & data flow.
  - `docs/DATA_SOURCES.md`: NASA satellite data adapters & APMC schemas.
  - `docs/MODEL_CARD.md`: Plant Disease Detection+ AI model card and responsible AI evaluation.
  - `docs/DEMO_SCRIPT.md`: 3-minute hackathon pitch script for Nagpur Space Apps judges.
  - `docs/HONESTY_REPORT.md`: Live vs Cached vs Demo data integrity breakdown.

---

## 👤 Developer Details
- **Solo Lead Developer:** Swayam Gulhane (`@swayamgulhane538`)
- **Institution / Location:** Nagpur, Maharashtra, India
- **Hackathon:** NASA Space Apps Challenge Nagpur 2026

---

## 🤖 AI Usage Disclosure
In accordance with NASA Space Apps Challenge 2026 guidelines:
- **AI Tools Used:** Antigravity AI Mentor (Gemini).
- **Assisted Areas:** Architecture brainstorming, structuring standardized folders, scaffolding FastAPI adapters, and remote-sensing equations.
- **Human Work & Independence:** Solo developer Swayam Gulhane independently reviewed, tested, configured environment keys, executed unit test suites, verified remote endpoints against real Nagpur coordinates, and performed all git commits and pushes from his local machine.

---

## 🚀 Quickstart

### 1. Launch Interactive Dashboard
Open `index.html` directly in any modern browser (or view `agroverse_live_preview.html`).

### 2. Run Backend API & Test Suite
```bash
# Run unit tests
python -m unittest services/api/tests/test_engines.py

# Launch FastAPI microservice
uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger Documentation available at: `http://localhost:8000/docs`
