# Windows Subsystem for Linux

WSL2 with Ubuntu is the recommended Windows deployment path for this project.
The build uses GNU make, POSIX shell commands, x86-64 ELF tools, xorriso, and
QEMU, so running it inside Linux avoids most Windows shell and path
compatibility problems.

## Install WSL2

Open PowerShell as Administrator and install Ubuntu:

```powershell
wsl --install -d Ubuntu
```

Restart Windows if prompted, then open **Ubuntu** from the Start menu. Create
your Linux username and password when Ubuntu asks for them.

Check that the distribution is using WSL2 from PowerShell:

```powershell
wsl --list --verbose
```

The Ubuntu `VERSION` column should show `2`. If it shows `1`, convert it with:

```powershell
wsl --set-version Ubuntu 2
```

## Install Linux dependencies

Run these commands in the Ubuntu terminal:

```sh
sudo apt update
sudo apt install -y \
  build-essential \
  git \
  curl \
  xorriso \
  qemu-system-x86 \
  gdisk \
  mtools \
  nasm \
  python3 \
  python3-venv \
  python3-pip \
  ca-certificates
```

These packages provide GNU make, the C compiler and linker, Git, the ISO and
disk-image tools, Python, and QEMU. The `gdisk`, `mtools`, and `nasm` packages
are needed by optional HDD/USB-image or assembly workflows.

## Get the source

The build works from a Windows-mounted directory, but WSL filesystem I/O is
usually faster. Prefer cloning inside your Linux home directory:

```sh
mkdir -p ~/src
cd ~/src
git clone <repository-url> vol-zero
cd vol-zero
```

Replace `<repository-url>` with the repository's Git URL. If the repository
already exists on Windows, it can be used directly from a path such as:

```sh
cd /mnt/c/dev/vol-zero
```

## Install Nim 2.2.12

The freestanding kernel requires the upstream Nim 2.2.12 Linux binary. The
project's kernel Makefile expects Nim and Nimble at this exact location:

```text
$HOME/.local/opt/nim-2.2.12/bin
```

Install it in Ubuntu with:

```sh
mkdir -p "$HOME/.local/opt"
curl -fL \
  https://nim-lang.org/download/nim-2.2.12-linux_x64.tar.xz \
  -o /tmp/nim-2.2.12-linux_x64.tar.xz
tar -xJf /tmp/nim-2.2.12-linux_x64.tar.xz \
  -C "$HOME/.local/opt"
```

Verify both commands:

```sh
"$HOME/.local/opt/nim-2.2.12/bin/nim" --version
"$HOME/.local/opt/nim-2.2.12/bin/nimble" --version
```

## Install the project tools

From the repository root, create an optional Python virtual environment and
install the project command:

```sh
python3 -m venv env
. env/bin/activate
python -m pip install -e tools/app
```

The virtual environment is optional, but it keeps the `tool` command isolated
from other Python projects. Reactivate it in a new terminal with:

```sh
cd ~/src/vol-zero
. env/bin/activate
```

## Build and run

From the repository root:

```sh
tool compile
tool run --no-display
```

The first command obtains pinned kernel dependencies, builds the kernel, and
creates a bootable ISO under `dist/`. The second command runs that ISO in QEMU
with serial output in the terminal.

The equivalent Make commands are:

```sh
make all
make run
```

For an HDD image instead of an ISO:

```sh
make all-hdd
make run-hdd
```

## Run in VirtualBox

Install Oracle VirtualBox on Windows, then run this command from WSL after
building the ISO:

```sh
tool run oraclebox
```

The command uses `VBoxManage.exe` to create a VM named from the kernel version,
such as `VOL 0.1.0`, if needed, attach the current ISO, update its memory and
CPU settings, and start it in the VirtualBox GUI. Running it again after a new
build updates the same VM instead of creating a duplicate. When `kernel/VERSION`
changes, the runner migrates a single prior `VOL <version>` entry to the new
name. Use `tool run vbox` as a shorter alias.

For a headless launch or custom VM settings:

```sh
python tools/run_oraclebox.py --headless
python tools/run_oraclebox.py --name "VOL Debug" --memory 4096 --cpus 4
```

VirtualBox configures the guest COM1 port automatically and writes raw serial
output to `vol-serial-<version>.log` in the workspace, regardless of whether
the VM is started with a display or with `--headless`.

To use a live TCP serial console instead, run:

```sh
tool r vbox --headless --serial tcp
tool t
```

The `tool t` command waits for the VirtualBox TCP serial server and streams its
output to the terminal. Use `--serial file` to select raw-file logging.

If `VBoxManage.exe` is installed outside the standard VirtualBox directory,
add its directory to the WSL `PATH` before running the command.

## Existing Windows checkout troubleshooting

If the repository is under `/mnt/c` and `make all` reports:

```text
make: ./kernel/get-deps: No such file or directory
```

normalize the shell script and executable permission once:

```sh
sed -i 's/\r$//' kernel/get-deps
chmod +x kernel/get-deps
```

Then retry:

```sh
make all
```

New checkouts include repository attributes that preserve LF endings for this
script. The top-level Makefile also invokes it through `sh`, so current
checkouts do not depend on the mounted drive preserving executable bits.

## Common checks

Confirm the important tools are available with:

```sh
make --version
cc --version
git --version
xorriso -version
qemu-system-x86_64 --version
"$HOME/.local/opt/nim-2.2.12/bin/nimble" --version
```

Clean generated output while retaining downloaded dependencies:

```sh
python tools/cleanup.py
```

Remove generated output and downloaded dependencies too:

```sh
python tools/cleanup.py --hard
```
