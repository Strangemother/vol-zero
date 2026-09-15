# Limine C Template

This repository will demonstrate how to set up a basic x86-64 kernel in C using Limine.

It is recommended to cross reference the contents of this repository with [the Limine Bare Bones](https://osdev.wiki/wiki/Limine_Bare_Bones) OSDev wiki page.

## How to use this?

### Dependencies

Any `make` command depends on GNU make (`gmake`) and is expected to be run using it. This usually means using `make` on most GNU/Linux distros, or `gmake` on other non-GNU systems.

All `make all*` targets depend on a GNU-compatible C toolchain capable of generating x86-64 ELF objects. Usually `gcc/binutils` or `clang/llvm/lld` provided by any x86-64 UNIX like (including Linux) distribution will suffice.

Building also requires `git`, used to fetch the kernel's dependencies (see `kernel/get-deps`), `curl`, used to download the Limine release and the EDK2 OVMF firmware images, and a C compiler for the host (`cc` by default, see the `HOST_CC` `make` variable), used to build the `limine` host utility.

Additionally, building an ISO with `make all` requires `xorriso`, and building a HDD/USB image with `make all-hdd` requires `sgdisk` (usually from `gdisk` or `gptfdisk` packages) and `mtools`.

The kernel sources are written in Nim and require the upstream Nim 2.2.12 binary at `$HOME/.local/opt/nim-2.2.12/bin/nim`. Download and unpack `nim-2.2.12-linux_x64.tar.xz` from [nim-lang.org](https://nim-lang.org/download/nim-2.2.12-linux_x64.tar.xz) into that directory before running `make`.

### Kernel version

The canonical kernel version is stored in `kernel/VERSION`. Keep the file to a
single non-empty version string. The build reads it for the Nim package
metadata, embeds it in the kernel through
`kernel/src/core/version.nim`, displays it through the runtime
`get_version()` procedure, includes it in distribution filenames, and inserts
the version into the Limine boot-menu entry. The boot-menu name is currently
hardcoded as `VOL` in `limine.conf`; a broader configuration file can provide
that value later.

Update `kernel/VERSION` to bump the version; the other build and runtime values
are derived automatically.

Assembly files with the `*.S` extension are built using the same toolchain as the C sources. Only `*.asm` files, of which the template ships none, require `nasm`. The `run` targets require `qemu`.

### Toolchain selection

The `TOOLCHAIN` and `TOOLCHAIN_PREFIX` `make` variables can be used to set the toolchain. `TOOLCHAIN` can be set to `llvm` to use Clang/LLVM.

For example:
```
make TOOLCHAIN=llvm
```
or:
```
make TOOLCHAIN_PREFIX=x86_64-elf-
```

### Makefile targets

Running `make all` will compile the kernel (from the `kernel/` directory) and then generate the ISO named by `tools/dist_iso_filename.py` under `dist/`.

Running `make all-hdd` will compile the kernel and then generate the HDD image named by `tools/dist_hdd_filename.py` under `dist/`, a raw image suitable to be flashed onto a USB stick or hard drive/SSD.

Each `python3 tools/compile.py` build increments the persistent counter in `tools/cache.json` and records the build time. The resulting ISO and HDD names use that metadata, for example `vol-kernel-26-09-14-23-23-1.iso`.

Running `make run` will build the kernel and a bootable ISO (equivalent to make all) and then run it using `qemu` (if installed).

Running `make run-hdd` will build the kernel and a raw HDD image (equivalent to make all-hdd) and then run it using `qemu` (if installed).

The `run-uefi` and `run-hdd-uefi` targets are equivalent to their non `-uefi` counterparts except that they boot `qemu` using a UEFI-compatible firmware.

Run `python3 tools/cleanup.py` to remove local build outputs while preserving downloaded dependencies and tools. Use `python3 tools/cleanup.py --hard` to remove those downloaded assets as well.

### Tool command

Install the project tools from the repository root:

```
pip install -e tools/app
```

The installed `tool` command provides shortcuts for the common workflows:

```
tool cleanup
tool cleanup --hard
tool compile
tool first_time
tool run
tool run --no-display
tool lcr
tool cr
```

Short aliases are available as `tool l`, `tool c`, `tool f`, and `tool r`. The `--display` run mode is reserved for a future graphical runner.
