# Kernel Memory Allocation

This document describes the current low-level memory allocation tools in VOL.
It is written for code that runs inside the kernel, after Limine has entered
the kernel through `kmain`.

The implementation is intentionally small. It can find usable physical memory,
reserve it in page-sized units, and expose that memory through Limine's Higher
Half Direct Map (HHDM). It is not yet a general-purpose heap, a complete
virtual-memory manager, or a reclaimable allocator.

## The Short Version

To allocate one physical page and access it through a Nim pointer:

```nim
import core.memory.allocate as memory_allocate

let physical = memory_allocate.allocatePhysicalBytes(memory_allocate.pageSize)
let bytes = memory_allocate.physicalBytes(physical)

if bytes == nil:
	serial.write("Memory allocation or HHDM mapping failed\r\n")
else:
	bytes[3] = uint8('X')
```

The `physical` value is a physical address. The `bytes` value is a virtual
pointer produced through the HHDM. The distinction matters: a physical address
is a location in RAM, while a pointer is an address the CPU can use after page
tables translate it.

## Address Model

There are two addresses involved in a memory access:

```text
physical address:  0x00100000  location in RAM
virtual address:   0xffff800000100000  address used by a pointer
```

The HHDM is a mapping created by Limine. It makes physical memory visible at a
known virtual offset:

```text
virtual address = physical address + HHDM offset
```

The HHDM offset is selected by Limine and may vary. It must be requested from
Limine and must not be hard-coded.

The kernel is linked in the high half of the virtual address space, as shown in
`kernel/linker-scripts/x86_64.lds`. This is one reason a physical address must
not be assumed to be a directly usable Nim pointer.

## Module API

The Nim interface is in
`kernel/src/core/memory/allocate.nim`.

### `PhysicalAddress`

```nim
type PhysicalAddress* = distinct uint64
```

This type identifies a physical location. It is deliberately distinct from
`uint64`, which makes accidental mixing with ordinary numbers less likely.

Convert it to a number only when crossing a low-level interface or printing it:

```nim
let physical = memory_allocate.allocatePhysicalBytes(4096)
serial.writeUInt64(uint64(physical))
```

This value is not a pointer and should not be dereferenced.

### `VirtualAddress`

```nim
type VirtualAddress* = distinct uint64
```

This type identifies a virtual address. `physicalToVirtual` returns it as a
number so that conversion to a raw pointer is explicit. Most code should use
`physicalBytes` instead of doing that conversion manually.

### `pageSize`

```nim
const pageSize* = 4096'u64
```

This is the x86-64 page size used by the current allocator. Requests are
rounded up to whole pages:

```nim
allocatePhysicalBytes(1)     # consumes 4096 bytes
allocatePhysicalBytes(4096)  # consumes 4096 bytes
allocatePhysicalBytes(4097)  # consumes 8192 bytes
```

The comments above show the allocation sizes conceptually. In Nim, use the
constant through the module:

```nim
let physical = memory_allocate.allocatePhysicalBytes(memory_allocate.pageSize)
```

### `allocatePhysicalBytes`

```nim
proc allocatePhysicalBytes*(size: uint64): PhysicalAddress
```

This reserves `size` bytes from Limine memory-map entries marked
`LIMINE_MEMMAP_USABLE`. The allocator rounds the request up to a multiple of
4096 bytes and returns the first suitable physical address.

```nim
let physical = memory_allocate.allocatePhysicalBytes(4096)

if uint64(physical) == 0:
	serial.write("No usable physical memory\r\n")
```

A return value of zero means allocation failed. Do not use it as a pointer.
The current allocator does not provide `free`, so every successful allocation
remains reserved until reboot. It also keeps a single cursor and is not safe
for concurrent calls from multiple CPUs or interrupt handlers.

The function accepts a byte count, but the underlying unit is a page. For a
page allocator, requesting `pageSize` is usually the clearest choice.

### `hhdmAvailable`

```nim
proc hhdmAvailable*(): bool
```

This reports whether Limine returned an HHDM response.

```nim
if not memory_allocate.hhdmAvailable():
	serial.write("Cannot access physical memory through HHDM\r\n")
```

Do not infer availability from the offset being nonzero. A zero offset could
be a valid mapping on some system. Check this function before converting a
physical address into a pointer.

### `hhdmOffset`

```nim
proc hhdmOffset*(): uint64
```

This returns the offset selected by Limine.

```nim
if memory_allocate.hhdmAvailable():
	let offset = memory_allocate.hhdmOffset()
	serial.writeUInt64(offset)
```

