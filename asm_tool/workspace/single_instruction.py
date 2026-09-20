"""Instructions with multiple operands preserve their order."""

from lat import ASM, Reader, Registers


asm = ASM()
reg = Registers()
asm.mov(reg.eax, 1)
p = asm.add(reg.eax, reg.edx)
print(str(p))
asm.ret()

print(Reader(asm).flat_resolve())
