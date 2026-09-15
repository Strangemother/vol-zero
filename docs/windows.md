# Windows development

The supported Windows setup uses [MSYS2](https://www.msys2.org/) for the
POSIX build environment. The repository's Makefiles use GNU make recipes such
as `sed`, `rm`, `cp`, `dd`, and `tar`; running them from plain PowerShell or
from `cmd.exe` will not provide those commands consistently.

## Install list

Install these items on the Windows host:

| Component | Why it is needed |
| --- | --- |
| Git for Windows | Fetches the repository and kernel dependencies. |
| Python 3.10 or newer | Runs the project helper scripts and the `tool` command. |
| MSYS2 | Provides Bash, GNU make, core POSIX utilities, and the Unix-style build environment. |
| QEMU for Windows | Runs the generated x86-64 ISO. |
| Nim 2.2.12 | Builds the freestanding Nim kernel sources. Install/configure it separately; this guide intentionally does not automate the Nim toolchain. |

During MSYS2 installation, use the **UCRT64** environment. Open the
**MSYS2 UCRT64** terminal and install the build-side packages:

```sh
pacman -Syu
pacman -S --needed \
  base-devel \
  mingw-w64-ucrt-x86_64-gcc \
  mingw-w64-ucrt-x86_64-binutils \
  mingw-w64-ucrt-x86_64-nasm \
  mingw-w64-ucrt-x86_64-xorriso \
  mingw-w64-ucrt-x86_64-qemu \
  git curl
```

If a package is unavailable in the UCRT64 repository, install the equivalent
package from the MSYS2 repository and keep that command available on `PATH`.
The build also downloads Limine and OVMF automatically through `curl`.

For the optional `make all-hdd` target, install these additional MSYS2
packages if they are available for your environment:

```sh
pacman -S --needed gdisk mtools
```

The HDD image target is optional. ISO builds only require the tools listed in
the first package command.

## Python helper installation

From PowerShell at the repository root:

```powershell
python -m pip install -e .\tools\app
```

The `tool` command is convenient for hosted builds and for launching the
compiled image, but the Windows wrappers below do not require the package to
be installed.

## Build and run

From PowerShell at the repository root:

```powershell
.\tools\windows\build.ps1
.\tools\windows\run.ps1
```

The first command runs `make all` inside MSYS2 and produces the ISO under
`dist\`. The second command runs the most recently named ISO headlessly in
QEMU, with serial output in the current terminal. Use the graphical QEMU
runner instead with:

```powershell
.\tools\windows\run.ps1 -Display
```

Useful alternatives:

```powershell
.\tools\windows\build.ps1 -Target all-hdd
.\tools\windows\clean.ps1
.\tools\windows\clean.ps1 -Hard
```

The wrappers default to `C:\msys64`. Override it when MSYS2 is installed in a
different location:

```powershell
.\tools\windows\build.ps1 -MsysRoot D:\msys64
```

## Nim note

The current kernel Makefile expects the Nim/Nimble installation at the path
used by the existing Linux workflow (`$HOME/.local/opt/nim-2.2.12/bin`). The
Windows wrappers do not alter that toolchain or hide this requirement. Before
building, configure the Nim installation in the MSYS2 environment so that
`nim` and `nimble` resolve at the path expected by `kernel/GNUmakefile`.
