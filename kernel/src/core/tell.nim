#[ Echo macro for serial write

This is a convenience **macro** for writing to the serial output.
Importantly this assumes the `serial` module has been initialized and is ready for writing.

Example:

    kernelEcho.echo("Kernel version: ", kernelVersion.get_version())

Replaces:

    serial.write("Kernel version: ")
    serial.write(kernelVersion.get_version())
    serial.write("\r\n")

+ Supports multiple arguments to the serial output.
+ Handles _string_ and `uint64` types only.
+ appends a newline `\r\n` by default.

]#
import std/macros
import serial

#[ Echo macro for serial write

This macro allows writing multiple arguments to the serial output conveniently.
It handles _string_ and `uint64` types only and appends a newline `\r\n` by default.

With Serial:

    serial.writeUInt64(allocationState.entryIndex)
    serial.write(" ")
    serial.writeUInt64(allocationState.address)
    serial.write("\r\n")

Exact replacement:

    kernelEcho.echo(allocationState.entryIndex, allocationState.address)

---

Note this is a compile time macro and will be expanded during compilation. It is not a runtime function.

]#
macro kernel_write*(args: varargs[untyped], newline: untyped = "\r\n"): untyped =
    result = newStmtList()

    for arg in args:
        result.add quote do:
            when typeof(`arg`) is uint64:
                serial.writeUInt64(`arg`)
            else:
                serial.write(`arg`)

        result.add quote do:
            serial.write(" ")
    let newlineText = newline.strVal
    if newlineText.len > 0:
        let newlineLiteral = newLit(newlineText)
        result.add quote do:
            serial.write(`newlineLiteral`)
    