# Build dependencies and usage

## Dependencies

Any `make` command requires GNU make (`gmake` on systems where GNU make is not
the default). The build also requires:

- A GNU-compatible C toolchain that can generate x86-64 ELF objects, such as
  GCC/binutils or Clang/LLVM/lld.
- `git` to fetch kernel dependencies through `kernel/get-deps`.
- `curl` to download Limine and EDK2 OVMF firmware images.
- A host C compiler (`cc` by default, configurable with `HOST_CC`) for the
  Limine utility.
- `xorriso` for ISO images.
- `sgdisk` from `gdisk` or `gptfdisk`, and `mtools`, for HDD/USB images.
- `qemu` for the run targets.
- Nim 2.2.12 at `$HOME/.local/opt/nim-2.2.12/bin/nim` for the kernel sources.

The `tool c` and `tool c app` commands download and unpack the Nim archive
from [nim-lang.org](https://nim-lang.org/download/nim-2.2.12-linux_x64.tar.xz)
when it is missing.

## How to use this project

Install the project helper from the repository root, then build the kernel:

```sh
pip install -e tools/app
tool c
```

The build fetches the pinned kernel dependencies under `kernel_deps/` and
creates a bootable ISO under `dist/`. Use [Running the kernel](running.md) for QEMU and VirtualBox
instructions, or see [The `tool` command](tool.md) for the available workflows
and aliases.

For Windows setup, use [Windows Subsystem for Linux](windows-wsl.md) with
Ubuntu, or [Windows development](windows.md) with MSYS2 and the PowerShell
helpers.

## Makefile targets

From the repository root:

```sh
make all
make all-hdd
make run
make run-hdd
make run-uefi
make run-hdd-uefi
```

`make all` builds the kernel from `kernel/` and creates an ISO under `dist/`.
`make all-hdd` creates a raw HDD image suitable for a hard disk or USB drive.
The `run` targets build their corresponding image and start QEMU; the `-uefi`
variants use UEFI-compatible firmware.

Each `python3 tools/compile.py` build increments the persistent counter in
`tools/cache.json` and records the build time. ISO and HDD filenames include
that metadata.

Assembly files with the `*.S` extension use the C toolchain. Only `*.asm`
files require `nasm`; the template currently ships none.

## Toolchain selection

Set `TOOLCHAIN=llvm` to use Clang/LLVM, or set `TOOLCHAIN_PREFIX` for a
cross-toolchain:

```sh
make TOOLCHAIN=llvm
make TOOLCHAIN_PREFIX=x86_64-elf-
```

## Hosted build

For a fast hosted build from `kernel/`:

```sh
nimble buildHosted
./bin/vol-hosted
```

This uses `src/hosted_main.nim` with Nim's normal runtime and does not require
Limine or the freestanding linker. From the repository root, use `tool compile
app` and `tool run app` instead.

## Cleanup

Run `python3 tools/cleanup.py` to remove local build outputs while preserving
downloaded dependencies and tools. Add `--hard` to remove those downloaded
assets as well.