#!/usr/bin/env python3
"""Return the distribution ISO filename."""

from typing import Any

try:
    from .version import kernel_version
except ImportError:
    from version import kernel_version


def iso_filename(asset_knowledge: dict[str, Any]) -> str:
    version = kernel_version()
    date = asset_knowledge.get("build_datetime", "00-00-00-00-00")
    count = asset_knowledge.get("build_count", 0)
    return f"vol-kernel-{version}-{date}-{count}.iso"


def main() -> str:
    from build_cache import load_cache

    return iso_filename(load_cache())


if __name__ == "__main__":
    print(main())
