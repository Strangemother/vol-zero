simple addition

    mov rax, 5
    inc rax

+ Does not change carry:

    mov al, 255
    inc al

therefore change to

    mov al, 255
    ad al, 1

This time the add al will provide the carry flag.

    inc
    dec

does not change the carry flag. the above will produce an underflow without a carry flag.
A dec with underflag

    mov al, 0
    sub al, 1


===

the API should expose an inc like a standard increment.

    # literal
    asm.inc(reg.ebx)
    # other
    reg.ebx.inc()
    reg.ebx + 1


