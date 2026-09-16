const humanByteUnits = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]

var humanBytesBuffer: array[32, char]


proc byte_unit(bytes: uint64): tuple[size: uint64, index: int] =
    var size = 1'u64
    var index = 0

    while index < humanByteUnits.high and bytes >= (size shl 10):
        size = size shl 10
        inc index

    return (size, index)


proc human_bytes*(bytes: uint64): cstring =
    let unit = byte_unit(bytes)

    var whole = bytes div unit.size
    let remainder = bytes mod unit.size

    # One decimal place, rounded.
    var decimal = (remainder * 10 + unit.size div 2) div unit.size

    if decimal == 10:
        inc whole
        decimal = 0

    var index = humanBytesBuffer.high
    humanBytesBuffer[index] = '\0'

    # Unit: B / KB / MB / etc.
    let unitName = humanByteUnits[unit.index]

    for i in countdown(unitName.high, 0):
        dec index
        humanBytesBuffer[index] = unitName[i]

    # Space.
    dec index
    humanBytesBuffer[index] = ' '

    # Decimal digit.
    dec index
    humanBytesBuffer[index] = char(ord('0') + int(decimal))

    # Decimal point.
    dec index
    humanBytesBuffer[index] = '.'

    # Whole number.
    if whole == 0:
        dec index
        humanBytesBuffer[index] = '0'
    else:
        while whole > 0:
            dec index
            humanBytesBuffer[index] =
                char(ord('0') + int(whole mod 10))
            whole = whole div 10

    return cast[cstring](humanBytesBuffer[index].addr)