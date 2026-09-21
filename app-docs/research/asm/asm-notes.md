+ http://www.c-jump.com/CIS77/CPU/x86/X77_0070_gp_registers.htm
+ https://en.wikibooks.org/wiki/X86_Assembly/X86_Architecture

in atnt styax
    register prefix %
    vars with $

define a segment for .data

define a segment for .text
+ this is where the code goes

intel:

    mov al, 23         movb $23, %al
    mov bl, 6          movb $6, %bl
    add al, bl         addb $bl, %al

    mov eax, 100        movl $100, %eax

+ dollar == literal value
+ percent == register
+ 'eax' is the _destination_
+ 100 is the source

x86 registers
General purpose
    16 registers.

    RAX:
        + 64 bit verion

        EAX
            + is the 'extra' ax
            + 32 bit - AX is Low 16bits
            + cannot directly access top eax 16bit

            AX:
                AH
                    + 8bit
                AL
                    is 8bit (byte long)
                    + signed or unsigned
                    + single char
