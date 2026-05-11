import json
import os
from datetime import datetime

from pathlib import Path

DEFAULT_DATA = {}

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "entries.json"

FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

def create_file_if_not_exists():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump(DEFAULT_DATA, f, indent=2)


def load_entries():
    create_file_if_not_exists()
    with open(FILE_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def validate_entry(entry):
    required_keys = {
        "date": str,
        "internship_id": int,
        "description": str,
        "hours": (int, float),
        "links": str,
        "blockers": str,
        "learnings": str,
        "mood_slider": int,
        "skill_ids": list,
    }

    # Check missing keys
    for key in required_keys:
        if key not in entry:
            raise ValueError(f"Missing key: {key}")

    # Check types
    for key, expected_type in required_keys.items():
        if not isinstance(entry[key], expected_type):
            raise TypeError(f"{key} must be {expected_type}, got {type(entry[key])}")

    # Validate skill_ids contents
    if not all(isinstance(i, str) for i in entry["skill_ids"]):
        raise TypeError("skill_ids must be a list of strings")

    # Validate date format
    try:
        datetime.strptime(entry["date"], "%Y-%m-%d")
    except ValueError:
        raise ValueError("date must be in YYYY-MM-DD format")

    # Validate mood_slider range
    if not (1 <= entry["mood_slider"] <= 10):
        raise ValueError("mood_slider must be between 1 and 10")

    return True


def validate_all_entries(entries: list):
    for i, entry in enumerate(entries):
        try:
            validate_entry(entry)
        except Exception as e:
            raise ValueError(f"Entry {i} invalid: {e}")

    print("All entries are valid!")
