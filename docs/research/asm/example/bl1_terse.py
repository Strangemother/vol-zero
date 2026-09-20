"""A 16 bit bootloader with a print string "hello world."""
from register import Register
from lib import make
from lib.head import *


reg = Register('x16')
asm = make(register=reg)

bits(16)

ax = 0x07C0          # mov ax, 0x07C0
ds = ax              # mov ds, ax
ax = 0x07E0          # mov ax, 0x07E0      # 07E0h = (07C00h+200h)/10h, beginning of stack segment.
ss = ax              # mov ss, ax
sp = 0x2000          # mov sp, 0x2000      # 8k of stack space.

call('clearscreen')  # call clearscreen
push(0x0000)         # push 0x0000
call('movecursor')   # call movecursor
sp += 2              # add sp, 2

push('msg')          # push msg
call(_print)         # call print
sp += 2              # add sp, 2

cli()                # cli
hlt()                # hlt


def clearscreen(asm):
    bp.push()        # push bp
    bp = sp          # mov bp, sp
    pusha()          # pusha

    ah = 0x07        # mov ah, 0x07        # tells BIOS to scroll down window
    al = 0x00        # mov al, 0x00        # clear entire window
    bh = 0x07        # mov bh, 0x07        # white on black
    cx = 0x00        # mov cx, 0x00        # specifies top left of screen as (0,0)
    dh = 0x18        # mov dh, 0x18        # 18h = 24 rows of chars
    dl = 0x4f        # mov dl, 0x4f        # 4fh = 79 cols of chars
    vid_int()        # int 0x10            # calls video interrupt

    popa()           # popa
    sp = bp          # mov sp, bp
    bp.pop()         # pop bp
    ret()            # ret


def movecursor():
    bp.push()
    bp = sp
    pusha()

    dx = [bp+4]      # get the argument from the stack. |bp| = 2, |arg| = 2
    ah = 0x02        # set cursor position
    bh = 0x00        # page 0 - doesn't matter, we're not using double-buffering
    vid_int()        # int 0x10            # calls video interrupt

    popa()
    sp = bp
    bp.pop()
    ret()


def _print():
    push bp
    bp = sp
    pusha()
    si = [bp+4]      # grab the pointer to the data
    bh = 0x00        # page number, 0 again
    bl = 0x00        # foreground color, irrelevant - in text mode
    ah = 0x0E        # print character to TTY


with label('.char'):
    al = [si]        # get the current char from our pointer position
    si.add(1)        # add si, 1           # keep incrementing si until we see a null char
    al._or(0)        # or al, 0
    je('.return')    # je .return          # end if the string is done
    vid_int()        # int 0x10            # print the character if we're not done
    jmp('.char')     # jmp .char           # keep looping


with('.return'):
    popa()           # popa
    sp = bp          # mov sp, bp
    bp.pop()         # pop bp
    ret()            # ret


db.msg = "Oh boy do I sure love assembly!" # msg:    db "Oh boy do I sure love assembly!", 0

times(510).fill()       # times 510-(\$-$$) db 0
dw(0xAA55)              # dw 0xAA55
