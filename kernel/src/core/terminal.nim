#[ Small framebuffer terminal backed by Limine's Flanterm parameters. ]#

proc init*(preserve: bool): bool {.importc: "flanterm_terminal_init".}


proc init*(): bool =
    init(preserve=false)


proc write*(message: cstring) {.importc: "flanterm_terminal_write".}


proc set_xy*(column: uint64, row: uint64) {.importc: "flanterm_terminal_set_cursor_position".}


#[ Set the color of the terminal text. Example usage:

    terminal.set_text_fg(1, true) # bright red
    terminal.write("Warning")
    terminal.reset_text_fg()

Colors:

- The 8 standard ANSI colours 
 
    black, red, green, brown, blue, magenta, cyan, grey
]#
proc set_text_fg*(colour: uint64, bright: bool) {.importc: "flanterm_terminal_set_text_fg".}

proc set_text_bg*(colour: uint64, bright: bool) {.importc: "flanterm_terminal_set_text_bg".}


#[ Reset the foreground color of the terminal text. Example usage:

    terminal.reset_text_fg()
]#
proc reset_text_fg*() {.importc: "flanterm_terminal_reset_text_fg".}


proc reset_text_bg*() {.importc: "flanterm_terminal_reset_text_bg".}


proc columns*(): uint64 {.importc: "flanterm_terminal_columns".}


proc rows*(): uint64 {.importc: "flanterm_terminal_rows".}


proc write_line*(message: cstring) =
    write(message)
    write("\r\n")
