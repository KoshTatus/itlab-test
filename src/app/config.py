import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent.parent / "settings.json"

def load_settings():
    if not SETTINGS_FILE.exists():
        raise FileNotFoundError(f"Settings file not found: {SETTINGS_FILE}")

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")

    if "camera" not in settings and "region" not in settings["camera"]:
        raise ValueError("Missing 'camera.region' field in settings")

    return settings["camera"]["region"]