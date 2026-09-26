#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OBJECT_FILE="$SCRIPT_DIR/example.o"
BINARY_FILE="$SCRIPT_DIR/example"

command -v nasm >/dev/null || {
    printf '%s\n' 'nasm is not installed. Run ./install.sh first.' >&2
    exit 1
}
command -v ld >/dev/null || {
    printf '%s\n' 'ld is not installed. Run ./install.sh first.' >&2
    exit 1
}

nasm -f elf32 "$SCRIPT_DIR/example.asm" -o "$OBJECT_FILE"
ld -m elf_i386 "$OBJECT_FILE" -o "$BINARY_FILE"
printf 'Built %s\n' "$BINARY_FILE"