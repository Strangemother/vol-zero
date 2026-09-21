
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


def movecursor(asm):
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

def bootloader_fill(bytes_int=510):
    times(510).fill()       # times 510-(\$-$$) db 0
    dw(0xAA55)              # dw 0xAA55
