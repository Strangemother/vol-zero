from lib import bios, make
from lib.head import *

asm = make(register=Register('x16'), record_method='lrtd')

bios.bit_code(asm).org(asm)

jump(0, 'initialize_bios')


def initialize_bios(asm):
    ax.xor()
    ds = ax
    es = ax
    mov([bootdrive], dl) # store boot drive into data
    si = 'welcome'
    call(print_char)


def halt():
    hlt()
    jump(halt)


def print_char(asm):
    al = [si]
    si += 1
    al._or()
    jumpz('exit_function')
    ah = 0x0e
    bh = 0  # page number
    bl = 0x07 # color
    vid_int()
    jump(print_char)
    ret(label='exit_function:')

with section('data'):
    db.welcome =  'Loading...'
    db.error =  'Error'
    db.bootdrive =  0x00


times(200).fill() # 510 bytes
dw(0x0aa55) # 2 bytes for a total of 512
