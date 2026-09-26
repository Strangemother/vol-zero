from toys.memory_lab.sim.memory import *

configure_memory([
    (0x1000, PAGE_SIZE * 2),
    (0x9000, PAGE_SIZE),
])

first = allocate_physical_bytes(PAGE_SIZE)
second = allocate_physical_bytes(PAGE_SIZE)
third = allocate_physical_bytes(PAGE_SIZE)

assert (first, second, third) == (0x1000, 0x2000, 0x9000)

write(first, b"abcd")
memmove(first + 1, first, 3)
assert read(first, 4) == b"aabc"
assert memcmp(first, first, 4) == 0

reset()
assert allocate_physical_bytes(PAGE_SIZE) == first
assert read(first, 4) == b"aabc"  # reset moves the cursor, not the bytes

set_hhdm(available=False)
assert physical_bytes(first) is None
set_hhdm(available=True)
assert physical_to_virtual(first) == first + hhdm_offset()

print("memory-map, reset, copy, and HHDM behavior passed")