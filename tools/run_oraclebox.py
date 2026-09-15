#!/usr/bin/env python3
"""Create or update a VirtualBox VM and boot the current distribution ISO."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools import iso_filename, kernel_version
from tools.build_cache import load_cache


LEGACY_VM_NAME = "VOL Zero"
VERSIONED_VM_PREFIX = "VOL "
DEFAULT_OS_TYPE = "Other_64"
DEFAULT_MEMORY = 1024
DEFAULT_VIDEO_MEMORY = 50
DEFAULT_GRAPHICS_CONTROLLER = "vmsvga"
DEFAULT_IOAPIC = "on"


def find_vboxmanage() -> str:
    for command in ("VBoxManage", "VBoxManage.exe"):
        path = shutil.which(command)
        if path:
            return path
    standard_windows_path = Path("/mnt/c/Program Files/Oracle/VirtualBox/VBoxManage.exe")
    if standard_windows_path.is_file():
        return str(standard_windows_path)
    raise RuntimeError(
        "VBoxManage was not found. Install VirtualBox and ensure VBoxManage.exe "
        "is available on the WSL PATH."
    )


def run(command: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(command), flush=True)
    return subprocess.run(command, check=True, text=True, capture_output=capture_output)


def windows_path(path: Path) -> str:
    if os.name == "nt":
        return str(path)
    wslpath = shutil.which("wslpath")
    if not wslpath:
        raise RuntimeError("wslpath was not found; run this command inside WSL or Windows.")
    result = subprocess.run(
        [wslpath, "-w", str(path)], check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def vm_exists(vboxmanage: str, vm_name: str) -> bool:
    result = run([vboxmanage, "list", "vms"], capture_output=True)
    quoted_name = f'"{vm_name}"'
    return any(line.startswith(quoted_name + " ") for line in result.stdout.splitlines())


def vm_names(vboxmanage: str) -> list[str]:
    result = run([vboxmanage, "list", "vms"], capture_output=True)
    return [match.group(1) for line in result.stdout.splitlines() if (match := re.match(r'^"([^"]+)"\s', line))]


def vm_state(vboxmanage: str, vm_name: str) -> str:
    result = run(
        [vboxmanage, "showvminfo", vm_name, "--machinereadable"], capture_output=True
    )
    for line in result.stdout.splitlines():
        if line.startswith("VMState="):
            return line.partition("=")[2].strip('"')
    return "unknown"


def migrate_versioned_vm(vboxmanage: str, vm_name: str) -> None:
    if vm_exists(vboxmanage, vm_name):
        return

    candidates = [
        name
        for name in vm_names(vboxmanage)
        if name == LEGACY_VM_NAME or name.startswith(VERSIONED_VM_PREFIX)
    ]
    if len(candidates) != 1:
        return

    previous_name = candidates[0]
    state = vm_state(vboxmanage, previous_name)
    if state not in {"poweroff", "saved", "aborted", "unknown"}:
        run([vboxmanage, "controlvm", previous_name, "poweroff"])
    run([vboxmanage, "modifyvm", previous_name, "--name", vm_name])


def configure_vm(vboxmanage: str, vm_name: str, memory: int, cpus: int, iso_path: str) -> None:
    if not vm_exists(vboxmanage, vm_name):
        run(
            [
                vboxmanage,
                "createvm",
                "--name",
                vm_name,
                "--ostype",
                DEFAULT_OS_TYPE,
                "--register",
            ]
        )
        run(
            [
                vboxmanage,
                "storagectl",
                vm_name,
                "--name",
                "SATA",
                "--add",
                "sata",
                "--controller",
                "IntelAhci",
            ]
        )

    state = vm_state(vboxmanage, vm_name)
    if state not in {"poweroff", "saved", "aborted", "unknown"}:
        run([vboxmanage, "controlvm", vm_name, "poweroff"])

    run(
        [
            vboxmanage,
            "modifyvm",
            vm_name,
            "--memory",
            str(memory),
            "--ostype",
            DEFAULT_OS_TYPE,
            "--vram",
            str(DEFAULT_VIDEO_MEMORY),
            "--graphicscontroller",
            DEFAULT_GRAPHICS_CONTROLLER,
            "--ioapic",
            DEFAULT_IOAPIC,
            "--cpus",
            str(cpus),
            "--boot1",
            "dvd",
            "--boot2",
            "disk",
            "--boot3",
            "none",
            "--boot4",
            "none",
            "--audio-driver",
            "none",
        ]
    )
    run(
        [
            vboxmanage,
            "storageattach",
            vm_name,
            "--storagectl",
            "SATA",
            "--port",
            "0",
            "--device",
            "0",
            "--type",
            "dvddrive",
            "--medium",
            iso_path,
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--name",
        help="VirtualBox VM name (default: VOL followed by the kernel version)",
    )
    parser.add_argument("--memory", type=int, default=DEFAULT_MEMORY, help="VM memory in MiB")
    parser.add_argument("--cpus", type=int, default=2, help="Number of virtual CPUs")
    parser.add_argument("--headless", action="store_true", help="start without a VirtualBox window")
    return parser


def main(arguments: list[str] | None = None) -> int:
    parsed = build_parser().parse_args(arguments)
    if parsed.memory < 128 or parsed.cpus < 1:
        raise ValueError("memory must be at least 128 MiB and cpus must be positive")

    iso_path = PROJECT_ROOT / "dist" / iso_filename(load_cache())
    if not iso_path.is_file():
        raise FileNotFoundError(f"Compiled ISO was not found: {iso_path}. Run tool compile first.")

    vboxmanage = find_vboxmanage()
    vm_name = parsed.name or f"{VERSIONED_VM_PREFIX}{kernel_version()}"
    if parsed.name is None:
        migrate_versioned_vm(vboxmanage, vm_name)
    configure_vm(vboxmanage, vm_name, parsed.memory, parsed.cpus, windows_path(iso_path))
    run([vboxmanage, "startvm", vm_name, "--type", "headless" if parsed.headless else "gui"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"\nVirtualBox launch failed: {error}", file=sys.stderr)
        raise SystemExit(1)