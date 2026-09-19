#[ Small framebuffer terminal backed by Limine's Flanterm parameters. ]#

proc init*(preserve: bool): bool {.importc: "limine_terminal_init".}

proc write*(message: cstring) {.importc: "limine_terminal_write".}

proc setCursorPosition*(column: uint64, row: uint64) {.
    importc: "limine_terminal_set_cursor_position".}

proc writeLine*(message: cstring) =
    write(message)
    write("\r\n")