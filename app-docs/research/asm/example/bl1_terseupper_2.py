"""A 16 bit bootloader with a print string "hello world."""
from lib.head import *
from terseupper_import import *

asm = make(register=Register(16), walk_method='inline')

bits()                   # [bits 16]

with label.no_label:     # apply no label to the ASM; used for python indentation only.
    AX = 0x07C0          # mov AX, 0x07C0 == 1984b
    DS = AX              # mov DS, AX
    AX = 0x07E0          # mov AX, 0x07E0      # 07E0h = (07C00h+200h)/10h == (0x7C00+0x200)/0x010  # beginning of stack segment. 2016 (1984+512)/16
    SS = AX              # mov SS, AX
    SP = kb(8)           # mov sp, 0x2000      # 8k of stack space. 0x02000 == 8192b

    call(clearscreen)    # call clearscreen
    push(0x0000)         # push 0x0000
    call(movecursor)     # call movecursor
    SP += 2              # add sp, 2

    push('msg')          # push msg
    call(_print)         # call print
    SP += 2              # add sp, 2

    cli()                # cli
    hlt()                # hlt

clearscreen.write()       ## Write the ASM code at this location.
movecursor.write()

def _print():
    BP.push()
    BP = SP
    pusha()
    SI = [BP+4]           # grab the pointer to the data
    BH = 0x00             # page number, 0 again
    BL = 0x00             # foreground color, irrelevant - in text mode
    AH = 0x0E             # print character to TTY

with label.char:
    AL = [SI]             # get the current char from our pointer position
    SI.add(1)             # add si, 1                # keep incrementing si until we see a null char
    AL._or(0)             # or al, 0
    JE._return            # je .return               # end if the string is done
    vid_int()             # int 0x10                 # print the character if we're not done
    JMP.char              # jmp .char                # keep looping

with label._return:
    popa()                # popa
    SP = BP               # mov sp, BP
    BP.pop()              # pop BP
    ret()                 # ret

DB.msg = asset('mymsg.txt') # msg:    db "Oh boy do I sure love assembly!", 0

bootloader_fill()
