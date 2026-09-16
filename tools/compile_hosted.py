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
KERNEL_DIR = PROJECT_ROOT / "kernel"
HOSTED_OUTPUT = KERNEL_DIR / "bin" / "vol-hosted"


def main() -> int:
    environment = os.environ.copy()
    nimble = environment.get("NIMBLE") or str(ensure_nim())
    command = [nimble, "buildHosted", "HOSTED_OUTPUT=" + str(HOSTED_OUTPUT)]
    completed = subprocess.run(command, cwd=KERNEL_DIR, env=environment)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
