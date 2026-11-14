# AGROVERSE AI — NASA Space Apps Challenge 2026 Submission

## 1. Project Title & Tagline
- **Project Title:** AGROVERSE AI
- **Tagline:** Healthy Soil. Smarter Farming. Stronger Future.
- **Challenge:** *Field Shift: Adapting Farms with NASA Data*
- **Local Event:** NASA Space Apps Challenge Nagpur 2026
- **Solo Lead Developer:** Swayam Gulhane (`@swayamgulhane538`)

---

## 2. Short Project Summary (For Judges & Portal Card)
> **AGROVERSE AI** is an explainable agricultural intelligence platform that adapts smallholder farms in Vidarbha, Maharashtra using NASA Earth Observation data. Transitioning from Kharif cotton/soybean into Rabi sowing, smallholders face severe dry spells, terminal heat, and distress sales. AGROVERSE AI combines NASA POWER (temperature & solar radiation), NASA SMAP (root-zone soil moisture percentiles), and NASA GPM IMERG (precipitation risk) with official Kalamna APMC Mandi rates and CACP MSP benchmarks. With an Apple-minimalist Cadastral Parcel Map Studio (Module 10), FAO-56 Climate Stress Simulator, Net Mandi Logistics Planner (Module 16), Cold Storage Calculator (Module 15), Government Schemes Engine (Service S1), and IPM-First Disease Detection+ (Module 17), every single number is backed by a strict Provenance & Trust Layer (`Provenanced<T>`).

---

## 3. NASA Data & Earth Observation Assets Used
1. **NASA POWER (Prediction of Worldwide Energy Resources):**
   - *Parameters:* T2M (2m Air Temperature), PRECTOTCORR (Precipitation), ALLSKY_SFC_SW_DWN (Solar Radiation), Growing Degree Days (GDD).
   - *Use Case:* Thermal degree days and terminal heat shock modeling for Rabi Wheat vs Chickpea.
2. **NASA SMAP (Soil Moisture Active Passive):**
   - *Parameters:* SPL4SMGP (Surface & Root-Zone Soil Moisture Percentiles).
   - *Use Case:* Regional residual soil moisture ranking to determine sowing viability without irrigation.
3. **NASA GPM IMERG (Global Precipitation Measurement):**
   - *Parameters:* Precipitation calibrated estimates & historical dry-spell frequency distributions.
   - *Use Case:* 20-year probabilistic rainfall risk modeling (Module 11) for winter dry spells exceeding 21 days.
4. **NASA Landsat / Harmonized Landsat-Sentinel (HLS):**
   - *Parameters:* 30m multispectral surface reflectance & NDVI.
   - *Use Case:* Parcel vegetative vigour histograms and stand/gap health scouting.

---

## 4. How It Solves the Challenge (*Field Shift: Adapting Farms with NASA Data*)
- **Adapts Sowing to Climate Reality:** Instead of planting water-intensive wheat on depleted soil, our Crop Rotation Engine (Module 2) triggers Chickpea sowing based on SMAP 62nd percentile residual moisture, saving 170 mm of irrigation water and fixing +35 kg/ha of natural soil nitrogen.
- **Protects Farmer Economics:** Integrates official Agmarknet Kalamna APMC rates and CACP MSP 2026 data. Our Net Logistics Planner (Module 16) calculates true pocket realization after freight and cess, while our Store-vs-Sell Calculator (Module 15) calculates carrying costs to prevent distress harvest sales.
- **Maintains Zero Hallucination & Transparency:** Implements the `Provenanced<T>` schema on every metric, showing data source, observation date, fetch time, and spatial resolution chip.

---

## 5. Live Links & Repositories
- **GitHub Repository:** [https://github.com/swayamgulhane538/agroverse-ai](https://github.com/swayamgulhane538/agroverse-ai)
- **Live Hosted Web App (GitHub Pages):** [https://swayamgulhane538.github.io/agroverse-ai/](https://swayamgulhane538.github.io/agroverse-ai/)
- **Local Interactive App (On Local Server):** `http://localhost:3000` (or `http://10.24.203.230:3000` on Mobile Wi-Fi)
- **API Documentation (Swagger UI):** `http://localhost:8000/docs`
- **Release Version:** `v1.0.0-final`
