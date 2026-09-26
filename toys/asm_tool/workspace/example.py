from toys.asm_tool.src.lat import ASM, Reader, Registers

asm = ASM()
reg = Registers()
asm.mov(1, to=reg.eax)
# asm.ret()

print(Reader(asm).flat_resolve())