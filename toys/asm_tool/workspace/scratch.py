asm.mov(10, to=registers.eax)
asm.mov(destination="eax", source=10)
registers.eax.set(10)

# Expected normalized output for each caller:
# mov eax, 10
# mov eax, 10
# mov eax, 10

# Additional call forms from mov.md:
asm.mov(registers.eax, 10)
asm.mov("eax", 10)
asm.mov(value=10, into=registers.eax)
asm.mov(value=10, into="eax")
asm.mov(registers.eax, registers.edx)
registers.eax.mov(10)
move(10, into=registers.eax)
asm.mov(Memory("eax"), Immediate(10))
asm.raw("mov eax, 10")
