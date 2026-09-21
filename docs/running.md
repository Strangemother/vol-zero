# Running the kernel

Build the kernel before running it. The default output is a bootable ISO; an
HDD image can also be built for a hard disk or USB drive.

## QEMU

Run the kernel with a graphical display:

```sh
tool run
```

For headless mode with serial output in the terminal:

```sh
tool run --no-display
```

The headless runner prints kernel output and the kernel version. The equivalent
Make targets are `make run` and `make run-uefi` when UEFI firmware is needed.

## VirtualBox

After compiling an ISO, run:

```sh
tool run oraclebox
```

The command creates or updates a VirtualBox VM named from the kernel version,
attaches the current ISO, and starts the GUI. `tool run vbox` is a shorter
alias. When `kernel/VERSION` changes, the runner migrates one previous
`VOL <version>` VM to the new name.

The graphical VM displays the kernel's display output, including its gradient
test screen.

This workflow is intended for WSL with Windows VirtualBox installed. It uses
`VBoxManage.exe` and converts the WSL ISO path automatically. Add the
VirtualBox directory to the WSL `PATH` if it is installed in a non-standard
location.

For a headless launch or custom VM settings:

```sh
python tools/run_oraclebox.py --headless
python tools/run_oraclebox.py --name "VOL Debug" --memory 4096 --cpus 4
```

VirtualBox COM1 logging defaults to `vol-serial-<version>.log`. To stream
serial output over TCP instead:

```sh
tool r vbox --headless --serial tcp
tool t
```

Use `--serial file` to select raw-file mode explicitly.