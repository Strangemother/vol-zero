#[ Small framebuffer terminal backed by Limine's Flanterm parameters. ]#

proc init*(preserve: bool): bool {.importc: "limine_terminal_init".}

proc init*(): bool =
    init(preserve=false)

proc write*(message: cstring) {.importc: "limine_terminal_write".}

proc set_xy*(column: uint64, row: uint64) {.
    importc: "limine_terminal_set_cursor_position".}

proc columns*(): uint64 {.importc: "limine_terminal_columns".}

proc rows*(): uint64 {.importc: "limine_terminal_rows".}

proc write_line*(message: cstring) =
    write(message)
    write("\r\n")
