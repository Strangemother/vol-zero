#[
  The kernel version is supplied by the Nimble build task from `../VERSION`.

  `strdefine` makes this value available while compiling Nim code and embeds
  the same string in the kernel, so runtime code does not need to read a file.
]#
const kernelVersion* {.strdefine.} = "unknown"

#[
  Returns the embedded kernel version for runtime consumers such as the serial
  console. The returned `cstring` points to the read-only version string
  compiled into the kernel; callers must not modify it.
]#
proc get_version*(): cstring =
    kernelVersion.cstring
