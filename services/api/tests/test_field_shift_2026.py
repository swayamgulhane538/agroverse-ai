import pytest
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)


def test_nasa_earth_observation_dashboard():
    """Verify all 8 authentic NASA Earth Observation missions are present with provenance."""
    resp = client.get("/v1/nasa/dashboard?lat=21.1458&lon=79.0882")
    assert resp.status_code == 200
    data = resp.json()
    assert "value" in data
    assert "provenance" in data

    val = data["value"]
    telemetry = val["telemetry"]
    
    # 8 NASA Datasets
    assert "smap" in telemetry
    assert "gpm" in telemetry
    assert "power" in telemetry
    assert "landsat" in telemetry
    assert "modis" in telemetry
    assert "ecostress" in telemetry
    assert "grace" in telemetry
    assert "srtm" in telemetry

    # Verify metadata fields
    for k in ["smap", "gpm", "power", "landsat", "modis", "ecostress", "grace", "srtm"]:
        item = telemetry[k]
        assert "dataset_name" in item
        assert "source" in item
        assert "spatial_resolution" in item
        assert "status" in item
        assert "update_frequency" in item

    # Specific telemetry values
    assert telemetry["smap"]["rootzone_sm_0_100cm_m3_m3"] > 0
    assert telemetry["gpm"]["monsoon_anomaly_pct"] == 4.2
    assert telemetry["ecostress"]["evaporative_stress_index_esi"] == 0.73
    assert telemetry["srtm"]["elevation_m_msl"] == 314.0


def test_crop_rotation_comparison_post_and_get():
    """Verify Smart Crop Rotation Engine generates 3 strategies with Explainable AI (XAI)."""
    payload = {
        "current_crop": "soybean",
        "previous_crop": "cotton",
        "soil_type": "black_cotton",
        "soil_ph": 7.6,
        "available_water": "limited_1_irrigation",
        "farm_size_ha": 2.5,
        "farming_season": "rabi",
        "farmer_priorities": ["soil_health", "water_saving"]
    }
    resp = client.post("/v1/rotation/compare", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    val = data["value"]

    assert "strategies" in val
    assert "strategy_a" in val["strategies"]
    assert "strategy_b" in val["strategies"]
    assert "strategy_c" in val["strategies"]
    assert "statutory_disclaimer" in val
    assert "guaranteed" in val["statutory_disclaimer"].lower()

    # Check XAI block on Strategy B
    strat_b = val["strategies"]["strategy_b"]
    xai = strat_b["explainable_ai"]
    assert "why_this_crop" in xai
    assert "nasa_evidence" in xai
    assert "soil_health_impact" in xai
    assert "water_impact" in xai
    assert "financial_impact" in xai
    assert "risk_analysis" in xai
    assert "information_gaps" in xai
    assert "confidence_indicator" in xai

    # Test GET endpoint
    resp_get = client.get("/v1/rotation/compare?current_crop=soybean&priorities=income,water_saving")
    assert resp_get.status_code == 200
    assert resp_get.json()["value"]["recommended_strategy_code"] in ["A", "B", "C"]


def test_organic_fertilizer_advisor():
    """Verify Organic Fertilizer Advisor generates recommendations and conventional comparison."""
    resp = client.get("/v1/fertilizer/organic?crop=chickpea&soil_type=black_cotton&acres=3.0")
    assert resp.status_code == 200
    data = resp.json()
    val = data["value"]

    assert "recommendations" in val
    rec_names = [r["name"] for r in val["recommendations"]]
    assert any("Vermicompost" in n for n in rec_names)
    assert any("Farmyard Manure" in n or "शेणखत" in n for n in rec_names)
    assert any("Biofertilizer" in n or "जैविक" in n for n in rec_names)

    # Conventional comparison matrix
    assert "comparison_matrix" in val
    assert len(val["comparison_matrix"]) >= 4

    # Scientific disclaimer
    assert "scientific_disclaimer" in val
    assert "do not instantaneously" in val["scientific_disclaimer"].lower()
