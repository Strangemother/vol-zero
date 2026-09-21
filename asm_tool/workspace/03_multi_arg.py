"""Instructions with multiple operands preserve their order."""

from lat import ASM, Reader, Registers


asm = ASM()
reg = Registers()
asm.mov(reg.eax, 1)
asm.add(reg.eax, reg.edx)
asm.ret()

print(Reader(asm).flat_resolve())
