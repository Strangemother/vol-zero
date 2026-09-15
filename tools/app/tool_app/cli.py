"""Dispatch the Limine template utility commands."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.cleanup import main as cleanup_main
from tools.compile import main as compile_main
from tools.first_time import main as first_time_main
from tools.run_compiled_no_display import main as run_no_display_main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tool",
        description="Build, clean, and run the Limine kernel template.",
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

    run = subparsers.add_parser(
        "run", aliases=["r"], help="run the compiled ISO"
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

    subparsers.add_parser("lcr", help="cleanup, compile, then run")
    subparsers.add_parser("cr", help="compile, then run")
    return parser


def run_command(display: bool) -> int:
    if display:
        print("The --display runner is not implemented yet.", file=sys.stderr)
        return 2
    return run_no_display_main()


def main(arguments: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if arguments is None else arguments
    if arguments and arguments[0] in {"compile", "c"}:
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
    if parsed.command in {"run", "r"}:
        return run_command(parsed.display)
    if parsed.command == "lcr":
        status = cleanup_main([])
        if status == 0:
            status = compile_main([])
        if status == 0:
            status = run_command(False)
        return status
    if parsed.command == "cr":
        status = compile_main([])
        if status == 0:
            status = run_command(False)
        return status
    parser.error(f"unknown command: {parsed.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
