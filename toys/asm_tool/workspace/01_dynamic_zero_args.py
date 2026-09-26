"""Unknown ASM attributes become zero-argument mnemonics."""

from toys.asm_tool.src.lat import ASM, Reader


asm = ASM()
asm.hlt()
asm.pusha()
asm.again()

print(Reader(asm).flat_resolve())
