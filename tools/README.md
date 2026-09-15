# Tools for the VOL Bootloader Project

This directory contains various tools and utilities used in the development and testing of the VOL bootloader project.

## Getting Started

Install the `tool` to run the various utilities from the loader. Alternatively each script should run independently.

1. install `tools/app/` to make the application scripts available.
2. run `$ tool -h` to see the available options and commands.

### Install the App

To install the application scripts, navigate to the `tools/app/` directory and run the installation command:

```sh
$ pip install .

# run it.
$ tool -h
```

## General Usage

Generally you'll run:

```sh
# compile run
$ tool cr

# run
$ tool run
```

```
 tool -h
usage: tool [-h] COMMAND ...

Build, clean, and run the Limine kernel template.

positional arguments:
  COMMAND
    cleanup (l)         clean generated build assets
    compile (c)         build a fresh distribution ISO
    first_time (first-time, f)
                        install dependencies, build, and run QEMU
    run (r)             run the compiled ISO
    lcr                 cleanup, compile, then run
    cr                  compile, then run

options:
  -h, --help            show this help message and exit
```


