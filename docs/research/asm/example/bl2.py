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
    asm.org(0x7C00)

    asm.si = "HelloString"
    asm.call('print_string')
    asm.jump('$')
    data(**kw)
    last_pad()


def data(**kw):
    asm.comment("Data")
    val = kw.get('hello', 'Hello World')
    asm.db('HelloString', val)           # HelloString db 'Hello World', 0     ;HelloWorld string ending with 0


def last_pad():
    asm.times(510).fill()                # TIMES 510 - ($ - $$) db 0           ;Fill the rest of sector with 0
    asm.dw(0xAA55)                  # DW 0xAA55                           ;Add boot signature at the end of bootloader


# @magic.label('PrintCharacter:')
def print_char(asm):                #  ;Procedure to print character on screen ;Assume that ASCII value is in register AL
    reg.ah = 0x0e                   # MOV AH, 0x0E                        ;Tell BIOS that we need to print one charater on screen.
    reg.bh = 0x00                   # MOV BH, 0x00                        ;Page no.
    reg.bl = 0x07                   # MOV BL, 0x07                        ;Text attribute 0x07 is lightgrey font on black background
    vid_int()                       # INT 0x10                            ;Call video interrupt
    asm.ret()                       #                                     ;Return to calling procedure


@magic.label('print_string:')       # ;Procedure to print string on screen  ;Assume that string starting pointer is in register SI
# @magic.label('next_character:')
def next_char(asm):
    """
    1. using the si pointer, fetch as byte - into the accumulator
    2. inc the si pointer -
    3. if at the end of the string, jump to exit
    4. [else] call printString function, then loop back to #1.
    """
    # next_character:                     ;Lable to fetch next character from string
    reg.al = [asm.si]                # MOV AL, [SI]                        ;Get a byte from string and store in AL register
    asm.si += 1                      # INC SI                              ;Increment SI pointer
    reg.al.is_zero()                 # OR AL, AL                           ;Check if value in AL is zero (end of string)
    asm.jump.if_0('exit_function')   # JZ exit_function                    ;If end then return
    asm.call(print_char)             # CALL PrintCharacter                 ;Else print the character which is in AL register
    asm.jump(next_char)              # JMP next_character                  ;Fetch next character from string
    asm.label('exit_function:')      # exit_function:                      ;End label
    asm.ret()                        # RET                                 ;Return from procedure
