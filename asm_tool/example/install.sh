#!/usr/bin/env bash
set -eu

if [[ "$(id -u)" -eq 0 ]]; then
    apt-get update
    apt-get install -y nasm binutils coreutils
else
    sudo apt-get update
    sudo apt-get install -y nasm binutils coreutils
fi