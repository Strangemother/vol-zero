#!/usr/bin/env python3
"""Launch the current compiled ISO in QEMU without a graphical display."""

from pathlib import Path
import os
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools import iso_filename
from tools.build_cache import load_cache


def main() -> int:
    iso_path = PROJECT_ROOT / "dist" / iso_filename(load_cache())
    command = [
        "qemu-system-x86_64",
        "-M",
        "q35",
        "-cdrom",
        str(iso_path),
        "-boot",
        "d",
        "-m",
        "0.1G",
        "-display",
        "none",
        "-monitor",
        "none",
        "-serial",
        "stdio",
    ]
    os.chdir(PROJECT_ROOT)
    os.execvp(command[0], command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
