from pathlib import Path
import json
from typing import List, Dict, Any

PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"

def load_json_file(filename: str) -> List[Dict[str, Any]]:
    """
    Safely load a JSON dataset using pathlib.Path(__file__).parent,
    falling back to repo-level data/ if needed.
    """
    target = DATA_DIR / filename
    if not target.exists():
        # Fallback to root data/
        target = PACKAGE_DIR.parent.parent / "data" / filename

    if not target.exists():
        raise FileNotFoundError(f"Data file '{filename}' could not be located in {DATA_DIR} or root data/")

    with open(target, "r", encoding="utf-8") as f:
        return json.load(f)

def get_crops() -> List[Dict[str, Any]]:
    return load_json_file("crops.json")

def get_msp() -> List[Dict[str, Any]]:
    return load_json_file("msp_2026.json")

def get_schemes() -> List[Dict[str, Any]]:
    return load_json_file("schemes.json")

def get_spray_products() -> List[Dict[str, Any]]:
    return load_json_file("spray_products.json")

def get_msp_table() -> List[Dict[str, Any]]:
    return load_json_file("msp_table.json")


