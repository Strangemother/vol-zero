
var humanBytesBuffer: array[32, char]

proc human_bytes*(bytes: uint64): cstring =
    let
        kb = 1024'u64
        mb = kb * 1024
        gb = mb * 1024
    var value = bytes
    var unitLength = 2
    var unitFirst = ' '
    var unitSecond = 'B'

    if bytes >= gb:
        value = bytes div gb
        unitLength = 3
        unitFirst = 'G'
        unitSecond = 'B'
    elif bytes >= mb:
        value = bytes div mb
        unitLength = 3
        unitFirst = 'M'
        unitSecond = 'B'
    elif bytes >= kb:
        value = bytes div kb
        unitLength = 3
        unitFirst = 'K'
        unitSecond = 'B'

    var endIndex = humanBytesBuffer.len - 1
    humanBytesBuffer[endIndex] = '\0'
    dec endIndex
    humanBytesBuffer[endIndex] = unitSecond
    if unitLength == 3:
        dec endIndex
        humanBytesBuffer[endIndex] = unitFirst
        dec endIndex
        humanBytesBuffer[endIndex] = ' '
    else:
        dec endIndex
        humanBytesBuffer[endIndex] = unitFirst

    if value == 0:
        dec endIndex
        humanBytesBuffer[endIndex] = '0'
    else:
        while value > 0:
            dec endIndex
            humanBytesBuffer[endIndex] = char(ord('0') + int(value mod 10))
            value = value div 10

    return cast[cstring](humanBytesBuffer[endIndex].addr)