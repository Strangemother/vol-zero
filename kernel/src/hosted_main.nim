#[
  Hosted development entry point for VOL.

  This file uses the shared memory and version modules without importing
  Limine, serial-port I/O, framebuffer access, or CPU halt instructions. It
  can therefore be compiled as an ordinary Nim application for fast tests.
]#
import core/memory
# import core/serial
# import core/framebuffer
import core/halt as kernelHalt
import core/version


proc main() =
    var source = [uint8(1), 2, 3, 4]
    var destination: array[4, uint8]

    discard memcpy(destination.addr, source.addr, csize_t(source.len))

    let comparison = memcmp(source.addr, destination.addr, csize_t(source.len))
    if comparison != 0:
        quit "Hosted memory check failed"

    echo "VOL hosted test"
    echo "Kernel version: ", get_version()
    echo "Memory routines: OK"
    kernelHalt.halt()

main()
