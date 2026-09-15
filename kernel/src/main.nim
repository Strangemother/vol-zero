#[
  Main kernel entry point for the VOL bootloader.

  Initializes serial communication, sets up the framebuffer,
  and halts the CPU if necessary.
]#

# Memory is included as low-level C ABI support; the other modules are
# imported for organization and namespacing, not as a runtime performance choice.
include core/memory
import core/serial
import core/framebuffer
import core/halt as kernelHalt
import core/version as kernelVersion


# VOL through Limine enters the kernel through the C-compatible symbol kmain.
proc kmain() {.exportc: "kmain", noreturn.} =
    serial.init()
    serial.write("Kernel version: ")
    serial.write(kernelVersion.get_version())
    serial.write("\r\n")
    if not framebuffer.renderAll():
        kernelHalt.halt()
    kernelHalt.halt()
