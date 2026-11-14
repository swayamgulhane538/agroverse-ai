# AGROVERSE AI 🌾🚀
### Healthy Soil. Smarter Farming. Stronger Future.

> **NASA Space Apps Challenge 2026** — *Challenge: Field Shift: Adapting Farms with NASA Data*  
> **Demo Location:** Nagpur, Maharashtra, India (21.1458° N, 79.0882° E), Vidarbha region.  
> **Target Season:** Rabi 2026–27 (Transitioning from Kharif Soybean/Cotton).

---

## 🌟 Overview
**AGROVERSE AI** is an explainable, decision-support platform designed for Indian farmers. It turns **NASA Earth Observation data** (POWER, SMAP, GPM IMERG, Landsat/HLS) and **Official Indian Mandi rates** (AGMARKNET via data.gov.in) into actionable insights:
- **Climate Context:** Hyper-local historical precipitation, dry spells, and soil moisture percentiles.
- **Explainable Crop Rotation:** Multi-criteria weighted scoring engine for Kharif/Rabi transition.
- **Farmer Income Optimizer:** Cost-benefit and sensitivity analysis with transparent formulas.
- **AI Farm Simulator:** Transparent what-if scenarios (e.g. -20% rainfall, +2°C temperature shift) using FAO-56 crop coefficient equations.
- **Data Provenance on Everything:** Every single number shows its source, observation date, fetch time, and resolution chip.

---

## 🏗️ Architecture & Technology Stack
- **Frontend / Mobile:** React Native / Expo, TypeScript, TailwindCSS / NativeWind, Lucide Icons, SVG Charts.
- **Backend Services:** Python 3.11+, FastAPI, Pydantic v2, SQLite / PostgreSQL.
- **Data Sources:** 
  - NASA POWER (Weather & Solar Radiation)
  - NASA SMAP (Surface & Root-zone Soil Moisture)
  - NASA GPM IMERG (Satellite Rainfall)
  - AGMARKNET / data.gov.in (Indian Mandi Rates)
  - MSP (Minimum Support Price) official baseline records

---

## 👤 Developer Details
- **Solo Developer & Lead:** Swayam Gulhane (`@swayamgulhane538`)
- **Institution / Location:** Nagpur, Maharashtra, India
- **Hackathon:** NASA Space Apps Challenge Nagpur 2026


---

## 🤖 AI Usage Disclosure
In accordance with NASA Space Apps Challenge 2026 guidelines:
- **AI Tools Used:** Antigravity AI Mentor (Gemini).
- **Assisted Areas:** Brainstorming architecture, setting up standardized folder structure, drafting boilerplate FastAPI adapters, and explaining remote sensing algorithms.
- **Human Work & Independence:** All four human members independently reviewed, modified, configured environment keys, verified remote endpoints against real Nagpur coordinates, and executed commits/pushes from their local developer machines. No automated bot pushes were performed.

---

## 🚀 Quickstart

### 1. Backend Setup
```bash
cd services/api
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate
pip install -r requirements.txt
python main.py
```
Backend runs at: `http://localhost:8000` (Swagger UI: `http://localhost:8000/docs`)

### 2. Mobile / Frontend Setup
```bash
cd apps/mobile
npm install
npx expo start
```
