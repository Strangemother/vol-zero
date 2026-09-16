#[
  Hosted development entry point for VOL.

  This file uses the shared memory and version modules without importing
  Limine, serial-port I/O, framebuffer access, or CPU halt instructions. It
  can therefore be compiled as an ordinary Nim application for fast tests.
]#
# import core/memory/pure
import core/memory/test as mem_test
# import core/serial
# import core/display/gradient
import core/halt as kernelHalt
import core/version as kernelVersion


proc main() =
    if mem_test.quicktest_memory():
        echo "Memory routines: OK"
    else:
        echo "Hosted memory check failed"
        kernelHalt.halt()

    echo "VOL hosted test"
    echo "Kernel version: ", kernelVersion.get_version()

    kernelHalt.halt()

main()
