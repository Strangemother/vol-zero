# The `tool` command

Install the project helper from the repository root:

```sh
pip install -e tools/app
```

Common workflows include:

```sh
tool cleanup
tool cleanup --hard
tool compile
tool compile app
tool first_time
tool run
tool run app
tool run --no-display
tool run oraclebox
tool cr
tool lcr
```

Short aliases are available as `tool l`, `tool c`, `tool f`, and `tool r`.
The common kernel workflow is:

```sh
tool c
tool r vbox
tool run --no-display
```

Use `tool install nim`, `tool i nim`, or simply `tool i` to install and
configure the required Nim toolchain without starting a build. This also
links `nim` and `nimble` in `$HOME/.local/bin`; add that directory to `PATH`
when necessary.

The hosted workflow must be compiled before it is run:

```sh
tool compile app
tool run app
```

The executable is written to `dist/vol-hosted-{version}-{build_count}`. The
freestanding OS workflow remains the default for `tool compile`, `tool run`,
`tool cr`, and `tool lcr`. The aliases `tool arc` and `tool alcr` target the
hosted workflow. The `--display` run mode is reserved for a future graphical
runner.