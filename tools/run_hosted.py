#!/usr/bin/env python3
"""Run the hosted VOL development executable."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.build_cache import load_cache
from tools.dist_hosted_filename import hosted_filename


def main() -> int:
    hosted_output = PROJECT_ROOT / "dist" / hosted_filename(load_cache())
    if not hosted_output.exists():
        print("Hosted executable is missing; build it with 'tool compile app'.")
        return 2
    completed = subprocess.run([str(hosted_output)], cwd=PROJECT_ROOT, env=os.environ.copy())
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
