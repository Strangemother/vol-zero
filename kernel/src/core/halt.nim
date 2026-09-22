#[
  Stops execution permanently.

  The `hlt` instruction places the CPU in a halted state until an interrupt
  arrives. Because interrupts are not disabled here, an interrupt could wake
  the CPU and allow the loop to execute again; the loop makes the halt state
  permanent from the kernel's point of view. The `noreturn` pragma documents
  that this procedure never returns to its caller.

  Use this for an unrecoverable boot failure or when the kernel has completed
  its work and has no scheduler or idle loop to run.

  Example:
    
    halt()
]#


when defined(freestanding):
    #[  In kernel mode, calling `hlt` in a loop halts the CPU permanently. ]#
    proc halt*() {.noreturn.} =
        while true:
            asm "hlt"
else:
    #[  In hosted mode, we simply call app exit `quit`. ]#
    proc halt*() =
        quit "Hosted halt called"
