from toys.memory_lab.sim.memory import *

set_memory_limit(2 * PAGE_SIZE)
first = allocate_physical_bytes(PAGE_SIZE)
second = allocate_physical_bytes(PAGE_SIZE)
third = allocate_physical_bytes(1)

assert first == MEMORY_BASE
assert second == MEMORY_BASE + PAGE_SIZE
assert third == 0
print("two pages allocated; third allocation correctly failed")

set_memory_limit(None)
