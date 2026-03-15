import os
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data2001"


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data_file = DATA_DIR / "city_sets.json"
    if not data_file.exists():
        data_file.write_text("[]")


def load_city_sets() -> list[dict]:
    _ensure_data_dir()
    return json.loads((DATA_DIR / "city_sets.json").read_text())


def save_city_sets(data: list[dict]):
    _ensure_data_dir()
    (DATA_DIR / "city_sets.json").write_text(json.dumps(data, ensure_ascii=False, indent=2))