Most callers do not need this function directly. `physicalBytes` obtains and
uses the offset internally. It is useful when building a lower-level mapping
or diagnostic tool.

### `physicalToVirtual`

```nim
proc physicalToVirtual*(
	physical: PhysicalAddress,
	offset: uint64
): VirtualAddress
```

This applies the HHDM formula to a physical address:

```nim
if memory_allocate.hhdmAvailable():
	let physical = memory_allocate.allocatePhysicalBytes(4096)
	let virtual = memory_allocate.physicalToVirtual(
		physical,
		memory_allocate.hhdmOffset()
	)
```

The function returns zero when the physical address is zero or when the
addition would overflow `uint64`. It does not itself check that the physical
address was allocated, that Limine supplied the offset, or that the resulting
address is mapped. Those checks belong to the caller.

For ordinary byte access, prefer `physicalBytes` because it performs the HHDM
availability check and pointer conversion in one place.

### `physicalBytes`

```nim
proc physicalBytes*(
	physical: PhysicalAddress
): ptr UncheckedArray[uint8]
```

This converts a physical address into a byte-array pointer through the HHDM.

```nim
let physical = memory_allocate.allocatePhysicalBytes(4096)
let bytes = memory_allocate.physicalBytes(physical)

if bytes != nil:
	bytes[0] = uint8(0x2A)
	bytes[4095] = uint8(0x7F)
```

For a 4096-byte allocation, indexes `0` through `4095` are valid. The type is
an `UncheckedArray`, so Nim cannot enforce that limit. The caller must retain
the requested size and stay within it:

```nim
let requestedSize = memory_allocate.pageSize
let physical = memory_allocate.allocatePhysicalBytes(requestedSize)
let bytes = memory_allocate.physicalBytes(physical)

if bytes != nil:
	for index in 0'u64 ..< requestedSize:
		bytes[index] = 0
```

The pointer is `nil` when the physical address is zero, HHDM is unavailable,
or the physical-to-virtual conversion fails. It does not validate arbitrary
addresses, track pointer lengths, or make allocation thread-safe.

## How Limine Fits In

The Limine-facing code is in
`kernel/src/ext/limine_requests.c`.

It places two requests in the `.limine_requests` linker section:

1. `memoryMapRequest` asks Limine for the physical memory map.
2. `hhdmRequest` asks Limine for the HHDM offset.

The C bridge then exposes small functions for Nim:

```text
limine_allocate_physical
limine_hhdm_offset
limine_hhdm_available
```

Keeping the Limine structures in C means the project uses the definitions from
Limine's `limine.h` directly. The Nim module presents a smaller, typed
interface to the rest of the kernel.

The allocator walks memory-map entries in their supplied order. It skips every
entry whose type is not `LIMINE_MEMMAP_USABLE`. It aligns the start address,
checks the remaining length, returns the allocation, and advances its cursor.

## Common Mistakes

### Treating a physical address as a pointer

This is unsafe unless an identity mapping is known to exist:

```nim
let physical = memory_allocate.allocatePhysicalBytes(4096)
let wrong = cast[ptr uint8](uint64(physical))
```

Use `physicalBytes(physical)` instead.

### Forgetting allocation failure

Always check for zero or `nil`:

```nim
let physical = memory_allocate.allocatePhysicalBytes(4096)
if uint64(physical) == 0:
	serial.write("Allocation failed\r\n")
else:
	let bytes = memory_allocate.physicalBytes(physical)
```

### Reading past the allocation

The pointer has no length metadata. A 4096-byte allocation does not make
`bytes[4096]` valid. That access is one byte beyond the allocation and may
overwrite another page or fault.

### Allocating before boot information is available

The memory map and HHDM response are supplied by Limine during boot. This
allocator should only be used after the kernel entry point has been called and
the boot protocol responses are available.

### Assuming the allocator can free memory

It cannot yet. The current cursor only moves forward. A future allocator may
use a bitmap, free list, or another structure to recycle pages.

## Current Scope and Next Steps

This implementation is useful for early kernel work, page-table experiments,
and small boot-time structures. It intentionally leaves several larger tasks
for later:

- freeing physical pages;
- tracking allocation ownership and lengths;
- concurrency protection;
- a virtual address-space manager;
- page-table creation and permission flags;
- a heap or small-object allocator above 4096-byte pages.

The natural next layer is a page allocator that returns and frees individual
physical frames. A heap can then divide those frames into smaller allocations.
The virtual-memory manager can eventually replace the HHDM convenience mapping
with explicit mappings and controlled page permissions.
