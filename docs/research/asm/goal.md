The achieve the desired result the buildout should apply the following layers

# 1. Abstract the ASM

Allowing the compilation of .asm files to run python expressed asm content.
This includes the stnadard writer `asm.func(a, b)` and any linguistic expression.

At its core, it's very easy to create, being a simple printer. The written content
may utilise python __magic__, converting pythonic operands as asm operands in the
final output. In addition the `register` serves as a string placeholder and a pseudo
directive to apply more complex asm operations, using less complex oop style:

    del reg.eax
    # write .asm
    xor eax, eax

In addition, computing the inputs can help with pre-tests and compilation errors

    raw('bits 16')
    asm.mov(reg.rax, 2)
    # CompilationError: Cannot use 64 Bit 'RAX' with 'BIT 16'.

# 2. Sugar

Apply shortcuts for readability and pythonic macros, compiling functions with
hints to compilation methodology

    reg.rax = 3            mov rax, 5
    reg.rcx = 12           mov rcx, 12
    reg.rax + reg.rcx      add rax, rcx

cleaner functional calls can setup canned execution statements:

    asm.hlt()
    asm.clr()
    my_hello("welcome to my asm load screen")
    # my_hello db "welcome to my asm load screen", 0

as the python code executes procedurally, functional steps to isolate blocks


    def main():
        asm.mov('al', 2)
        clear()
        print_hello()
        clear()
        print_hello()


    def print_hello():
        asm.db('message', 0, label='hello')
        stmt='''
        print:
            push bp
            mov bp, sp
            pusha
            mov si, [bp+4]      # grab the pointer to the data
            mov bh, 0x00        # page number, 0 again
            mov bl, 0x00        # foreground color, irrelevant - in text mode
            mov ah, 0x0E        # print character to TTY
        '''
        raw(stmt)

    def clear():
        stmt = """
        clearscreen:
            push bp
            mov bp, sp
            pusha

            mov ah, 0x07        # tells BIOS to scroll down window
            mov al, 0x00        # clear entire window
            mov bh, 0x07        # white on black
            mov cx, 0x00        # specifies top left of screen as (0,0)
            mov dh, 0x18        # 18h = 24 rows of chars
            mov dl, 0x4f        # 4fh = 79 cols of chars
            int 0x10            # calls video interrupt

            popa
            mov sp, bp
            pop bp
            ret
        """
        raw(stmt)


# 3. Target Syntax

Using script arguments, target a compiler such as 'atnt', changing the .asm output form

    asm.mov('al', 2)
    mov $2, %al     ; atnt
    mov al, 2       ; intel

