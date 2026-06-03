import copy
import json
import os
from pathlib import Path

from app.github_db import read_json, write_json

BASE_DIR = Path(__file__).resolve().parent.parent


def _fallback_value(fallback):
    return copy.deepcopy(fallback)


def _local_path(path):
    return BASE_DIR / path


def load_json(path, fallback):
    token = os.getenv("GITHUB_TOKEN")
    if token:
        data = read_json(path, token)
        return _fallback_value(fallback) if data is None else data

    full_path = _local_path(path)
    if not full_path.exists():
        return _fallback_value(fallback)

    try:
        return json.loads(full_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _fallback_value(fallback)


def save_json(path, data, message):
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return write_json(path, data, token, message=message)

    full_path = _local_path(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "local": True, "path": path}
