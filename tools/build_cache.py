#!/usr/bin/env python3
"""Load and update persistent build metadata."""

import json
from pathlib import Path
from typing import Any


CACHE_PATH = Path(__file__).resolve().with_name("cache.json")


def load_cache(path: Path = CACHE_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as cache_file:
        data = json.load(cache_file)
    if not isinstance(data, dict):
        raise ValueError(f"Build cache must contain a JSON object: {path}")
    return data


def save_cache(cache: dict[str, Any], path: Path = CACHE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".json.tmp")
    with temporary_path.open("w", encoding="utf-8") as cache_file:
        json.dump(cache, cache_file, indent=2, sort_keys=True)
        cache_file.write("\n")
    temporary_path.replace(path)
