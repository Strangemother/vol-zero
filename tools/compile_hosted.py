#!/usr/bin/env python3
"""Build the hosted VOL development executable."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KERNEL_DIR = PROJECT_ROOT / "kernel"
HOSTED_OUTPUT = KERNEL_DIR / "bin" / "vol-hosted"


def main() -> int:
    environment = os.environ.copy()
    nimble = environment.get("NIMBLE", str(Path.home() / ".local/opt/nim-2.2.12/bin/nimble"))
    command = [nimble, "buildHosted", "HOSTED_OUTPUT=" + str(HOSTED_OUTPUT)]
    completed = subprocess.run(command, cwd=KERNEL_DIR, env=environment)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
