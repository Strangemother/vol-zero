# VOL Zero

VOL is a minimal x86-64 operating system kernel built with Nim and the Limine
bootloader. The project supports both freestanding kernel builds and a hosted
build that exercises shared runtime modules as a normal application.

The repository produces:

1. A minimal x86-64 VOL kernel image.
2. A hosted VOL application for development and testing.

## Quick start

> One shot tool ` tool c; tool r vbox --serial tcp; tool t` [read more here](tool.md)

For the fastest setup, use the convenience tool to build and run the kernel.

```sh
# install the convenience tool
pip install -e tools/app
tool -h
```

You may need to install the core libs for the os:

```sh
# installs dependencies, builds, and runs QEMU
tool first-time
```

You can always just _compile and run_:

```sh
# compile and run QEMU
tool cr
```

Or, if you prefer a graphical interface,
start VirtualBox (also with TCP serial output):

```sh
# Run VirtualBox with TCP serial output
tool r vbox --serial tcp
# tail the serial output
tool t 
```

This command runs Oracle VirtualBox with the most recent kernel image.

See [Running the kernel](running.md) for display, UEFI, HDD, and VirtualBox
options.

## Important information

- The freestanding kernel requires Nim 2.2.12.
- Run build commands from the repository root unless a page says otherwise.
- The default output is an ISO for QEMU or VirtualBox. HDD/USB images are also
  available.
- The `tool` command wraps the common build, run, cleanup, and hosted workflows.

For platform-specific setup, see [Windows Subsystem for Linux](windows-wsl.md)
or [Windows development with MSYS2](windows.md).

## Documentation

- [Running the kernel](running.md): run the ISO with QEMU or VirtualBox.
- [The `tool` command](tool.md): install and use the project helper.
- [Build dependencies and usage](dev/build.md): dependencies, hosted builds,
  toolchain selection, Makefile targets, and cleanup.
- [Kernel versioning](dev/versioning.md): update and consume the canonical version.
- [License and links](license.md): project license and upstream references.