"""Install and locate the Nim toolchain required by the kernel builds."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


NIM_VERSION = "2.2.12"
NIM_ARCHIVE_NAME = f"nim-{NIM_VERSION}-linux_x64.tar.xz"
NIM_DOWNLOAD_URL = f"https://nim-lang.org/download/{NIM_ARCHIVE_NAME}"
NIM_INSTALL_DIR = Path.home() / ".local" / "opt" / f"nim-{NIM_VERSION}"
NIM_BIN_DIR = NIM_INSTALL_DIR / "bin"
NIM_PATH = NIM_BIN_DIR / "nim"
NIMBLE_PATH = NIM_BIN_DIR / "nimble"
USER_BIN_DIR = Path.home() / ".local" / "bin"


def _run(command: list[str]) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    subprocess.run(command, check=True)


def ensure_nim() -> Path:
    """Download Nim when needed and return the Nimble executable path."""
    if NIM_PATH.is_file() and NIMBLE_PATH.is_file():
        return NIMBLE_PATH

    NIM_INSTALL_DIR.parent.mkdir(parents=True, exist_ok=True)
    archive_path = Path(tempfile.gettempdir()) / NIM_ARCHIVE_NAME
    print(f"Installing Nim {NIM_VERSION}...", flush=True)
    try:
        _run(["curl", "-fL", NIM_DOWNLOAD_URL, "-o", str(archive_path)])
        _run(["tar", "-xJf", str(archive_path), "-C", str(NIM_INSTALL_DIR.parent)])
    finally:
        archive_path.unlink(missing_ok=True)

    if not NIM_PATH.is_file() or not NIMBLE_PATH.is_file():
        raise RuntimeError(f"Nim {NIM_VERSION} was not installed at {NIM_INSTALL_DIR}")
    return NIMBLE_PATH


def configure_nim() -> None:
    """Make Nim and Nimble available through the user's local bin directory."""
    USER_BIN_DIR.mkdir(parents=True, exist_ok=True)
    for command, target in (("nim", NIM_PATH), ("nimble", NIMBLE_PATH)):
        link = USER_BIN_DIR / command
        if link.is_symlink() and link.resolve() == target:
            continue
        if link.exists() or link.is_symlink():
            print(f"Skipping existing {link}; it was not changed.", flush=True)
            continue
        link.symlink_to(target)