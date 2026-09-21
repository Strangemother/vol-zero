"""Dispatch the Limine template utility commands."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.cleanup import main as cleanup_main
from tools.compile import main as compile_main
from tools.compile_hosted import main as compile_hosted_main
from tools.first_time import main as first_time_main
from tools.nim import NIM_BIN_DIR, USER_BIN_DIR, configure_nim, ensure_nim
from tools.run_compiled_no_display import main as run_no_display_main
from tools.run_oraclebox import main as run_oraclebox_main
from tools.run_hosted import main as run_hosted_main
from tools.site_export import main as site_export_main
from tools.tail_serial import main as tail_serial_main


def build_parser() -> argparse.ArgumentParser:

    banner = Path(__file__).resolve().parent / "banner.txt"
    parser = argparse.ArgumentParser(
        prog="tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=banner.read_text(),
        description="Build, clean, and run the kernel.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    cleanup = subparsers.add_parser(
        "cleanup", aliases=["l"], help="clean generated build assets"
    )
    cleanup.add_argument(
        "--hard",
        action="store_true",
        help="also remove downloaded assets",
    )

    compile_parser = subparsers.add_parser(
        "compile", aliases=["c"], help="build a fresh distribution ISO"
    )
    compile_parser.add_argument("make_args", nargs=argparse.REMAINDER)

    subparsers.add_parser(
        "first_time",
        aliases=["first-time", "f"],
        help="install dependencies, build, and run QEMU",
    )

    install = subparsers.add_parser(
        "install", aliases=["i"], help="install and configure toolchain dependencies"
    )
    install.add_argument(
        "dependency",
        nargs="?",
        choices=["nim"],
        default="nim",
        help="dependency to install (default: nim)",
    )

    run = subparsers.add_parser(
        "run", aliases=["r"], help="run the compiled ISO"
    )
    run.add_argument(
        "target",
        nargs="?",
        choices=["os", "app", "oraclebox", "vbox"],
        default="os",
        help="run the OS image, hosted app, or VirtualBox VM (default: os)",
    )
    run_mode = run.add_mutually_exclusive_group()
    run_mode.add_argument(
        "--no-display",
        action="store_true",
        help="run QEMU without a graphical display (default)",
    )
    run_mode.add_argument(
        "--display",
        action="store_true",
        help="run with a graphical display (not implemented yet)",
    )
    run.add_argument(
        "--serial",
        choices=["file", "tcp"],
        default="file",
        help="VirtualBox serial output mode (default: file)",
    )
    run.add_argument(
        "--headless",
        action="store_true",
        help="start VirtualBox without a window",
    )

    subparsers.add_parser(
        "tail",
        aliases=["t"],
        help="wait for and stream the VirtualBox TCP serial console",
    )

    site = subparsers.add_parser(
        "site",
        aliases=["s"],
        help="manage the static documentation site",
    )
    site_subparsers = site.add_subparsers(dest="site_command", metavar="COMMAND")
    site_export = site_subparsers.add_parser(
        "export",
        help="export the Flask documentation site as static files",
    )
    site_export.add_argument(
        "config",
        nargs="?",
        help="JSON export configuration file",
    )
    site_export.add_argument("--base-url", help="override the configured Flask docs site URL")
    site_export.add_argument("--output-dir", help="override the configured output directory")
    site_export.add_argument("--max-pages", type=int, help="override the configured crawl page limit")
    site_run = site_subparsers.add_parser(
        "run",
        help="run the Flask documentation site",
    )
    site_run.add_argument(
        "--host",
        default="127.0.0.1",
        help="host interface to bind (default: 127.0.0.1)",
    )
    site_run.add_argument(
        "--port",
        type=int,
        default=9050,
        help="port to bind (default: 9050)",
    )
    site_run.add_argument(
        "--no-debug",
        action="store_true",
        help="disable Flask debug mode",
    )

    for command, help_text in (("lcr", "cleanup, compile, then run"), ("cr", "compile, then run")):
        parser_for_command = subparsers.add_parser(command, help=help_text)
        parser_for_command.add_argument(
            "target",
            nargs="?",
            choices=["os", "app"],
            default="os",
            help="build the OS image or hosted app (default: os)",
        )
    subparsers.add_parser("alcr", help="cleanup, compile hosted app, then run")
    subparsers.add_parser(
        "arc",
        aliases=["acr", "car"],
        help="compile hosted app, then run",
    )
    return parser


def run_command(display: bool) -> int:
    if display:
        print("The --display runner is not implemented yet.", file=sys.stderr)
        return 2
    return run_no_display_main()


def compile_target(target: str) -> int:
    if target == "app":
        return compile_hosted_main()
    return compile_main([])


def install_target(dependency: str) -> int:
    if dependency == "nim":
        ensure_nim()
        configure_nim()
        print(f"Nim is ready at {NIM_BIN_DIR}.", flush=True)
        if str(USER_BIN_DIR) not in os.environ.get("PATH", "").split(os.pathsep):
            print(f"Add it to this shell with: export PATH=\"{USER_BIN_DIR}:$PATH\"", flush=True)
    return 0


def run_target(
    target: str,
    display: bool = False,
    serial: str = "file",
    headless: bool = False,
) -> int:
    if target == "app":
        return run_hosted_main()
    if target in {"oraclebox", "vbox"}:
        arguments = ["--serial", serial]
        if headless:
            arguments.append("--headless")
        return run_oraclebox_main(arguments)
    return run_command(display)


def run_site(host: str, port: int, debug: bool) -> int:
    from doc_site.app import main as site_run_main

    site_run_main(host=host, port=port, debug=debug)
    return 0


def main(arguments: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if arguments is None else arguments
    if arguments and arguments[0] in {"compile", "c"}:
        if len(arguments) > 1 and arguments[1] == "app":
            return compile_hosted_main()
        return compile_main(arguments[1:])

    parser = build_parser()
    parsed = parser.parse_args(arguments)

    if parsed.command is None:
        parser.print_help()
        return 0
    if parsed.command in {"cleanup", "l"}:
        return cleanup_main(["--hard"] if parsed.hard else [])
    if parsed.command in {"compile", "c"}:
        return compile_main(parsed.make_args)
    if parsed.command in {"first_time", "first-time", "f"}:
        return first_time_main()
    if parsed.command in {"install", "i"}:
        return install_target(parsed.dependency)
    if parsed.command in {"run", "r"}:
        if parsed.target in {"oraclebox", "vbox"}:
            return run_target(parsed.target, parsed.display, parsed.serial, parsed.headless)
        return run_target(parsed.target, parsed.display)
    if parsed.command in {"tail", "t"}:
        return tail_serial_main()
    if parsed.command == "site":
        if parsed.site_command == "export":
            site_arguments = []
            if parsed.config:
                site_arguments.append(parsed.config)
            if parsed.base_url:
                site_arguments.extend(["--base-url", parsed.base_url])
            if parsed.output_dir:
                site_arguments.extend(["--output-dir", parsed.output_dir])
            if parsed.max_pages:
                site_arguments.extend(["--max-pages", str(parsed.max_pages)])
            return site_export_main(site_arguments)
        if parsed.site_command == "run":
            return run_site(parsed.host, parsed.port, not parsed.no_debug)
        parser.error("site requires a command: export, run")
    if parsed.command in {"lcr", "cr"}:
        target = parsed.target
    elif parsed.command in {"alcr", "arc", "acr", "car"}:
        target = "app"
    else:
        target = "os"
    if parsed.command in {"lcr", "alcr"}:
        status = cleanup_main([])
        if status == 0:
            status = compile_target(target)
        if status == 0:
            status = run_target(target)
        return status
    if parsed.command in {"cr", "arc", "acr", "car"}:
        status = compile_target(target)
        if status == 0:
            status = run_target(target)
        return status
    parser.error(f"unknown command: {parsed.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
