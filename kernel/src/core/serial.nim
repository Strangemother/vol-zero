#[
  The x86 CPU communicates with legacy devices through I/O ports. Nim does not
  express the compiler constraints needed by the `inb` and `outb` instructions,
  so these small C helpers provide that boundary.

  The `"a"` constraint places the byte value in the accumulator register, and
  `"Nd"` allows the compiler to use either an immediate port number or the DX
  register. `volatile` prevents the compiler from removing or reordering the
  hardware access as if it were an ordinary unused calculation.
]#
{.emit: """
static inline void nim_serial_out(unsigned short port, unsigned char value) {
  __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}

static inline unsigned char nim_serial_in(unsigned short port) {
  unsigned char value;
  __asm__ volatile ("inb %1, %0" : "=a"(value) : "Nd"(port));
  return value;
}
""".}

#[
  Declares the C helper that writes one byte to an x86 I/O port.

  This procedure is private to this module because callers should normally
  use `init` and `write` instead of manipulating UART registers directly.
]#
proc serialOut(port: uint16, value: uint8) {.importc: "nim_serial_out".}

#[
  Declares the C helper that reads one byte from an x86 I/O port.

  It is used to inspect the UART status register before writing another byte.
]#
proc serialIn(port: uint16): uint8 {.importc: "nim_serial_in".}

#[
  Configures the first PC serial port, COM1, for eight data bits, no parity,
  one stop bit, and a baud-rate divisor of three.

  The numeric port addresses are COM1's standard registers. Call this before
  `write` so the UART is configured to transmit reliably.

  Example:
    init()
    write("serial console ready\0")
]#
proc init*() =
    serialOut(0x3f9, 0)
    serialOut(0x3fb, 0x80)
    serialOut(0x3f8, 3)
    serialOut(0x3f9, 0)
    serialOut(0x3fb, 3)
    serialOut(0x3fa, 0xc7)
    serialOut(0x3fc, 0x0b)

#[
  Sends a NUL-terminated message through COM1.

  A `cstring` is a pointer to characters ending with a NUL byte (`'\0'`). The
  procedure reads one character at a time, waits until the UART transmitter is
  ready, and then writes the character to COM1. Call `init` first and provide a
  valid NUL-terminated string.

  Example:
    init()
    write("hello from the kernel\0")
]#
proc write*(message: cstring) =
    let current = cast[ptr UncheckedArray[char]](message)
    var index = 0
    while current[index] != '\0':
        while (serialIn(0x3fd) and 0x20) == 0:
            discard
        serialOut(0x3f8, uint8(current[index]))
        inc index

proc writeUInt64*(value: uint64) =
  var digits: array[20, char]
  var remaining = value
  var index = digits.len
  if remaining == 0:
    write("0")
    return
  while remaining > 0:
    dec index
    digits[index] = char(ord('0') + int(remaining mod 10))
    remaining = remaining div 10
  write(cast[cstring](digits[index].addr))
