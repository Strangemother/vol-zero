from register import Register
from lib import make

reg = Register('x16')

def generate(*a, **kw):
    asm = make(*a, **kw)

    start(asm)
    print_memory_value(asm)
    loop(asm)

    asm.finish()

def print_memory_value(asm):
    with asm.label('.printMemoryValue:') as b:
        reg.cx = hex(6)  #"0006H"       # CX:DX = 00068480h Pause for about 0.4 sec
        reg.dx = '8480H'                # mov   dx, 8480H
        reg.ah = '86h'   # BIOS.Delay   # mov   ah, 86h     ; BIOS.Delay
        asm.int(0x15)    # call kernel  # int   15h
        asm.mov(reg.bp, value_of=reg.di)# mov   bp, [di]
                                        # Moving content of memory location in BP
        # Display page 0 in BH, Attribute WhiteOnBlack in BL
        b.mov(reg.sp, 0x007)            # mov   bx, 0007h
        rex.cx = 16                     # mov   cx, 16


def start(asm):
    # start statement and block
    with asm.label('start') as b:
        b.ax.xor()
        b.mov(reg.dx, reg.ax)
        b.mov(reg.ss, reg.ax)
        b.mov(reg.sp, "7F00h")
        b.mov(reg.di, "7C00h")


def loop(asm):

    with asm.label('.loopstart:') as b:
        asm.rol(reg.bp, 1)          # rol   bp, 1       ; Produces a CF
        reg.ax = '0E00h'            # mov   ax, 0E00h   ; Function number in AH, zeroing AL
        asm.adc(reg.ax, '0')        # adc   al, "0"     ; 0 + "0" + CF=0 ==> "0"
        asm.int(0x10)               # int   10h         ; 0 + "0" + CF=1 ==> "1"
        reg.cx.dec()                # dec   cx
        asm.jnz('.loopstart')       # jnz   .loopstart
        reg.ax = "0E0Dh"            # mov   ax, 0E0Dh   ; Newline is carriage return plus linefeed
        asm.int("10h")              # int   10h
        reg.ax = "0E0Ah"            # mov   ax, 0E0Ah
        asm.int("10h")              # int   10h
        asm.add(reg.di, "2")        # add   di, 2
        asm.cmp(reg.di, "7E00h")    # cmp   di, 7E00h
        asm.jb(".printMemoryValue") # jb    .printMemoryValue
        asm.hlt()

        asm.times("510-($-$$) db 0")# times 510-($-$$) db 0
        asm.dw("0AA55h")            # ; => 55h 0AAh (little endian byte order)
