from register import Register
from lib import make

reg = Register('x16')

def generate(*a, **kw):
    asm = make(*a, **kw)
    ordered = asm.compile(start, print_memory_value, loop, )
    ordered.write('hello.asm')


@magic.label('start')
def start(asm):
    # start statement and block
    reg.ax.zero()               # xor   ax, ax      ; This is shorter/faster than "mov ax, 0h"
    reg.ds = reg.ax          # mov   ds, ax
    reg.ss = reg.ax          # mov   ss, ax
    reg.sp = "7F00h"         # mov   sp, 7F00h   ; set stack pointer after our bootloader
    reg.di = "7C00h"         # mov   di, 7C00h   ; set Data pointer to where is our bootloader loaded


@magic.label('.printMemoryValue')
def print_memory_value(asm):
    bios_delay(4)
    asm.int(0x15)    # call kernel  # int   15h
    reg.bp = [reg.di]               # mov   bp, [di]     # Moving content of memory location in BP
    reg.bx = 0x007                  # mov   bx, 0007h    # Display page 0 in BH, Attribute WhiteOnBlack in BL
    rex.cx = 16                     # mov   cx, 16


@magic.label('.loopstart')
def loop(asm):

    asm.rol(reg.bp, 1)          # rol   bp, 1       ; Produces a CF
    reg.ax = '0E00h'            # mov   ax, 0E00h   ; Function number in AH, zeroing AL
    reg.al.adc('0')             # adc   al, "0"     ; 0 + "0" + CF=0 ==> "0"
    vid_int()                   # int   10h
    reg.cx -= 1                 # dec   cx
    # asm.jump.if_not_0(loop)   # jnz   .loopstart
    asm.jump(loop) if not 0     # jnz   .loopstart

    reg.ax.crlf()               # mov   ax, 0E0Dh   ; Newline is carriage return plus linefeed
    vid_int()                   # int   10h
    reg.ax = "0E0Ah"            # mov   ax, 0E0Ah
    vid_int()                   # int   10h
    reg.di += 2                 # add   di, 2
    reg.di.cmp(0x7E00)          # cmp   di, 7E00h
    #asm.jump.if_0(printMemoryValue)    # jb    .printMemoryValue
    asm.jump(printMemoryValue) if 0    # jb    .printMemoryValue
    asm.hlt()

    asm.times("510-($-$$) db 0")# times 510-($-$$) db 0
    asm.dw(0x0AA55)             # ; => 55h 0AAh (little endian byte order)


def split_hex(exp_hex):
    return exp_hex[0:4], exp_hex[4::]


def as_hex(number):
    return hex(int(number))[2:].rjust(8, '0')


def bios_delay(ms)
    cpu_ms = ms * 106784.0
    ha, hb = split_hex(as_hex(cpu_ms))

    reg.cx = f"{ha}h"     # "0006H"       # CX:DX = 00068480h Pause for about 0.4 sec
    reg.dx = f"{hb}h"     # mov   dx, 8480H
    reg.ah = 0x86         # mov   ah, 86h     ; BIOS.Delay
