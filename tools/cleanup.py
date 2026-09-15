#!/usr/bin/env python3
"""Remove generated kernel, bootloader, dependency, and image assets."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SOFT_GENERATED_PATHS = [
    "template.iso",
    "template.hdd",
    "dist",
    "iso_root",
    "kernel/bin",
    "kernel/obj",
    "kernel/.cache",
    "kernel/compile_commands.json",
    "__pycache__",
    "tools/__pycache__",
    "tools/app/tool_app/__pycache__",
    "tools/app/limine_template_tools.egg-info",
]

DOWNLOADED_PATHS = [
    "limine-binary",
    "limine-binary.tar.gz",
    "edk2-ovmf-bins",
    "edk2-ovmf-bins.tar.gz",
    "kernel/.deps-obtained",
    "kernel/freestanding-c-hdrs",
    "kernel/cc-runtime",
    "kernel/limine-protocol",
]


def remove_generated(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()
    else:
        return
    print(f"Removed {path}")


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    cleanup_mode = parser.add_mutually_exclusive_group()
    cleanup_mode.add_argument(
        "--soft",
        action="store_true",
        help="remove local build outputs while preserving downloaded assets (default)",
    )
    cleanup_mode.add_argument(
        "--hard",
        action="store_true",
        help="also remove downloaded toolchain and kernel dependencies",
    )
    parsed_arguments = parser.parse_args(arguments)

    project_dir = Path(__file__).resolve().parent.parent
    generated_paths = list(SOFT_GENERATED_PATHS)
    if parsed_arguments.hard:
        generated_paths.extend(DOWNLOADED_PATHS)
    for relative_path in generated_paths:
        remove_generated(project_dir / relative_path)
    print("Cleanup complete. Source and project configuration were preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
