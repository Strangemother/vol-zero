#!/usr/bin/env python3
"""Run the hosted VOL development executable."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent.parent
HOSTED_OUTPUT = PROJECT_ROOT / "dist" / "vol-hosted"


def main() -> int:
    if not HOSTED_OUTPUT.exists():
        print("Hosted executable is missing; build it with 'tool compile app'.")
        return 2
    completed = subprocess.run([str(HOSTED_OUTPUT)], cwd=PROJECT_ROOT, env=os.environ.copy())
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
