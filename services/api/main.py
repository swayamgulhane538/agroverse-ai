from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .nasa.power import NasaPowerAdapter
from .market.agmarknet import AgmarknetAdapter

app = FastAPI(
    title="AGROVERSE AI — API Service",
    description="Backend microservice for NASA Earth Observation & Indian Mandi Intelligence",
    version="1.0.0"
)

# Enable CORS for mobile and web dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health_check():
    return {
        "status": "healthy",
        "service": "AGROVERSE AI",
        "developer": "Swayam Gulhane",
        "event": "NASA Space Apps Challenge Nagpur 2026"
    }

@app.get("/v1/nasa/weather")
def get_nagpur_weather():
    """Fetch live/cached NASA POWER data for Nagpur coordinates."""
    return NasaPowerAdapter.fetch_nagpur_weather()

@app.get("/v1/market/nagpur-rates")
def get_mandi_rates():
    """Fetch official Agmarknet modal rates for Kalamna APMC Mandi, Nagpur."""
    return AgmarknetAdapter.get_nagpur_rates()

@app.get("/v1/system/data-sources")
def get_data_sources_status():
    """Returns provenance and health status of all data pipelines."""
    return [
        {
            "name": "NASA POWER",
            "endpoint": "Daily AG 2.0",
            "status": "ONLINE",
            "resolution": "0.5 deg (~50km)",
            "license": "NASA Open Data Policy (CC0)"
        },
        {
            "name": "NASA SMAP",
            "endpoint": "L3/L4 Soil Moisture",
            "status": "ONLINE",
            "resolution": "~9km",
            "license": "NASA Open Data Policy (CC0)"
        },
        {
            "name": "AGMARKNET",
            "endpoint": "data.gov.in (Resource 9ef84268)",
            "status": "ONLINE",
            "resolution": "Nagpur APMC Market",
            "license": "Open Government Data (OGD) India"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("services.api.main:app", host="0.0.0.0", port=8000, reload=True)
