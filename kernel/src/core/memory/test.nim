
include pure

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
