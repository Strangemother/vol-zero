#[
    Main kernel entry point for the VOL bootloader.

    Initializes serial communication, sets up the framebuffer,
    and halts the CPU if necessary.
]#

# Memory is included as low-level C ABI support; the other modules are
# imported for organization and namespacing, not as a runtime performance choice.
# include core/memory/pure
import core/memory/test as mem_test
import core/memory/info as mem_info
import core/serial
import core/display/gradient
import core/halt as kernelHalt
import core/version as kernelVersion

import core/human/bytes_x as human_bytes

# VOL through Limine enters the kernel through the C-compatible symbol kmain.
proc kmain() {.exportc: "kmain", noreturn.} =
    serial.init()

    if mem_test.quicktest_memory():
        serial.write("Memory routines: OK\r\n")
    else:
        serial.write("Hosted memory check failed\r\n")
        kernelHalt.halt()

    serial.write("Kernel version: ")
    serial.write(kernelVersion.get_version())
    serial.write("\r\n")

    serial.write("Usable memory: ")
    serial.writeUInt64(mem_info.usableMemoryBytes())

    serial.write(human_bytes.human_bytes(mem_info.usableMemoryBytes()))
    serial.write("\r\n")

    if not gradient.renderAll():
        kernelHalt.halt()

    kernelHalt.halt()
