"""Instructions with multiple operands preserve their order."""

from lat import ASM, Reader, Registers, Memory


asm = ASM()
# reg = Registers()
reg = Registers(asm=asm)
# print(reg.eax.mov(10))
# print(Reader(asm).flat_resolve())
# print(str(reg.eax))
reg.eax.mov(10)
# asm.mov(reg.eax, 0x0)
print(Reader(asm).flat_resolve())
