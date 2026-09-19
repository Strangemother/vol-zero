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
import core/tell

import core/human/bytes_x as human_bytes


proc print_allocation_state() =
    serial.write("Allocation state: ")
    let allocationState = mem_allocate.getAllocationState()
    tell.line(allocationState.entryIndex, allocationState.address)


proc print_clock_info() =
    tell.line("Clock:")
    tell.line("   Monotonic time:   ", monotonic.delta())
    tell.line("   Monotonic time 2: ", monotonic.delta())
    tell.line("   tsc:              ", monotonic.read_tsc64())
    tell.line("   Date at boot:     ", uint64(monotonic.date_at_boot()))
    tell.line("   Frequency:        ", monotonic.tsc_frequency())


proc perform_single_byte_memory_test() =
    serial.write("Performing single byte memory test\r\n")
    let physical = mem_allocate.allocatePhysicalBytes(mem_allocate.pageSize)
    let bytes = mem_allocate.physicalBytes(physical)

    if bytes == nil:
        serial.write("Memory allocation or HHDM mapping failed\r\n")
    else:
        bytes[3] = uint8('X')
        if bytes[3] == uint8('X'):
            serial.write("Memory allocation and HHDM mapping succeeded\r\n")
        else:
            serial.write("Memory allocation succeeded but HHDM mapping failed\r\n")
    

## VOL through Limine enters the kernel through the C-compatible symbol kmain.
proc kmain() {.exportc: "kmain", noreturn.} =
    monotonic.record_start()

    serial.init()

    print_clock_info()

    if mem_test.quicktest_memory():
        serial.write("Memory routines: OK\r\n")
    else:
        serial.write("Hosted memory check failed\r\n")
        kernelHalt.halt()

    tell.line("Kernel version: ", kernelVersion.get_version())
    tell.line(
        "Usable memory: ", 
        mem_info.usableMemoryBytes(),
        human_bytes.human_bytes(mem_info.usableMemoryBytes())
    )

    print_allocation_state()    
    perform_single_byte_memory_test()
    print_allocation_state()

    if not gradient.renderAll():
        kernelHalt.halt()

    kernelHalt.halt()
