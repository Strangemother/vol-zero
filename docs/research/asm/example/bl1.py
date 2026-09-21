"""A 16 bit bootloader with a print string "hello world."""
from register import Register
from lib import make

reg = Register('x16')

def main(*a, **kw):
    kw['hello'] = "Hello World + Dave."
    asm = make(*a, **kw)
    generate(*a, **kw)
    asm.finish()


def generate(*a, **kw):
    asm.bits(16)

    reg.ax = 0x07C0         # mov ax, 0x07C0
    reg.ds = reg.ax         # mov ds, ax
    reg.ax = 0x07E0         # mov ax, 0x07E0      # 07E0h = (07C00h+200h)/10h, beginning of stack segment.
    reg.ss = reg.ax         # mov ss, ax
    reg.sp = 0x2000         # mov sp, 0x2000      # 8k of stack space.

def sys():
    call(clearscreen)       # call clearscreen

    asm.push(0x0000)        # push 0x0000
    call(movecursor)        # call movecursor
    reg.sp += 2             # add sp, 2

    asm.push(msg)           # push msg
    call(print)             # call print
    reg.sp += 2             # add sp, 2

    asm.cli()                # cli
    asm.hlt()                # hlt


def clearscreen(asm):
    reg.bp.push()        # push bp
    reg.bp = reg.sp      # mov bp, sp
    asm.pusha()          # pusha

    reg.ah = 0x07        # mov ah, 0x07        # tells BIOS to scroll down window
    reg.al = 0x00        # mov al, 0x00        # clear entire window
    reg.bh = 0x07        # mov bh, 0x07        # white on black
    reg.cx = 0x00        # mov cx, 0x00        # specifies top left of screen as (0,0)
    reg.dh = 0x18        # mov dh, 0x18        # 18h = 24 rows of chars
    reg.dl = 0x4f        # mov dl, 0x4f        # 4fh = 79 cols of chars
    vid_int()            # int 0x10            # calls video interrupt

    asm.popa()           # popa
    reg.sp = bp          # mov sp, bp
    reg.bp.pop()         # pop bp
    reg.ret()            # ret


def movecursor():
    reg.bp.push()
    reg.bp = reg.sp
    asm.pusha()

    reg.dx = [reg.bp+4]  # get the argument from the stack. |bp| = 2, |arg| = 2
    reg.ah = 0x02        # set cursor position
    reg.bh = 0x00        # page 0 - doesn't matter, we're not using double-buffering
    vid_int()            # int 0x10            # calls video interrupt

    asm.popa()
    reg.sp = bp
    reg.bp.pop()
    asm.ret()
