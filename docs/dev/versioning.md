# Kernel versioning

The canonical kernel version is stored in `kernel/VERSION`. Keep this file to
a single non-empty version string.

The build derives the following values from it:

- Nim package metadata.
- The embedded version in `kernel/src/core/version.nim`.
- Runtime output from `get_version()`.
- Distribution filenames.
- The version in the Limine boot-menu entry.
- The VirtualBox VM name, such as `VOL 0.1.0`.

Update `kernel/VERSION` to bump the version. The other build and runtime values
are generated automatically. The boot-menu name is currently hardcoded as
`VOL` in `limine.conf`.