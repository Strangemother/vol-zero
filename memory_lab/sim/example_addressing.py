from memory import *

reset()
address = allocate_physical_bytes(8)

write(address, b"VOL\x00")
write_byte(address + 4, 0x2A)
memset(address + 5, 0xFF, 3)

assert read(address, 8) == b"VOL\x00\x2A\xFF\xFF\xFF"
assert physical_bytes(address)[4] == 0x2A
print(read(address, 8))
