clearing a register can be doen with mov

    mov rcx, -1

but xor is faster

    xor rcx, rcx

asm block:

    asm.xor(reg.rcx)

xor against none can be the same register.

    sub ax, ax

+ if you NOT the result of an XOR you get an equals.
