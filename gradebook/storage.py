import json, os
from typing import Dict, Any
from logging import getLogger

logger = getLogger(__name__)
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "gradebook.json")

def _ensure_parent_dir(path): os.makedirs(os.path.dirname(path), exist_ok=True)

def load_data(path=None) -> Dict[str, Any]:
    path = path or DEFAULT_PATH
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("students", [])
            data.setdefault("courses", [])
            data.setdefault("enrollments", [])
            return data
    except FileNotFoundError:
        return {"students": [], "courses": [], "enrollments": []}
    except json.JSONDecodeError:
        print("❌ JSON corrupted. Starting empty.")
        return {"students": [], "courses": [], "enrollments": []}

def save_data(data, path=None):
    path = path or DEFAULT_PATH
    _ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
