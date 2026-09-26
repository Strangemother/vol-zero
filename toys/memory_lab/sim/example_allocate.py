from toys.memory_lab.sim.memory import *

reset()
first = allocate_physical_bytes(1)
second = allocate_physical_bytes(PAGE_SIZE + 1)

assert first == MEMORY_BASE
assert second == first + PAGE_SIZE
print(f"one byte allocation: 0x{first:x}")
print(f"two page allocation: 0x{second:x}")
