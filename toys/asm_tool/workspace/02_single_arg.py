"""Instructions with one operand."""

from toys.asm_tool.src.lat import ASM, Reader, Registers


asm = ASM()
reg = Registers()
asm.push(reg.bp)
asm.pop(reg.sp)
asm.ret()

print(Reader(asm).flat_resolve())
