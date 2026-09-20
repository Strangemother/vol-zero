The compile and translate steps should detect usage and perhaps warn on elements (hard coded)

ARM Setting Condition Flags:

    When using the Thumb instruction set, special attention should be given to the use of 16-bit instruction forms. Many of those (moves, adds, shifts, etc) automatically set the condition flags. For best performance, consider using the 32-bit encodings which include forms that do not set the condition flags, within the bounds of the codedensity requirements of the program

As such when a registry flag is switched, the compiler test can verfiy if the flipped flag was accessed. If not, a warning can suggest an edit for performance. in a compiler phase this may be captured.

    mov al, 10
    # flag flipped

    asm.mov(reg.al, 10)

