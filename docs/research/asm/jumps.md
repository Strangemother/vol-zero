Conditional jumps
Let the instruction pointer do a conditional jump to the defined address. See the table below for the available conditions.

Instruction Description Condition  Alternatives

    JC      Jump if carry      Carry = TRUE                    JB, JNAE
    JNC     Jump if no carry   Carry = FALSE                   JNB, JAE
    JZ      Jump if zero       Zero = TRUE                     JB, JE
    JNZ     Jump if no zero    Zero = FALSE                    JNE
    JA      >                  Carry = FALSE && Zero = FALSE   JNBE
    JNBE    not <=             Carry = FALSE && Zero = FALSE   JA
    JAE     >=                 Carry = FALSE                   JNC, JNB
    JNB     not <              Carry = FALSE                   JNC, JAE
    JB      <                  Carry = TRUE                    JC, JNAE
    JNAE    not >=             Carry = TRUE                    JC, JB
    JBE     <=                 C = TRUE or Z = TRUE            JNA
    JNA     not >              C = TRUE or Z = TRUE            JBE
    JE      =                  Z = TRUE                        JZ
    JNE     !=                 Z = FALSE                       JNZ


The jump intuction compiler provides each through the asm:

    asm.jc()
    asm.jnc()
    ...


Functions with expanded names perform the same functionality, albeit more verbose.

    asm.jump(next_char)              # JMP next_character
    asm.jump.if_carry()
    asm.jump.if_no_carry()
    asm.jump.if_0('exit_function')   # JZ exit_function
    asm.jump.if_not_0('exit_function')   # JZ exit_function

    # JA, Carry = FALSE && Zero = FALSE
    asm.jump.if_carry_zero(False)
    # JBE, C = TRUE or Z = TRUE
    asm.jump.if_carry_zero(True)


Classical assignment:

    asm.call(print_char)
    if asm.jump.carry(True):
        asm.jump(next_char)


