The magic statements help bridge ASM and python without the user getting involved.

## Decorator

Decororate a functional statement to encompass logic as executable ASM. This means coverting the literal python to literal ASM.

During standard execution the ASM is generated through specific functional calls, to generate a tree of compiled lines. This parsing doesn't include python statements. Essentially a file writer... To bridge this, decorating code will enact a magic convertor, reading python code as ASM logic and generating the correct ASM lines.

    if reg.ax == 1:
        asm.mov(reg.ax, 10)

In the above case, the `if` statement is inert to the ASM output, therefore this attempts a compilation tests on the ax value (not recommended). As an alternative:

    @magic
    def move_ax():
        if reg.ax == 1:
            asm.move(rex.ax, 10)

In this example the function is flagged to compile all the logic as ASM. This will result is more ASM lines than the expected `mov` statement; as the `if` will use full operand and jump execution testing.


