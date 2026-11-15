"""
AGROVERSE AI - Disease Doctor backend (real photo analysis)

HOW TO USE
1) pip install fastapi httpx python-multipart pydantic
2) In your FastAPI app file:
       from disease_scan_api import router as disease_router
       app.include_router(disease_router)
3) Set environment variables (Vercel -> Project -> Settings -> Environment Variables; NEVER in frontend code):
       VISION_API_KEY   = your vision-model API key
       VISION_MODEL     = model name (verify the current name in your provider's docs)
       VISION_API_URL   = (optional) default is the Anthropic Messages API URL
   If you use Gemini/OpenAI instead, replace ONLY the function call_vision_model() below.

WHAT IT DOES
- Accepts a leaf/plant photo + crop, asks a vision model for a STRICT JSON answer, validates it,
  removes any pesticide names/doses (we never give doses from an AI), and returns an honest result:
  likely / possible / uncertain / not_a_plant / poor_image.
- No fake confidence percentage. No canned results. If the model is not configured, it says so.
"""
from __future__ import annotations

import base64
import json
import os
import re
from datetime import datetime, timezone
from typing import Literal

import httpx
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

router = APIRouter()

MAX_UPLOAD_BYTES = 4 * 1024 * 1024  # Vercel functions reject request bodies above ~4.5 MB
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
VISION_API_URL = os.getenv("VISION_API_URL", "https://api.anthropic.com/v1/messages")

# ---------------------------------------------------------------------------
# Closed-set candidates per crop (names only: no treatments/doses are stored here).
# The model must choose from these ids, which reduces made-up diagnoses.
# ---------------------------------------------------------------------------
CANDIDATES: dict[str, list[tuple[str, str, str]]] = {
    "chickpea": [
        ("pod_borer", "Gram pod borer (Helicoverpa armigera)", "insect_pest"),
        ("fusarium_wilt", "Fusarium wilt", "disease"),
        ("dry_root_rot", "Dry root rot", "disease"),
        ("ascochyta_blight", "Ascochyta blight", "disease"),
        ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
        ("water_stress", "Water/heat stress", "abiotic"),
    ],
    "cotton": [
        ("leaf_curl_virus", "Cotton leaf curl virus", "disease"),
        ("pink_bollworm", "Pink bollworm", "insect_pest"),
        ("bacterial_blight", "Bacterial blight", "disease"),
        ("sucking_pests", "Sucking pests (whitefly, aphid, jassid)", "insect_pest"),
        ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
        ("water_stress", "Water/heat stress", "abiotic"),
    ],
    "soybean": [
        ("soybean_rust", "Asian soybean rust", "disease"),
        ("yellow_mosaic", "Yellow mosaic virus", "disease"),
        ("girdle_beetle", "Girdle beetle", "insect_pest"),
        ("leaf_eating_caterpillars", "Leaf-eating caterpillars", "insect_pest"),
        ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
        ("water_stress", "Water/heat stress", "abiotic"),
    ],
    "wheat": [
        ("yellow_rust", "Yellow (stripe) rust", "disease"),
        ("leaf_rust", "Leaf (brown) rust", "disease"),
        ("leaf_blight", "Leaf blight", "disease"),
        ("aphids", "Aphids", "insect_pest"),
        ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
        ("water_stress", "Water/heat stress", "abiotic"),
    ],
    "pigeonpea": [
        ("fusarium_wilt", "Fusarium wilt", "disease"),
        ("sterility_mosaic", "Sterility mosaic", "disease"),
        ("pod_borer", "Pod borer (Helicoverpa)", "insect_pest"),
        ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
    ],
    "tomato": [
        ("early_blight", "Early blight", "disease"),
        ("late_blight", "Late blight", "disease"),
        ("leaf_curl_virus", "Tomato leaf curl virus", "disease"),
        ("fruit_borer", "Fruit borer", "insect_pest"),
        ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
    ],
    "citrus": [
        ("citrus_canker", "Citrus canker", "disease"),
        ("greening_hlb", "Citrus greening (HLB)", "disease"),
        ("leaf_miner", "Citrus leaf miner", "insect_pest"),
        ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
    ],
}
GENERIC = [
    ("unknown_disease", "Possible disease (cannot name)", "disease"),
    ("unknown_pest", "Possible insect pest (cannot name)", "insect_pest"),
    ("nutrient_deficiency", "Nutrient deficiency", "nutrient"),
    ("water_stress", "Water/heat stress", "abiotic"),
]
ALWAYS = [("healthy", "Looks healthy", "healthy"), ("other_unknown", "Other / cannot tell", "unknown")]

ALIASES = {
    "chana": "chickpea", "gram": "chickpea", "chickpea": "chickpea",
    "kapas": "cotton", "cotton": "cotton",
    "soyabean": "soybean", "soybean": "soybean",
    "gehu": "wheat", "wheat": "wheat",
    "tur": "pigeonpea", "arhar": "pigeonpea", "pigeonpea": "pigeonpea",
    "tomato": "tomato",
    "orange": "citrus", "santra": "citrus", "citrus": "citrus", "mosambi": "citrus", "lemon": "citrus",
}


