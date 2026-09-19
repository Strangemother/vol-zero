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
import core/memory/allocate as mem_allocate
import core/serial
import core/display/gradient
import core/halt as kernelHalt
import core/version as kernelVersion
import core/monotonic

import core/human/bytes_x as human_bytes


proc print_allocation_state() =
    serial.write("Allocation state: ")
    let allocationState = mem_allocate.getAllocationState()
    serial.writeUInt64(allocationState.entryIndex)
    serial.write(" ")
    serial.writeUInt64(allocationState.address)
    serial.write("\r\n")

    
proc print_clock_info() =
    serial.write("Clock:")
    serial.write("\r\n   Monotonic time: ")
    serial.writeUInt64(monotonic.delta())
    serial.write("\r\n   tsc:            ")
    serial.writeUInt64(monotonic.read_tsc64())
    serial.write("\r\n   Date at boot:   ")
    serial.writeUInt64(uint64(monotonic.date_at_boot()))
    serial.write("\r\n   Frequency:      ")
    serial.writeUInt64(monotonic.tsc_frequency())
    serial.write("\r\n")

## VOL through Limine enters the kernel through the C-compatible symbol kmain.
proc kmain() {.exportc: "kmain", noreturn.} =
    serial.init()
    monotonic.record_start()

    print_clock_info()

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
    serial.write("\r\n")
    
    serial.write(human_bytes.human_bytes(mem_info.usableMemoryBytes()))
    serial.write("\r\n")

    print_allocation_state()

    serial.write("Performing single byte memory test\r\n")
    let physical = mem_allocate.allocatePhysicalBytes(mem_allocate.pageSize)
    let bytes = mem_allocate.physicalBytes(physical)

    print_allocation_state()

    if bytes == nil:
        serial.write("Memory allocation or HHDM mapping failed\r\n")
    else:
        bytes[3] = uint8('X')
        if bytes[3] == uint8('X'):
            serial.write("Memory allocation and HHDM mapping succeeded\r\n")
        else:
            serial.write("Memory allocation succeeded but HHDM mapping failed\r\n")
    
    if not gradient.renderAll():
        kernelHalt.halt()

    kernelHalt.halt()
