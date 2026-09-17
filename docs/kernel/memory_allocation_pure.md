# Pure Memory Operations

This document explains how the kernel's pure memory functions work with the
physical allocator. The functions are in
`kernel/src/core/memory/pure.nim`.

The word "pure" here means that these functions manipulate memory that already
exists. They do not find free RAM and they do not create pointers. Allocation
and access are separate steps:

```text
allocatePhysicalBytes -> reserves physical memory
physicalBytes         -> gives access through the HHDM
memset/memcpy/...      -> read or modify that accessible memory
```

## Complete Example

This example allocates one page, clears it, writes a source buffer into it,
and checks the copied bytes.

```nim
import core/memory/allocate as memory_allocate
import core/memory/pure as memory_pure

let pageSize = memory_allocate.pageSize
let physical = memory_allocate.allocatePhysicalBytes(pageSize)
let bytes = memory_allocate.physicalBytes(physical)

if bytes == nil:
    serial.write("Could not access allocated memory\r\n")
else:
    discard memory_pure.memset(bytes, 0, csize_t(pageSize))

    var source: array[4, uint8] = [1, 2, 3, 4]
    discard memory_pure.memcpy(bytes, source.addr, csize_t(source.len))

    let result = memory_pure.memcmp(bytes, source.addr, csize_t(source.len))
    if result == 0:
        serial.write("Memory copied successfully\r\n")
```

The page is 4096 bytes, but only the first four bytes are used for the source
buffer. The remaining bytes are still part of the allocation and were cleared
by `memset`.

## `memset`: Fill Memory

`memset` writes the same byte value repeatedly:

```nim
proc memset*(destination: pointer, value: cint, size: csize_t): pointer
```

Example:

```nim
var buffer: array[8, uint8]
discard memory_pure.memset(buffer.addr, 0, csize_t(buffer.len))
```

Every byte in `buffer` becomes zero. To fill a page obtained from the
allocator:

```nim
let physical = memory_allocate.allocatePhysicalBytes(memory_allocate.pageSize)
let bytes = memory_allocate.physicalBytes(physical)

if bytes != nil:
    discard memory_pure.memset(
        bytes,
        0,
        csize_t(memory_allocate.pageSize)
    )
```

`value` is treated as a byte. Only its lowest eight bits are written. The
function does not check the destination length, so `size` must not be larger
than the memory available at `destination`.

`memset` is commonly used to initialize newly allocated memory, but it does not
perform the allocation itself.

## `memcpy`: Copy Non-Overlapping Memory

`memcpy` copies a specified number of bytes from a source to a destination:

```nim
proc memcpy*(destination: pointer, source: pointer, size: csize_t): pointer
```

Example with ordinary Nim arrays:

```nim
var source: array[4, uint8] = [10, 20, 30, 40]
var destination: array[4, uint8]

discard memory_pure.memcpy(
    destination.addr,
    source.addr,
    csize_t(source.len)
)
```

Example copying into an allocated page:

```nim
let physical = memory_allocate.allocatePhysicalBytes(memory_allocate.pageSize)
let bytes = memory_allocate.physicalBytes(physical)
var source: array[4, uint8] = [10, 20, 30, 40]

if bytes != nil:
    discard memory_pure.memcpy(bytes, source.addr, csize_t(source.len))
```

The source and destination must not overlap. Use `memmove` when they may refer
to overlapping parts of the same allocation. Both regions must be valid for at
least `size` bytes, and the destination must be writable.

## `memmove`: Copy Overlapping Memory

`memmove` copies bytes safely when the source and destination overlap:

```nim
proc memmove*(destination: pointer, source: pointer, size: csize_t): pointer
```

For example, this shifts the contents of a buffer one byte to the right:

```nim
var buffer: array[5, uint8] = [1, 2, 3, 4, 5]

discard memory_pure.memmove(
    buffer[1].addr,
    buffer[0].addr,
    csize_t(4)
)
```

After the move, the buffer contains:

```text
[1, 1, 2, 3, 4]
```

The implementation chooses a safe copy direction based on the addresses. As
with `memcpy`, it cannot determine the size of the regions, so the caller must
supply a valid byte count.

## `memcmp`: Compare Memory

`memcmp` compares two byte regions:

```nim
proc memcmp*(first: pointer, second: pointer, size: csize_t): cint
```

Example:

```nim
var left: array[3, uint8] = [1, 2, 3]
var right: array[3, uint8] = [1, 2, 4]

let result = memory_pure.memcmp(
    left.addr,
    right.addr,
    csize_t(left.len)
)

if result == 0:
    serial.write("Memory is equal\r\n")
else:
    serial.write("Memory is different\r\n")
```

The result has three possible meanings:

```text
result == 0  both regions are equal
result < 0   the first differing byte is smaller in first
result > 0   the first differing byte is larger in first
```

Only the sign is important. Do not depend on the exact nonzero value.

## Pointer and Size Rules

These functions receive `pointer`, so Nim cannot infer the size of the memory.
The `size` argument is the caller's responsibility.

For one allocated page:

```nim
let size = memory_allocate.pageSize
let physical = memory_allocate.allocatePhysicalBytes(size)
let bytes = memory_allocate.physicalBytes(physical)

if bytes != nil:
    bytes[0] = 1
    bytes[4095] = 2
```

This is invalid:

```nim
bytes[4096] = 3
```

Index 4096 is one byte beyond a 4096-byte page. An out-of-bounds access may
corrupt another allocation or cause a fault. The `UncheckedArray` type does not
perform bounds checking.

Also remember that a physical address is not itself a pointer. Always obtain a
pointer through `physicalBytes` or another valid virtual mapping before using
these functions.

## Reset and Lifetime

The current allocator supports a whole-arena reset:

```nim
memory_allocate.reset()
```

After reset, future allocations may reuse physical addresses returned earlier.
Every pointer and physical address obtained before reset must therefore be
considered invalid. Do not run `memcpy`, `memset`, `memmove`, or `memcmp` on
those old pointers after reset.

The pure functions do not track ownership or lifetime. They operate only on the
addresses supplied by the caller.

## Choosing the Function

Use the operation that matches the situation:

```text
initialize a region       memset
copy separate regions     memcpy
copy overlapping regions  memmove
compare regions           memcmp
```

A useful mental model is:

```text
allocation answers: "Which memory may I use?"
HHDM answers:       "Which pointer can access it?"
pure functions answer: "What should I do with those bytes?"
```

These functions are low-level building blocks. Higher-level allocators can use
them later for page metadata, bitmaps, free lists, and heap objects.
