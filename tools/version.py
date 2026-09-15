#!/usr/bin/env python3
"""Read the canonical kernel version."""

from pathlib import Path


VERSION_PATH = Path(__file__).resolve().parent.parent / "kernel" / "VERSION"


def kernel_version(path: Path = VERSION_PATH) -> str:
    version = path.read_text(encoding="utf-8").strip()
    if not version:
        raise ValueError(f"Kernel version must not be empty: {path}")
    return version


if __name__ == "__main__":
    print(kernel_version())
