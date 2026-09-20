add

Add two 64 bit registers

    mov rax, 5
    mov rcx, 12

    add rax, rcx

become

    move(5, into=rax)
    asm.mov(reg.rax, 5)

    add(rax, rcx)

better:

    rax = 5     ; mov
    rcx = 12    ; mov
    rax + rcx   ; add

