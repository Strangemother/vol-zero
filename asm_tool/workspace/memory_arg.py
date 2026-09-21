"""Instructions with multiple operands preserve their order."""

from lat import ASM, Reader, Registers, Memory


asm = ASM()
reg = Registers()

# identical
asm.mov([reg.eax], 1)
asm.mov(Memory("eax"), 1)
asm.mov(Memory(reg.eax), 1)

print(Reader(asm).flat_resolve())
