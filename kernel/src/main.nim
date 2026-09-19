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
import core/terminal
import core/halt as kernelHalt
import core/version as kernelVersion
import core/monotonic
import core/tell

import core/human/bytes_x as human_bytes


proc print_allocation_state() =
    serial.write("Allocation state: ")
    let state = mem_allocate.current_state()
    tell.line(state.entryIndex, state.address)


proc print_clock_info() =
    tell.line("Clock:")
    tell.line("   Monotonic time:   ", monotonic.delta())
    tell.line("   Monotonic time 2: ", monotonic.delta())
    tell.line("   tsc:              ", monotonic.read_tsc64())
    tell.line("   Date at boot:     ", uint64(monotonic.date_at_boot()))
    tell.line("   Frequency:        ", monotonic.tsc_frequency())


proc perform_single_byte_memory_test() =
    tell.line("Performing single byte memory test")
    let physical = mem_allocate.allocate_physical_bytes(mem_allocate.pageSize)
    let bytes = mem_allocate.physical_bytes(physical)

    if bytes == nil:
        tell.line("Memory allocation or HHDM mapping failed")
    else:
        bytes[3] = uint8('X')
        if bytes[3] == uint8('X'):
            tell.line("Memory allocation and HHDM mapping succeeded")
        else:
            tell.line("Memory allocation succeeded but HHDM mapping failed")


## VOL through Limine enters the kernel through the C-compatible symbol kmain.
proc kmain() {.exportc: "kmain", noreturn.} =
    monotonic.record_start()

    serial.init()

    print_clock_info()

    if mem_test.quicktest_memory():
        tell.line("Memory routines: OK")
    else:
        tell.line("Hosted memory check failed")
        kernelHalt.halt()

    tell.line("Kernel version: ", kernelVersion.get_version())
    tell.line(
        "Usable memory: ",
        mem_info.usable_memory_bytes(),
        human_bytes.human_bytes(mem_info.usable_memory_bytes())
    )

    print_allocation_state()
    perform_single_byte_memory_test()
    print_allocation_state()

    # if not gradient.renderAll():
    #     kernelHalt.halt()

    # if terminal.init():
    #     terminal.writeLine("VOL kernel booted")
    #     terminal.writeLine("Memory routines: OK")
    #     terminal.writeLine("Framebuffer terminal: OK")

    kernelHalt.halt()
