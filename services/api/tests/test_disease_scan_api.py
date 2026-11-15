import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
import disease_scan_api as m

app = FastAPI()
app.include_router(m.router)
client = TestClient(app)
JPEG = b"\xff\xd8\xff\xe0" + b"0" * 200

def post(image=JPEG, name="leaf.jpg", ctype="image/jpeg", crop="chana", lang="en", answers=""):
    return client.post("/v1/disease/scan", files={"image": (name, image, ctype)},
                       data={"crop": crop, "language": lang, "answers": answers})

def fake(payload):
    async def _f(*a, **k):
        return payload if isinstance(payload, str) else json.dumps(payload)
    return _f

GOOD = {
  "is_plant": True, "crop_seen": "chickpea", "image_quality_ok": True, "image_quality_issues": [],
  "overall_certainty": "possible",
  "what_is_happening": "Leaves show small holes and chewed edges.",
  "possible_issues": [
    {"id": "pod_borer", "name": "Gram pod borer", "kind": "disease", "likelihood": "medium",
     "evidence_seen": ["holes in leaves", "spray emamectin benzoate 5% SG @ 4g per litre"], "evidence_missing": ["larvae not visible"]},
    {"id": "made_up_id", "name": "X", "kind": "disease", "likelihood": "high"}],
  "follow_up_questions": ["Are there holes in the pods?"],
  "safe_next_steps": ["Check 10 plants for larvae", "Spray chlorantraniliprole 3 ml per litre", "Remove badly damaged plants"],
  "see_expert_if": ["Many larvae per plant"]}

def test_not_configured(monkeypatch):
    monkeypatch.delenv("VISION_API_KEY", raising=False); monkeypatch.delenv("VISION_MODEL", raising=False)
    r = post(); assert r.status_code == 503 and r.json()["error"]["code"] == "VISION_NOT_CONFIGURED"

def test_empty_and_bad_type_and_large():
    assert post(image=b"").status_code == 400
    assert post(image=b"hello world not an image").json()["error"]["code"] == "BAD_IMAGE_TYPE"
    assert post(image=JPEG + b"0" * (5 * 1024 * 1024)).status_code == 413

def test_good_result_sanitised(monkeypatch):
    monkeypatch.setattr(m, "call_vision_model", fake(GOOD))
    r = post(); assert r.status_code == 200
    res = r.json()["result"]
    ids = [i["id"] for i in res["possible_issues"]]
    assert ids == ["pod_borer"]                                   # made-up id dropped
    assert res["possible_issues"][0]["kind"] == "insect_pest"     # kind from our list, not the model
    assert res["possible_issues"][0]["evidence_seen"] == ["holes in leaves"]  # dose line removed
    assert "Spray chlorantraniliprole 3 ml per litre" not in res["safe_next_steps"]
    assert len(res["safe_next_steps"]) == 2
    assert "confidence" not in json.dumps(r.json()).lower()       # no fake percentage
    assert r.json()["provenance"]["kind"] == "ai_estimate"

def test_json_in_code_fence_and_retry(monkeypatch):
    calls = {"n": 0}
    async def flaky(*a, **k):
        calls["n"] += 1
        return "not json at all" if calls["n"] == 1 else "```json\n" + json.dumps(GOOD) + "\n```"
    monkeypatch.setattr(m, "call_vision_model", flaky)
    r = post(); assert r.status_code == 200 and calls["n"] == 2

def test_bad_output_twice(monkeypatch):
    monkeypatch.setattr(m, "call_vision_model", fake("garbage"))
    r = post(); assert r.status_code == 502 and r.json()["error"]["code"] == "BAD_MODEL_OUTPUT"

def test_not_a_plant_forced(monkeypatch):
    bad = dict(GOOD, is_plant=False, overall_certainty="likely")
    monkeypatch.setattr(m, "call_vision_model", fake(bad))
    res = post().json()["result"]
    assert res["overall_certainty"] == "not_a_plant" and res["possible_issues"] == []

def test_likely_without_issue_downgraded(monkeypatch):
    bad = dict(GOOD, overall_certainty="likely", possible_issues=[{"id": "zzz", "likelihood": "high"}])
    monkeypatch.setattr(m, "call_vision_model", fake(bad))
    assert post().json()["result"]["overall_certainty"] == "uncertain"

def test_upstream_error(monkeypatch):
    async def boom(*a, **k): raise m.VisionUpstreamError("model API returned 500")
    monkeypatch.setattr(m, "call_vision_model", boom)
    assert post().status_code == 502

def test_crop_alias_and_language_fallback(monkeypatch):
    seen = {}
    async def spy(img, mt, system, user_text):
        seen["t"] = user_text; return json.dumps(GOOD)
    monkeypatch.setattr(m, "call_vision_model", spy)
    r = post(crop="kapas", lang="xx"); assert r.json()["crop_selected"] == "cotton" and r.json()["language"] == "en"
    assert "pink_bollworm" in seen["t"] and "pod_borer" not in seen["t"]
