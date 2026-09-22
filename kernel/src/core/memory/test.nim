
include pure
import allocate as mem_allocate

#[
Quick memory test for the VOL kernel.

This test verifies that memory can be copied correctly using memcpy and compared using memcmp.
]#
proc quicktest_memory*(): bool =
    var source = [uint8(1), 2, 3, 4]
    var destination: array[4, uint8]

    discard memcpy(destination.addr, source.addr, csize_t(source.len))

    let comparison = memcmp(source.addr, destination.addr, csize_t(source.len))
    return comparison == 0


proc perform_single_byte_memory_test*(): int =
    let physical = mem_allocate.allocate_physical_bytes(mem_allocate.pageSize)
    let bytes = mem_allocate.physical_bytes(physical)

    if bytes == nil: return 1 # allocation or HHDM mapping failed
    
    bytes[3] = uint8('X')
    if bytes[3] == uint8('X'):
        return 0 # allocation and hhdm mapping succeeded
    else:
        return 1 # allocation succeeded but HHDM mapping failed
