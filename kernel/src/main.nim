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
    tell.line("   Date at boot:     ", monotonic.boot_date())
    tell.line("   Frequency:        ", monotonic.tsc_frequency())
    

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

    let umb: uint64 = mem_info.usable_memory_bytes()
    tell.line("Kernel version: ", kernelVersion.get_version())
    tell.line("Usable memory: ", umb, human_bytes.human_bytes(umb))
    # discard umb

    print_allocation_state()
    let singleByteTestResult = mem_test.perform_single_byte_memory_test()
    if singleByteTestResult == 0:
        tell.line("Single byte memory test: OK")
    else:
        tell.line("Single byte memory test: FAILED")
    print_allocation_state()

    # if not gradient.renderAll():
        #     kernelHalt.halt()

    if terminal.init():
        terminal.set_xy(0, 1)
        terminal.write_line("VOL kernel booted")
        terminal.write("Memory routines: ")
        
        terminal.set_text_fg(6, true) # bright cyan
        terminal.write_line("OK")
        terminal.reset_text_fg()
        
        terminal.write_line("Framebuffer terminal: OK")

    kernelHalt.halt()
