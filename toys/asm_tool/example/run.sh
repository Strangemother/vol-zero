#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINARY_FILE="$SCRIPT_DIR/example"
EXPRESSION="${1:-2+3}"

if [[ ! -x "$BINARY_FILE" ]]; then
    printf '%s\n' 'example is not compiled. Run ./compile.sh first.' >&2
    exit 1
fi

if [[ ! "$EXPRESSION" =~ ^.[+*/-].$ ]]; then
    printf 'Usage: %s [digit\{+,-,\*,/\}digit]\n' "$0" >&2
    exit 2
fi

printf '%s' "$EXPRESSION" | timeout 5 "$BINARY_FILE"
printf '\n'