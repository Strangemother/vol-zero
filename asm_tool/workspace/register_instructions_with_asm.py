"""Instructions with multiple operands preserve their order."""

from lat import ASM, Reader, Registers, Memory


asm = ASM()
reg = Registers(asm=asm)

reg.eax.mov(10)
reg.eax.mov(reg.ebx)
reg.eax.inc()
reg.eax.add(5)

reg.eax.mov(0)                  # falsy immediate
reg.eax.mov(Memory(reg.ebx))    # register <- memory

reg.eax.add(reg.ebx)            # register source
reg.eax.sub(1)                  # arithmetic immediate
reg.eax.xor(reg.ebx)            # register logic
reg.eax.cmp(10)                 # comparison
reg.eax.test(reg.ebx)            # flags-only operation

print(Reader(asm).flat_resolve())
