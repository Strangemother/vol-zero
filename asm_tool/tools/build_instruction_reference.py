#!/usr/bin/env python3
"""Build the checked-in Markdown instruction catalog from both web indexes."""

from argparse import ArgumentParser
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from docs.instruction_catalog import (
    C9X_URL,
    FELIX_CLOUTIER_URL,
    collect_instructions,
    render_markdown,
)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("docs/instructions.md"),
        help="Markdown output path (default: docs/instructions.md)",
    )
    parser.add_argument("--felix-url", default=FELIX_CLOUTIER_URL)
    parser.add_argument("--c9x-url", default=C9X_URL)
    args = parser.parse_args()

    instructions = collect_instructions(args.felix_url, args.c9x_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(instructions), encoding="utf-8")
    print(f"Wrote {len(instructions)} instructions to {args.output}")


if __name__ == "__main__":
    main()