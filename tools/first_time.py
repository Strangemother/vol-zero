#!/usr/bin/env python3
"""Install dependencies, build the Limine kernel, and run it in QEMU."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.nim import ensure_nim


PACKAGES = [
    "build-essential",
    "git",
    "curl",
    "xorriso",
    "qemu-system-x86",
    "gdisk",
    "mtools",
]

REQUIRED_COMMANDS = [
    "make",
    "cc",
    "ld",
    "git",
    "curl",
    "xorriso",
    "qemu-system-x86_64",
]


def run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    subprocess.run(command, check=True, env=env)


def apt_prefix() -> list[str]:
    if os.geteuid() == 0:
        return []
    if shutil.which("sudo") is None:
        raise RuntimeError("sudo is required to install packages when not running as root")
    return ["sudo"]


def install_packages() -> None:
    prefix = apt_prefix()
    run(prefix + ["apt-get", "update"])
    run(prefix + ["apt-get", "install", "-y", *PACKAGES])


def verify_commands() -> None:
    missing = [command for command in REQUIRED_COMMANDS if shutil.which(command) is None]
    if missing:
        raise RuntimeError("Missing commands after installation: " + ", ".join(missing))


def main() -> int:
    os.chdir(PROJECT_ROOT)

    print("Installing build and QEMU dependencies...", flush=True)
    install_packages()

    print("Checking the configured toolchain...", flush=True)
    verify_commands()
    ensure_nim()

    environment = os.environ.copy()
    environment.setdefault("HOST_CC", "cc")
    qemu_flags = ["-m", "2G", "-display", "none", "-monitor", "none", "-serial", "stdio"]

    print("Building the kernel and bootable ISO...", flush=True)
    run(["make", "all"], env=environment)

    print("Starting QEMU. Press Ctrl+C to stop the intentionally halted kernel.", flush=True)
    run(["make", "run", "QEMUFLAGS=" + " ".join(qemu_flags)], env=environment)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        raise SystemExit(130)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"\nBootstrap failed: {error}", file=sys.stderr)
        raise SystemExit(1)
