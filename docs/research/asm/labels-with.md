## functional exposure.

Mixing it up a little, it'd be nice to refer to internal references to apply ASM logic

    item = asm.label('next_char')
    item.mov(reg.AH, 0x0E)
    item.mov(reg.BH, 0x00)
    item.mov(reg.BL, 0x07)
    item.ret()
    asm.call(item)

nice if:

    item = asm.label('next_char', write_here=False)
    asm.call(item)
    with next_char as item.write_here(): # returns self for __enter__
        item.mov(reg.AH, 0x0E)
        item.mov(reg.BH, 0x00)
        item.mov(reg.BL, 0x07)
        item.ret()

creating:

    next_char:
        mov AH, 0x0E
        mov BH, 0x00
        mov BL, 0x07
        ret

    call next_char