def normalise_crop(crop: str) -> str:
    key = (crop or "").strip().lower()
    return ALIASES.get(key, "other")


def candidates_for(crop_key: str) -> list[tuple[str, str, str]]:
    base = CANDIDATES.get(crop_key, GENERIC)
    return list(base) + ALWAYS


# ---------------------------------------------------------------------------
# Output schema (validated). No numeric "confidence": model self-reported
# probabilities are not calibrated, so we only expose a certainty label.
# ---------------------------------------------------------------------------
class Issue(BaseModel):
    id: str
    name: str = ""
    kind: Literal["disease", "insect_pest", "nutrient", "abiotic", "healthy", "unknown"] = "unknown"
    likelihood: Literal["high", "medium", "low"] = "low"
    evidence_seen: list[str] = Field(default_factory=list)
    evidence_missing: list[str] = Field(default_factory=list)


class ScanResult(BaseModel):
    is_plant: bool
    crop_seen: str | None = None
    image_quality_ok: bool = True
    image_quality_issues: list[str] = Field(default_factory=list)
    overall_certainty: Literal["likely", "possible", "uncertain", "not_a_plant", "poor_image"]
    what_is_happening: str = ""
    possible_issues: list[Issue] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)
    safe_next_steps: list[str] = Field(default_factory=list)
    see_expert_if: list[str] = Field(default_factory=list)


LANG_NAMES = {"en": "English", "hi": "Hindi", "mr": "Marathi"}

SYSTEM_PROMPT = """You are a crop-health TRIAGE assistant for smallholder farmers in India.
You look at ONE photo and describe what is visibly happening to the plant.

Rules (strict):
- Describe only what is VISIBLE in the photo. Never invent symptoms.
- If the photo is not a plant/crop, set is_plant=false and overall_certainty="not_a_plant".
- If the photo is too blurry, dark, far away or has no affected part visible, set overall_certainty="poor_image".
- Prefer "uncertain" over guessing. Many pests (e.g. caterpillars inside pods) cannot be confirmed from a leaf photo;
  say so and suggest scouting.
- Choose possible_issues ONLY from the allowed ids given by the user (max 3, most likely first).
- NEVER mention pesticide, fungicide or insecticide product names, doses, dilutions or spray schedules.
- safe_next_steps: only non-chemical, low-risk steps (scouting, isolating/removing badly affected plants,
  field sanitation, irrigation/drainage checks, retaking photos, contacting the local KVK).
- see_expert_if: clear signs when to contact a KVK / agriculture officer.
- Output JSON ONLY (no markdown, no extra text) with exactly these keys:
  is_plant (bool), crop_seen (string|null), image_quality_ok (bool), image_quality_issues (list of strings),
  overall_certainty ("likely"|"possible"|"uncertain"|"not_a_plant"|"poor_image"),
  what_is_happening (2-4 simple sentences for a farmer),
  possible_issues (list of {id, name, kind, likelihood("high"|"medium"|"low"), evidence_seen[], evidence_missing[]}),
  follow_up_questions (max 3 yes/no questions that would help decide),
  safe_next_steps (max 5), see_expert_if (max 3).
- Keep ids, kinds, likelihood and certainty values in English. Write all other text in the requested language,
  using simple words."""


class VisionNotConfigured(Exception):
    pass


class VisionUpstreamError(Exception):
    pass


async def call_vision_model(image_bytes: bytes, media_type: str, system: str, user_text: str) -> str:
    """Anthropic Messages API format. To use another provider, replace ONLY this function."""
    key = os.getenv("VISION_API_KEY")
    model = os.getenv("VISION_MODEL")
    if not key or not model:
        raise VisionNotConfigured()
    payload = {
        "model": model,
        "max_tokens": 1200,
        "system": system,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": base64.b64encode(image_bytes).decode("ascii"),
                        },
                    },
                    {"type": "text", "text": user_text},
                ],
            }
        ],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(VISION_API_URL, json=payload, headers=headers)
    except httpx.HTTPError as exc:
        raise VisionUpstreamError(f"network error: {exc.__class__.__name__}") from exc
    if r.status_code != 200:
        raise VisionUpstreamError(f"model API returned {r.status_code}")
    data = r.json()
    return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sniff_image_type(data: bytes) -> str | None:
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return None


def extract_json(text: str) -> dict:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON object found")
    return json.loads(text[start : end + 1])


_DOSE = re.compile(
    r"(\d+(\.\d+)?\s*(ml|g|gm|gram|grams|kg|l|ltr|litre|litres|liter|liters|le)\s*(/|per)\s*(ha|hectare|acre|l|ltr|litre|liter|10\s*l))"
    r"|(@\s*\d)|(\d+\s*%\s*(sc|ec|sg|wp|sl|wdg))",
    re.IGNORECASE,
)
_PRODUCTS = (
    "emamectin", "chlorantraniliprole", "imidacloprid", "thiamethoxam", "cypermethrin", "profenofos",
    "acephate", "monocrotophos", "mancozeb", "carbendazim", "hexaconazole", "propiconazole", "azoxystrobin",
    "lambda", "fipronil", "spinosad", "quinalphos", "chlorpyrifos", "copper oxychloride", "streptocycline",
)


