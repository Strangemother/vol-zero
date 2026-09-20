"""A 16 bit bootloader with a print string "hello world."""
from register import Register
from lib import make
from lib.head import *


reg = Register('x16')
asm = make(register=reg, walk_method='inline')

bits(16)

AX = 0x07C0          # mov AX, 0x07C0
DS = AX              # mov DS, AX
AX = 0x07E0          # mov AX, 0x07E0      # 07E0h = (07C00h+200h)/10h, beginning of stack segment.
SS = AX              # mov SS, AX
SP = 0x2000          # mov sp, 0x2000      # 8k of stack space.

call('clearscreen')  # call clearscreen
push(0x0000)         # push 0x0000
call('movecursor')   # call movecursor
SP += 2              # add sp, 2

push('msg')          # push msg
call(_print)         # call print
SP += 2              # add sp, 2

cli()                # cli
hlt()                # hlt


def clearscreen(asm):
    BP.push()        # push BP
    BP = SP          # mov BP, sp
    pusha()          # pusha

    AH = 0x07        # mov AH, 0x07        # tells BIOS to scroll down window
    AL = 0x00        # mov al, 0x00        # clear entire window
    BH = 0x07        # mov BH, 0x07        # white on black
    CX = 0x00        # mov cx, 0x00        # specifies top left of screen as (0,0)
    DH = 0x18        # mov dh, 0x18        # 18h = 24 rows of chars
    DL = 0x4f        # mov dl, 0x4f        # 4fh = 79 cols of chars
    vid_int()        # int 0x10            # calls video interrupt

    popa()           # popa
    SP = BP          # mov sp, BP
    BP.pop()         # pop BP
    ret()            # ret


def movecursor():
    BP.push()
    BP = SP
    pusha()

    DX = [BP+4]      # get the argument from the stack. |BP| = 2, |arg| = 2
    AH = 0x02        # set cursor position
    BH = 0x00        # page 0 - doesn't matter, we're not using double-buffering
    vid_int()        # int 0x10            # calls video interrupt

    popa()
    SP = BP
    BP.pop()
    ret()


def _print():
    BP.push()
    BP = SP
    pusha()
    SI = [BP+4]      # grab the pointer to the data
    BH = 0x00        # page number, 0 again
    BL = 0x00        # foreground color, irrelevant - in text mode
    AH = 0x0E        # print character to TTY


with label('.char'):
    AL = [SI]        # get the current char from our pointer position
    SI.add(1)        # add si, 1           # keep incrementing si until we see a null char
    AL._or(0)        # or al, 0
    je('.return')    # je .return          # end if the string is done
    vid_int()        # int 0x10            # print the character if we're not done
    jmp('.char')     # jmp .char           # keep looping


with('.return'):
    popa()           # popa
    SP = BP          # mov sp, BP
    BP.pop()         # pop BP
    ret()            # ret


DB.msg = "Oh boy do I sure love assembly!" # msg:    db "Oh boy do I sure love assembly!", 0

times(510).fill()       # times 510-(\$-$$) db 0
dw(0xAA55)              # dw 0xAA55
