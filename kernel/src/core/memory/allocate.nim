#[
Low-level physical memory allocation and HHDM (Higher Half Direct Map) support.

This module has two related responsibilities:

1. Allocate a range of currently usable physical memory.
2. Convert that physical address into a virtual address that the kernel can
   access through a Nim pointer.

A physical address is a number describing a location in RAM. A Nim pointer is
a virtual address that the CPU must translate through page tables. The HHDM is
a bootloader-provided virtual mapping that makes this conversion simple:

    virtual address = physical address + HHDM offset

The physical allocator and HHDM do not provide a general-purpose heap. Memory
returned by this module is not freed, and callers must not access more bytes
than they requested.
]#
type
    PhysicalAddress* = distinct uint64
    VirtualAddress* = distinct uint64
    # The {.bycopy.} annotation
    # is important when Nim receives a C struct by value.
    AllocationState* {.bycopy.} = object
        entryIndex*: uint64
        address*: uint64

const
    ## The x86-64 hardware page size used by the physical allocator.
    pageSize* = 4096'u64


proc getAllocationState*(): AllocationState
    {.importc: "limine_get_allocation_state".}

#[
Resets the physical allocator back to the beginning of the memory map.

Example:

    reset()
    let physical = allocatePhysicalBytes(pageSize)

After the reset, the next allocation may reuse addresses returned before the
reset. Every pointer and physical address allocated before `reset()` must
therefore be considered invalid. Use this only when all earlier allocations
are disposable. This is a whole-arena reset, not an individual deallocator.
]#
proc reset*() {.importc: "limine_allocator_reset".}

#[
Returns a physical address from the C implementation of the Limine-backed
allocator.

This is an internal ABI bridge. Nim code should call `allocatePhysicalBytes`
instead, because that function returns the type-safe `PhysicalAddress` type.

The allocator rounds sizes up to whole pages and returns zero when allocation
fails. The returned address is physical memory, not automatically a Nim
pointer.
]#
proc allocatePhysicalBytesRaw(size: uint64): uint64 {.importc: "limine_allocate_physical".}

#[
Returns the HHDM offset supplied by Limine.

This is an internal ABI bridge. Nim code should normally call `hhdmOffset`
instead. The value must not be guessed or hard-coded because Limine may choose
a different offset on different boots or configurations.
]#
proc hhdmOffsetRaw(): uint64 {.importc: "limine_hhdm_offset".}

#[
Reports whether Limine supplied an HHDM response.

This is an internal ABI bridge. Nim code should call `hhdmAvailable` instead.
The C function returns an integer because that is a simple C ABI
representation of a boolean value.
]#
proc hhdmAvailableRaw(): uint64 {.importc: "limine_hhdm_available".}

#[
Allocates a range of usable physical memory.

Example:

    let physical = allocatePhysicalBytes(pageSize)
    if uint64(physical) == 0:
        serial.write("Allocation failed\r\n")

The allocator rounds `size` up to a multiple of `pageSize`. For example, a
request for 1 byte consumes one 4096-byte page, and a request for 4097 bytes
consumes two pages. A result of zero means that allocation failed.

The returned value is a `PhysicalAddress`, not a dereferenceable pointer. Use
`physicalBytes` after confirming that an HHDM mapping is available. This first
allocator is intentionally simple: it does not free memory and is not safe to
call concurrently from multiple CPUs or interrupt handlers.
]#
proc allocatePhysicalBytes*(size: uint64): PhysicalAddress =
    PhysicalAddress(allocatePhysicalBytesRaw(size))

#[
Returns the HHDM offset selected by Limine.

Example:

    if hhdmAvailable():
        let offset = hhdmOffset()
        serial.writeUInt64(offset)

The offset is added to a physical address to produce the corresponding HHDM
virtual address. Do not use this value unless `hhdmAvailable()` is true. A
zero offset can be valid on some systems, so checking the offset alone is not
a reliable availability test.
]#
proc hhdmOffset*(): uint64 =
    hhdmOffsetRaw()

#[
Reports whether Limine created the HHDM mapping requested by the kernel.

Example:

    if not hhdmAvailable():
        serial.write("HHDM unavailable\r\n")

When this returns `false`, the kernel must not turn physical addresses into
pointers with this module. A physical allocator can still return addresses,
but those addresses need another virtual mapping before they can be read or
written by Nim code.
]#
proc hhdmAvailable*(): bool =
    hhdmAvailableRaw() != 0

#[
Converts a physical address into its HHDM virtual address.

Example:

    let physical = allocatePhysicalBytes(pageSize)
    let virtual = physicalToVirtual(physical, hhdmOffset())

The conversion is only meaningful when `hhdmAvailable()` is true. A zero
physical address is treated as invalid because zero is also the allocator's
failure value. The function returns zero if adding the offset would overflow
the 64-bit address space.

This function returns a `VirtualAddress` number, not a Nim pointer. Use
`physicalBytes` when byte access is required.
]#
proc physicalToVirtual*(physical: PhysicalAddress, offset: uint64): VirtualAddress =
    let address = uint64(physical)
    if address == 0 or offset > high(uint64) - address:
        return VirtualAddress(0)
    VirtualAddress(address + offset)

#[
Returns a byte-array pointer for a physical allocation through the HHDM.

Example:

    let physical = allocatePhysicalBytes(pageSize)
    let bytes = physicalBytes(physical)

    if bytes != nil:
        bytes[3] = uint8('X')

The returned pointer can access the allocated memory through the HHDM. For a
4096-byte allocation, valid indexes are 0 through 4095. Nim does not know the
allocation length because `UncheckedArray` has no bounds checking, so callers
must track the requested size themselves.

This returns `nil` when the physical address is zero or when HHDM is
unavailable. It does not validate that an arbitrary physical address belongs
to an allocation made by this module. The pointer is also unsuitable for
sharing between CPUs until the allocator is made concurrency-safe.
]#
proc physicalBytes*(physical: PhysicalAddress): ptr UncheckedArray[uint8] =
    if not hhdmAvailable():
        return nil
    let virtual = physicalToVirtual(physical, hhdmOffsetRaw())
    if uint64(virtual) == 0:
        return nil
    cast[ptr UncheckedArray[uint8]](uint64(virtual))