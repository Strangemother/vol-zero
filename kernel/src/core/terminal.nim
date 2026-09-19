#[ Small framebuffer terminal backed by Limine's Flanterm parameters. ]#

proc init*(): bool {.importc: "limine_terminal_init".}

proc write*(message: cstring) {.importc: "limine_terminal_write".}

proc writeLine*(message: cstring) =
    write(message)
    write("\r\n")