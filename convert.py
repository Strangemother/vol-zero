#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from runpy import run_path


CONVERTER = Path(__file__).resolve().parent / "github-pages" / "convert.py"


if __name__ == "__main__":
    run_path(str(CONVERTER), run_name="__main__")