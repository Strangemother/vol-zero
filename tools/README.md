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

## Static Site Export

`tool site export` renders the hosted Flask documentation site as static files
for GitHub Pages. By default it reads `github-pages/config.json` when that file
exists.

```sh
tool site export github-pages/config.json
```

The config controls the source `base_url`, output directory, crawl limit,
stylesheet path, manifest filename, and ignored file patterns such as `.git`
folders.

The compatibility command still works from the repository root:

```sh
python convert.py
```

## Nim Documentation Metadata

`nim_docs.py` extracts the project's existing `#[ ... ]#` and `##` comments,
associates them with module-level Nim declarations, and recognizes a multiline
comment beginning on line one as file documentation. It is intended as a source
of metadata for a custom documentation site rather than as a replacement for
Nim's compiler or documentation generator.

Print a summary:

```sh
python tools/nim_docs.py kernel/src/core/display/gradient.nim
```

Emit JSON for one module:

```sh
python tools/nim_docs.py \
  kernel/src/core/display/gradient.nim \
  --json --pretty > gradient.json
```

The parser is also importable by a Flask application:

```python
from tools.nim_docs import parse_nim_source

module = parse_nim_source("kernel/src/core/display/gradient.nim")
page = module.to_dict()
```

The resulting module contains its path, module name, imports, includes,
declarations, visibility, source lines, signatures, and extracted documentation.
Each import/include entry contains its `name`, optional `alias`, source `line`,
and `.nim` `filename`. Indented locals and object fields are ignored so each
result represents a module-level page entry.


