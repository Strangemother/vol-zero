#!/usr/bin/env python3
"""Build the hosted VOL development executable."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.nim import ensure_nim
from tools.build_cache import load_cache, save_cache
from tools.dist_hosted_filename import hosted_filename
KERNEL_DIR = PROJECT_ROOT / "kernel"
DIST_DIR = PROJECT_ROOT / "dist"


def main() -> int:
    asset_knowledge = load_cache()
    asset_knowledge["build_count"] = int(asset_knowledge.get("build_count", 0)) + 1
    save_cache(asset_knowledge)
    hosted_output = DIST_DIR / hosted_filename(asset_knowledge)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    environment = os.environ.copy()
    nimble = environment.get("NIMBLE") or str(ensure_nim())
    environment["HOSTED_OUTPUT"] = str(hosted_output)
    command = [nimble, "buildHosted"]
    completed = subprocess.run(command, cwd=KERNEL_DIR, env=environment)
    if completed.returncode == 0:
        (DIST_DIR / "vol-hosted").unlink(missing_ok=True)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