def is_unsafe_line(line: str) -> bool:
    low = line.lower()
    return bool(_DOSE.search(line)) or any(p in low for p in _PRODUCTS)


def clean_lines(lines: list[str], limit: int) -> list[str]:
    out: list[str] = []
    for line in lines:
        line = (line or "").strip()
        if line and not is_unsafe_line(line):
            out.append(line[:300])
        if len(out) >= limit:
            break
    return out


def sanitise(result: ScanResult, allowed_ids: set[str], names: dict[str, tuple[str, str]]) -> ScanResult:
    issues: list[Issue] = []
    for issue in result.possible_issues:
        if issue.id not in allowed_ids:
            continue  # drop made-up ids
        canonical_name, canonical_kind = names[issue.id]
        issue.name = issue.name or canonical_name
        issue.kind = canonical_kind  # type comes from our list, not the model  # type: ignore[assignment]
        issue.evidence_seen = clean_lines(issue.evidence_seen, 4)
        issue.evidence_missing = clean_lines(issue.evidence_missing, 3)
        issues.append(issue)
    result.possible_issues = issues[:3]
    result.safe_next_steps = clean_lines(result.safe_next_steps, 5)
    result.see_expert_if = clean_lines(result.see_expert_if, 3)
    result.follow_up_questions = clean_lines(result.follow_up_questions, 3)
    result.image_quality_issues = clean_lines(result.image_quality_issues, 4)
    if is_unsafe_line(result.what_is_happening):
        result.what_is_happening = "Please check the plant closely and ask your local KVK for advice."
    # Certainty consistency: never say "likely" without any issue, or for a non-plant.
    if not result.is_plant:
        result.overall_certainty = "not_a_plant"
        result.possible_issues = []
    elif result.overall_certainty in ("likely", "possible") and not result.possible_issues:
        result.overall_certainty = "uncertain"
    return result


def error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@router.post("/v1/disease/scan")
async def scan_leaf(
    image: UploadFile = File(...),
    crop: str = Form(...),
    language: str = Form("en"),
    answers: str = Form(""),
):
    data = await image.read()
    if len(data) == 0:
        return error(400, "EMPTY_IMAGE", "No image received.")
    if len(data) > MAX_UPLOAD_BYTES:
        return error(413, "IMAGE_TOO_LARGE", "Image is too large. Please retake or choose a smaller photo.")
    media_type = sniff_image_type(data)
    if media_type is None or media_type not in ALLOWED_TYPES:
        return error(400, "BAD_IMAGE_TYPE", "Please upload a JPEG, PNG or WebP photo.")

    lang = language if language in LANG_NAMES else "en"
    crop_key = normalise_crop(crop)
    cand = candidates_for(crop_key)
    allowed_ids = {c[0] for c in cand}
    names = {c[0]: (c[1], c[2]) for c in cand}
    cand_text = "\n".join(f"- {cid}: {nm} [{kd}]" for cid, nm, kd in cand)

    user_text = (
        f"Crop selected by the farmer: {crop or 'unknown'}.\n"
        f"Write text fields in {LANG_NAMES[lang]}.\n"
        f"Allowed issue ids:\n{cand_text}\n"
        + (f"Farmer's answers to earlier follow-up questions: {answers[:500]}\n" if answers.strip() else "")
        + "Analyse the photo and return the JSON now."
    )

    result: ScanResult | None = None
    last_problem = ""
    for attempt in range(2):
        try:
            raw = await call_vision_model(
                data, media_type, SYSTEM_PROMPT,
                user_text if attempt == 0 else user_text + "\nReturn VALID JSON ONLY, no other text.",
            )
        except VisionNotConfigured:
            return error(503, "VISION_NOT_CONFIGURED", "Photo analysis is not set up on the server yet (missing API key/model).")
        except VisionUpstreamError as exc:
            return error(502, "VISION_UPSTREAM_ERROR", f"The analysis service failed ({exc}). Please try again.")
        try:
            result = ScanResult.model_validate(extract_json(raw))
            break
        except (ValueError, ValidationError) as exc:
            last_problem = exc.__class__.__name__
    if result is None:
        return error(502, "BAD_MODEL_OUTPUT", f"Could not read the analysis result ({last_problem}). Please try again.")

    result = sanitise(result, allowed_ids, names)
    return {
        "result": result.model_dump(),
        "crop_selected": crop_key,
        "language": lang,
        "disclaimer": "AI-assisted triage from one photo. It is NOT a lab diagnosis. Confirm with your local KVK / agriculture officer before spending money on treatment.",
        "provenance": {
            "source": "AI vision model",
            "model": os.getenv("VISION_MODEL"),
            "kind": "ai_estimate",
            "mode": "live",
            "fetchedAt": datetime.now(timezone.utc).isoformat(),
        },
    }
