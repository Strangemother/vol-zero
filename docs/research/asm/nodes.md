http://www.cs.virginia.edu/~evans/cs216/guides/x86.html
https://50linesofco.de/post/2018-02-28-writing-an-x86-hello-world-bootloader-with-assembly
http://faydoc.tripod.com/cpu/index.htm
https://gist.github.com/AVGP/85037b51856dc7ebc0127a63d6a601fa
http://joebergeron.io/posts/post_two.html
http://www.coranac.com/tonc/text/asm.htm
https://en.wikipedia.org/wiki/Microcode
http://www.keil.com/support/man/docs/armasm/armasm_dom1361290008953.htm

# Move

    mov — Move (Opcodes: 88, 89, 8A, 8B, 8C, 8E, ...)

The mov instruction copies the data item referred to by its second operand (i.e. register contents, memory contents, or a constant value) into the location referred to by its first operand (i.e. a register or memory). While register-to-register moves are possible, direct memory-to-memory moves are not. In cases where memory transfers are desired, the source memory contents must first be loaded into a register, then can be stored to the destination memory address.

Syntax
    mov <reg>,<reg>
    mov <reg>,<mem>
    mov <mem>,<reg>
    mov <reg>,<const>
    mov <mem>,<const>

Examples

    # copy the value in ebx into eax
    mov eax, ebx
    # store the value 5 into the byte at location var
    mov byte ptr [var], 5


# add — Integer Addition

The add instruction adds together its two operands, storing the result in its first operand. Note, whereas both operands may be registers, at most one operand may be a memory location.

Syntax
    add <reg>,<reg>
    add <reg>,<mem>
    add <mem>,<reg>
    add <reg>,<con>
    add <mem>,<con>

Examples

    # — EAX ← EAX + 10
    add eax, 10
    # — add 10 to the single byte stored at memory address var
    add BYTE PTR [var], 10
