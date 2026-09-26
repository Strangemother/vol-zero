"""Raw text and lazy register lookup."""

from toys.asm_tool.src.lat import ASM, RawInstruction, Reader, Registers


asm = ASM()
reg = Registers()
asm.install_instruction(RawInstruction)
asm.raw("mov eax, 1")
asm.raw("add $12, %eax")
asm.pop(reg.BP)
asm.ret()

print(Reader(asm).flat_resolve())
