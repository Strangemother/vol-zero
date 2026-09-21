A templating structure or pythonic macros to append to the application in an oop manner.

Result:

    [BITS 16]                           ;Tells the assembler that its a 16 bit code
    [ORG 0x7C00]                        ;Origin, tell the assembler that where the code will
                                        ;be in memory after it is been loaded

    MOV SI, HelloString                 ;Store string pointer to SI
    CALL PrintString                    ;Call print string procedure
    JMP $                               ;Infinite loop, hang it here.


    PrintCharacter:                     ;Procedure to print character on screen
                                        ;Assume that ASCII value is in register AL
        MOV AH, 0x0E                        ;Tell BIOS that we need to print one charater on screen.
        MOV BH, 0x00                        ;Page no.
        MOV BL, 0x07                        ;Text attribute 0x07 is lightgrey font on black background

        INT 0x10                            ;Call video interrupt
        RET                                 ;Return to calling procedure



    PrintString:                        ;Procedure to print string on screen
                                        ;Assume that string starting pointer is in register SI

        next_character:                     ;Lable to fetch next character from string
        MOV AL, [SI]                        ;Get a byte from string and store in AL register
        INC SI                              ;Increment SI pointer
        OR AL, AL                           ;Check if value in AL is zero (end of string)
        JZ exit_function                    ;If end then return
        CALL PrintCharacter                 ;Else print the character which is in AL register
        JMP next_character                  ;Fetch next character from string
        exit_function:                      ;End label
        RET                                 ;Return from procedure


    ;Data
    HelloString db 'Hello World', 0     ;HelloWorld string ending with 0

    TIMES 510 - ($ - $$) db 0           ;Fill the rest of sector with 0
    DW 0xAA55                           ;Add boot signature at the end of bootloader


The ASM should be extendable. The desired result should look something like:



    import asm.ASM

    class Boot(asm.ASM):

        def start(self):
            asm.bit(16)
            asm.org(0x7C00)
            self.print_hello()

        def print_hello():
            asm.db('Hello World', label='helloString', place='data')

        def asm_print_char(self):
            _asm = asm.label('next_char')
            # use internal module for indenation.
            _asm.mov(reg.AH, 0x0E)
            _asm.mov(reg.BH, 0x00)
            _asm.mov(reg.BL, 0x07)
            # video interrupt to print
            # _asm.int(16)             # INT 0x10
            _asm.vint()

            _asm.ret()


        def asm_print_str(self):

            with asm.label('next_char'):
                asm.mov('al', ['si'])
                reg.si.inc()
                asm.or(reg.al)
                asm.jz('exit_function')
                asm.call('print_char')
                asm.jmp('next_char')
                asm.label('exit_function')
                asm.ret()

## functional exposure.

Mixing it up a little, it'd be nice to refer to internal references to apply ASM logic

    item = asm.label('next_char')
    item.mov(reg.AH, 0x0E)
    item.mov(reg.BH, 0x00)
    item.mov(reg.BL, 0x07)
    item.ret()
    asm.call(item)

nice if:

    item = asm.label('next_char', write_here=False)
    asm.call(item)
    with next_char as item.write_here(): # returns self for __enter__
        item.mov(reg.AH, 0x0E)
        item.mov(reg.BH, 0x00)
        item.mov(reg.BL, 0x07)
        item.ret()

creating:

    next_char:
        mov AH, 0x0E
        mov BH, 0x00
        mov BL, 0x07
        ret

    call next_char
