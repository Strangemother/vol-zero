#[ Limine's identifier for a 32-bit RGB framebuffer. ]#
const LimineFramebufferRgb = 1'u8

#[
  These objects mirror the field order, sizes, and alignment of the matching
  structures in Limine's `limine.h`.

  Limine fills these structures before transferring control to the kernel. The
  Nim code reads that existing memory through pointers, so changing a field's
  type or order would make later fields appear at the wrong addresses and
  break the C/Nim ABI. The framebuffer `address` points to pixel memory,
  `pitch` is the number of bytes between rows, and the mask fields describe
  where each color channel belongs inside a pixel.
]#
type
    LimineFramebuffer = object
        address: pointer
        width: uint64
        height: uint64
        pitch: uint64
        bpp: uint16
        memoryModel: uint8
        redMaskSize: uint8
        redMaskShift: uint8
        greenMaskSize: uint8
        greenMaskShift: uint8
        blueMaskSize: uint8
        blueMaskShift: uint8
        unused: array[7, uint8]
        edidSize: uint64
        edid: pointer
        modeCount: uint64
        modes: pointer

    LimineFramebufferResponse = object
        revision: uint64
        framebufferCount: uint64
        framebuffers: ptr ptr LimineFramebuffer

    LimineFramebufferRequest = object
        id: array[4, uint64]
        revision: uint64
        response: ptr LimineFramebufferResponse

#[
  The request objects themselves are declared in `ext/limine_requests.c`.

  Importing them keeps Limine's official request identifiers and linker-section
  placement in C, where the Limine headers define them. `volatile` tells the
  compiler that these values come from externally populated memory and must be
  read rather than optimized away as ordinary unused variables.
]#
var framebufferRequest {.importc: "framebufferRequest", volatile.}: LimineFramebufferRequest
var limineBaseRevision {.importc: "limineBaseRevision", volatile.}: array[3, uint64]

#[
  Converts an 8-bit color channel to the framebuffer's channel range and moves
  it into the channel's bit position.

  For example, a five-bit channel has values from 0 to 31 rather than 0 to
  255. The multiplication and division preserve relative brightness while the
  left shift places the result in the packed pixel.
]#
proc framebufferChannel(value: uint8, maskSize: uint8, maskShift: uint8): uint32 =
    let maximum = (uint64(1) shl maskSize) - 1
    uint32((uint64(value) * maximum div 255) shl maskShift)

#[
  Packs red, green, and blue channel values into one framebuffer pixel.

  Each channel is converted using the layout supplied by Limine, then the
  channel bit fields are combined with bitwise OR. This works for different
  RGB layouts instead of assuming that every framebuffer uses the same bits.
]#
proc framebufferPixel(framebuffer: ptr LimineFramebuffer, red: uint8, green: uint8, blue: uint8): uint32 =
    framebufferChannel(red, framebuffer.redMaskSize, framebuffer.redMaskShift) or
      framebufferChannel(green, framebuffer.greenMaskSize, framebuffer.greenMaskShift) or
      framebufferChannel(blue, framebuffer.blueMaskSize, framebuffer.blueMaskShift)

#[
  Fills one framebuffer with a blue-to-green gradient.

  Pixels are accessed as 32-bit values. Since Limine reports `pitch` in bytes,
  it is divided by four to obtain the number of 32-bit pixel positions between
  the starts of adjacent rows. That row stride must be used instead of the
  visible width because padding may exist at the end of a framebuffer row.
]#
proc render(framebuffer: ptr LimineFramebuffer) =
    let pixels = cast[ptr UncheckedArray[uint32]](framebuffer.address)
    let pitchPixels = framebuffer.pitch div 4
    for y in 0'u64 ..< framebuffer.height:
        for x in 0'u64 ..< framebuffer.width:
            let nx = uint8(x * 255 div framebuffer.width)
            let ny = uint8(y * 255 div framebuffer.height)
            pixels[y * pitchPixels + x] = framebufferPixel(framebuffer, nx, 0, ny)

#[
  Validates Limine's framebuffer response and renders the demo pattern.

  The function checks that the requested Limine base revision is supported,
  that Limine returned a response, and that at least one framebuffer exists. It
  then visits every framebuffer and rejects layouts this renderer does not
  understand. `true` means every framebuffer was rendered; `false` means the
  response was missing or unsupported.

  Example:
    if not renderAll():
      halt()
]#
proc renderAll*(): bool =
    if limineBaseRevision[2] != 0 or framebufferRequest.response == nil or
          framebufferRequest.response.framebufferCount < 1:
        return false

    for index in 0'u64 ..< framebufferRequest.response.framebufferCount:
        let framebuffers = cast[ptr UncheckedArray[ptr LimineFramebuffer]](framebufferRequest.response.framebuffers)
        let framebuffer = framebuffers[index]
        # This renderer only understands 32-bit RGB pixel memory.
        if framebuffer.memoryModel != LimineFramebufferRgb or framebuffer.bpp != 32:
            return false
        render(framebuffer)

    return true
