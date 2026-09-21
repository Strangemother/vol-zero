"""Unknown ASM attributes become zero-argument mnemonics."""

from lat import ASM, Reader


asm = ASM()
asm.hlt()
asm.pusha()
asm.again()

print(Reader(asm).flat_resolve())
