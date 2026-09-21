At points you can use python to produce asm.

    mov eax, [ebp+8]
    mov esi, [ebp+12]
    mov edi, [ebp+16]

The following ASM can be a for loop:

    regs = [reg.eax, 'esi', reg.edi]
    for index, reg in enumerate(regs):
        i = 8 + (4 * index)
        asm.mov(reg, value_of=reg.ebp + i)
