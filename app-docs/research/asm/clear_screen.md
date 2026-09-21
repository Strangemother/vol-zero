    clearscreen:
        push bp
        mov bp, sp
        pusha

        mov ah, 0x07        # tells BIOS to scroll down window
        mov al, 0x00        # clear entire window
        mov bh, 0x07        # white on black
        mov cx, 0x00        # specifies top left of screen as (0,0)
        mov dh, 0x18        # 18h = 24 rows of chars
        mov dl, 0x4f        # 4fh = 79 cols of chars
        int 0x10            # calls video interrupt

        popa
        mov sp, bp
        pop bp
        ret
