#[
    Replaces Nim's default panic handler for the freestanding kernel.

    A hosted application can print an error and ask the operating system to
    terminate. A kernel has no operating system available to do that, so this
    handler disables interrupts with `cli` and permanently stops the CPU with
    `hlt`. The `noreturn` pragma tells the compiler that execution never comes
    back to the caller. `message` is currently accepted for API compatibility,
    but this implementation does not display it.

    Example:
        panic("unrecoverable kernel error")
]#
proc panic*(message: string) {.nimcall, noreturn.} =
    while true:
        asm "cli"
        asm "hlt"

#[
    Provides the raw-output hook expected by some Nim runtime paths.

    This freestanding implementation intentionally does nothing. It keeps code
    that requests runtime output linkable without introducing a dependency on a
    hosted terminal or file system. `message` is therefore ignored.

    Example:
        rawoutput("diagnostic text")
]#
proc rawoutput*(message: string) {.nimcall.} =
    discard

