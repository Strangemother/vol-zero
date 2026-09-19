#[
  Freestanding memory manipulation routines for the Limine kernel.
  Provides implementations of memcpy, memset, memmove, and memcmp.

  Note: For VOL. these are reserved for the core machine and potentially a stepper.
  
]#

when defined(freestanding):
    {.pragma: memoryExport, exportc.}
else:
    {.pragma: memoryExport.}


#[
  Sugar for converting pointers to unsigned integers.

  Converts a raw pointer to an unsigned integer containing its address.

  This is a template rather than a runtime procedure: Nim substitutes the
  `cast[uint]` expression at the call site. It makes the purpose of the cast
  easier to read while preserving the same low-level behavior.
]#
template pointer_to_uint(address: pointer): uint =
    cast[uint](address)


template pointer_to_byte_array(address: pointer): ptr UncheckedArray[uint8] =
    # cast[ptr UncheckedArray[uint8]](...) views that address as a pointer to an array of bytes.
    cast[ptr UncheckedArray[uint8]](address)


#[
  Copies `size` bytes from a source byte array to a destination byte array in
  forward order. The pointers do not contain length information, so `size`
  tells the template how many byte positions are valid to access.
]#
template copy_bytes_forward(source, destination: ptr UncheckedArray[uint8], size: csize_t) =
    for index in 0 ..< int(size):
        destination[index] = source[index]


template copy_bytes_backward(
    source, destination: ptr UncheckedArray[uint8],
    size: csize_t
) =
    var index = int(size)
    while index > 0:
        dec index
        destination[index] = source[index]

        
#[
   Copies `size` bytes from `source` to `destination`.
  
   The memory regions must not overlap. If they overlap, the copy order used
   by `memcpy` can overwrite source bytes before they are read; use `memmove`
   when overlapping regions are possible.
  
   `destination` must refer to a writable region of at least `size` bytes,
   and `source` must refer to a readable region of at least `size` bytes.
   A `size` of zero performs no memory access. The procedure returns the
   original `destination` pointer, matching the C `memcpy` contract.

   Example:
       
     var source = [uint8(1), 2, 3, 4]
     var destination: array[4, uint8]
     discard memcpy(destination.addr, source.addr, csize_t(source.len))
]#
proc memcpy*(destination: pointer, source: pointer, size: csize_t): pointer {.memoryExport.} =
    let destinationBytes = pointer_to_byte_array(destination)
    let sourceBytes = pointer_to_byte_array(source)
    copy_bytes_forward(sourceBytes, destinationBytes, size)
    return destination


#[
  Fills the first `size` bytes of `destination` with `value`.
  
  Only the low eight bits of `value` are written to each byte, because the
  destination is a byte array. `destination` must refer to a writable region
  of at least `size` bytes. A `size` of zero performs no memory access. The
  procedure returns the original `destination` pointer, matching the C
  `memset` contract.

   Example:
       
     var buffer: array[8, uint8]
     discard memset(buffer.addr, 0, csize_t(buffer.len))
]#
proc memset*(destination: pointer, value: cint, size: csize_t): pointer {.memoryExport.} =
    let destinationBytes = pointer_to_byte_array(destination)
    for index in 0 ..< int(size):
        destinationBytes[index] = uint8(value)
    return destination

    
#[
  Copies `size` bytes from `source` to `destination`, safely handling overlap.

  When the destination begins before the source, bytes are copied from low to
  high addresses. When the destination begins after the source, bytes are
  copied from high to low addresses so that unread source bytes are preserved.
  If both pointers are equal, no copying is necessary. `destination` must be
  writable and `source` readable for the requested range; the procedure
  returns the original `destination` pointer, matching the C `memmove`
  contract.

   Example:
       
     var source = [uint8(10), 20, 30, 40]
     var destination: array[4, uint8]
     discard memmove(destination.addr, source.addr, csize_t(source.len))
]#
proc memmove*(destination: pointer, source: pointer, size: csize_t): pointer {.memoryExport.} =
    # destination is a raw pointer, so Nim does not know what data it points to.
    let destinationAddress = pointer_to_uint(destination)
    let sourceAddress = pointer_to_uint(source)

    let destinationBytes = pointer_to_byte_array(destination)
    let sourceBytes = pointer_to_byte_array(source)

    # Copy forward when destination starts lower; otherwise copy backward so
    # overlapping writes cannot overwrite source bytes not yet read.
    if sourceAddress > destinationAddress:
        copy_bytes_forward(sourceBytes, destinationBytes, size)
    elif sourceAddress < destinationAddress:
        copy_bytes_backward(sourceBytes, destinationBytes, size)
    return destination

    
#[
  Compares the first `size` bytes at `first` and `second` lexicographically.

  Bytes are compared as unsigned values, from low to high addresses. The
  procedure returns a negative value when the first differing byte in `first`
  is smaller, a positive value when it is larger, and zero when all `size`
  bytes are equal. Callers should rely on the sign of a nonzero result rather
  than on its exact magnitude. Both pointers must refer to readable regions
  of at least `size` bytes; a `size` of zero returns zero without reading.

   Example:
       
     var left = [uint8(1), 2, 3]
     var right = [uint8(1), 2, 4]
     let comparison = memcmp(left.addr, right.addr, csize_t(left.len))
     # comparison is negative because 3 is less than 4.
]#
proc memcmp*(first: pointer, second: pointer, size: csize_t): cint {.memoryExport.} =
    let firstBytes = pointer_to_byte_array(first)
    let secondBytes = pointer_to_byte_array(second)
    for index in 0 ..< int(size):
        if firstBytes[index] != secondBytes[index]:
            return if firstBytes[index] < secondBytes[index]: -1 else: 1
    return 0
