# Call

The call statement binds to a functional call in ASM They may be applied literally, or magically using the asm lib

## Literal

Use the literal functions to print explicit ASM lines.

    asm.call('mylabel')
    lasm = asm.label('mylabel')
    lasm.push(reg.ebp)
    lasm.pop(reg.ebp)
    lasm.ret()

producing:

    call mylabel
    mylabel:
        push ebp
        pop ebp
        ret


## Magic

Apply the call subroutine execution code within a python function and reference. The asm subroutine is applied to the output ASM file automatically

    @asm.label('mylabel')
    def pushpop():
        lasm.push(reg.ebp)
        lasm.pop(reg.ebp)
        lasm.ret()

    asm.call(pushpop)
