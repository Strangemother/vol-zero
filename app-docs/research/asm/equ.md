equ is a directive, giving nasm a value to apply

    sys_exit equ 1

write this this to the compiler

    asm.equ('sys_exit', 1)
    asm.equ.sys_exit = 1

Future:

    sys_exit = 1
    # sys_exit equ 1

