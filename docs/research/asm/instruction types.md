Instructions accept the following types:

    <reg32>     Any 32-bit register (EAX, EBX, ECX, EDX, ESI, EDI, ESP, or EBP)
    <reg16>     Any 16-bit register (AX, BX, CX, or DX)
    <reg8>      Any 8-bit register (AH, BH, CH, DH, AL, BL, CL, or DL)
    <reg>       Any register
    <mem>       A memory address (e.g., [eax], [var + 4], or dword ptr [eax+ebx])
    <con32>     Any 32-bit constant
    <con16>     Any 16-bit constant
    <con8>      Any 8-bit constant
    <con>       Any 8-, 16-, or 32-bit constant

    mov <reg>,<reg>
    mov <reg>,<mem>
    mov <mem>,<reg>
    mov <reg>,<const>
    mov <mem>,<const>

Therefore applying a value to a type not accepted can yield a compilation error
