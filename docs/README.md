# VOL Zero.

+ [the Limine Bare Bones](https://osdev.wiki/wiki/Limine_Bare_Bones) OSDev wiki page.
+ [limine-c-template-x86-64 GitHub repository](https://github.com/Limine-Bootloader/limine-c-template-x86-64)


## High Level Overview

This presents a minimal setup for a x86-64 VOL kernel using the Limine bootloader and demonstrates how to structure the project for both hosted and freestanding development.

It produces:

1. A minimal x86-64 VOL kernel image
2. An app; standard like.

Making the kernel looks like this:

```sh
$ tool c
make: Entering directory '/workspaces/limine-c-template-x86-64'
make -C kernel
...
# dist/vol-kernel-0.1.0-26-09-15-03-34-15.iso
```

This can be ran using QEMU or VirtualBox. Compiling the 'hdd' version allows booting from a hard disk or USB drive.

### Kernel: QEMU

To run the kernel using QEMU:

```sh
tool run
```

To run the kernel without a display (headless mode) (default on terminal):

```sh
$ tool run --no-display
# Kernel version: 0.1.0
```

This version prints the kernel output and version to the terminal.

### Kernel: VirtualBox

1. Open VirtualBox and create a new virtual machine.
2. Set the type to "Linux" or "Other" and the version to "Other/Unknown (64-bit)".
3. Allocate memory and create a virtual hard disk as needed: e.g. 40mb
4. Go to the "Storage" section and attach the generated ISO file under the "Controller: IDE".
5. Start the virtual machine.

This version loads the _display_ output (a pretty gradient).


### Hosted Version

VOL also compiled to 'an app', allowing the standard execution of the runtime in a hosted environment.

Ensure to compile the `app` version before running it.

```sh
$ tool compile app
```

```sh
$ tool run app
VOL hosted test
Kernel version: 0.1.0
Memory routines: OK
Hosted halt called
```

This is hoping to be the same experience as running the kernel, but in a hosted environment.

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
tool run oraclebox
tool lcr
tool cr
```

Typically you'll want to compile and run the display version of the kernel.

```bash
tool c 
tool r vbox # Oracle virtualbox handles a display output
tool run --no-display # QEMU default; headless mode.
```

Short aliases are available as `tool l`, `tool c`, `tool f`, and `tool r`. The `--display` run mode is reserved for a future graphical runner.


## How to use this?

For a Windows setup using WSL2 and Ubuntu, see
[Windows Subsystem for Linux](windows-wsl.md). For a native Windows setup
using MSYS2 and PowerShell helper scripts, see [Windows development](windows.md).

### Dependencies

Any `make` command depends on GNU make (`gmake`) and is expected to be run using it. This usually means using `make` on most GNU/Linux distros, or `gmake` on other non-GNU systems.

All `make all*` targets depend on a GNU-compatible C toolchain capable of generating x86-64 ELF objects. Usually `gcc/binutils` or `clang/llvm/lld` provided by any x86-64 UNIX like (including Linux) distribution will suffice.

Building also requires `git`, used to fetch the kernel's dependencies (see `kernel/get-deps`), `curl`, used to download the Limine release and the EDK2 OVMF firmware images, and a C compiler for the host (`cc` by default, see the `HOST_CC` `make` variable), used to build the `limine` host utility.

Additionally, building an ISO with `make all` requires `xorriso`, and building a HDD/USB image with `make all-hdd` requires `sgdisk` (usually from `gdisk` or `gptfdisk` packages) and `mtools`.

The kernel sources are written in Nim and require the upstream Nim 2.2.12 binary at `$HOME/.local/opt/nim-2.2.12/bin/nim`. `tool c` and `tool c app` download and unpack `nim-2.2.12-linux_x64.tar.xz` from [nim-lang.org](https://nim-lang.org/download/nim-2.2.12-linux_x64.tar.xz) into that directory when it is missing.

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

For a fast hosted development build, run this from `kernel/`:

```sh
nimble buildHosted
./bin/vol-hosted
```

This uses `src/hosted_main.nim` with Nim's normal runtime and exercises the
shared modules without requiring Limine or the freestanding linker.

From the repository root, the hosted workflow is also available through the
`tool` command:

```sh
tool compile app
tool run app
tool arc
tool alcr
```

The `tool compile app` command writes the hosted executable to
`dist/vol-hosted-{version}-{build_count}` and `tool run app` runs the current
filename from the build cache.

The existing commands continue to target the OS build by default. Use `tool
compile`, `tool run`, `tool cr`, or `tool lcr` for the freestanding OS image.

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

### VirtualBox

After compiling an ISO, run `tool run oraclebox` to create or update a
VirtualBox VM named from the kernel version, such as `VOL 0.1.0`, attach the
current ISO, and start it in the VirtualBox GUI. Repeating the command updates
the existing VM instead of creating another one. When `kernel/VERSION` changes,
the runner migrates a single prior `VOL <version>` entry to the new name.
`tool run vbox` is a shorter alias.

This command is intended for WSL with Windows VirtualBox installed. It uses
`VBoxManage.exe` and converts the WSL ISO path for Windows automatically. If
VirtualBox is installed in a non-standard location, add its directory to the
WSL `PATH`.

For a headless launch or VM customization, use the standalone script:

```sh
python tools/run_oraclebox.py --headless
python tools/run_oraclebox.py --name "VOL Debug" --memory 4096 --cpus 4
```

Run `python3 tools/cleanup.py` to remove local build outputs while preserving downloaded dependencies and tools. Use `python3 tools/cleanup.py --hard` to remove those downloaded assets as well.

