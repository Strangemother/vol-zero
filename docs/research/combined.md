# Historical research archive

This file is a preserved concatenation of earlier research notes. It is a
source archive, not the current specification. Use [readme.md](readme.md) for
the organized view, then consult [concepts.md](concepts.md),
[examples.md](examples.md), [demos.md](demos.md), [python-poc.md](python-poc.md),
and [roadmap.md](roadmap.md) for the active design.

The headings below refer to historical note names, including notes that were
later removed or folded into the archive. Preserve them when comparing how the
idea evolved.

=========== add.md =========

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


========== END OF add.md =========


=========== api.md =========

A concept to work with the API.

A standard command has two parts, the operand and condition

    mov eax, 10

Standard notation works within python to simple print exact statements:

    # literal
    asm.mov(reg.eax, 10)
    # expanded
    asm.mov(10, to=reg.eax)
    # even a string
    asm.mov(10, to='eax')
    # Alias args
    asm.mov(value=10, into='eax')

the api should build an object from a string, reverse parse:

    v = asm.parse('mov eax, 10')
    v.value == 10
    v.type == 'mov'


# Register

The register tool is relatively cheap- but serves as a computation / write, and placeholder

    v = asm.mov(reg.al, 2)
    v.string() == 'mov al, 2'
    # For a syntax change to atnt
    v.string('atnt') == 'mov %al, $2'

The register can act as a pseudo placeholder. The python and psuedo comparible:

    asm.mov('al', 2)
    reg.al = 2

    asm.add(reg.rax, reg.rcx)
    reg.rax + reg.rcx

# Meta steps

The api created an ASM to build through the chosen compiler therefore each asm statement
creates an entry within the asm file. This allows python meta-programming on build args, captured in the asm creation script, or in the calling function.

    if compiler.type == 'atnt':
        raw('add $12, %eax')
    else:
        raw('add eax, 12')


# injection

as a core feature, the asm generator can call into other files and functions to write code.
As this is the meta phase to the compiler stage, we can use functions to OOP our asm, or include external files.

    def header():
        asm.db('written as assembly.', label='msg')



# Example

A Mixed file presentation may incorporate all the considered calling type.

    # literal
    asm.mov(reg.al, 2)
    # pythonic
    move(value=2, into='al')
    # pseudo
    reg.al + 10
    # inline (not compiler safe)
    raw('add eax, edx')





========== END OF api.md =========


=========== asm-notes.md =========

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

========== END OF asm-notes.md =========


=========== asm.md =========

notes for asm conversion.

A explain level to translate easy-to-read into asm

+ like for like string generative commands
+ Build literal ASM
+ Functional call makers

The registers and values used are written as literals and tracked in a pseudo
VM or simulator within python. Each function called can occur on the python equivelent.
This should be pretty easy.

Each unit called is a class instance to manage and write the entity. Each instance
may be instansiated via inline execution or string statement capture.

+ Somehow produce a revese capture.
+ For each iteration type, a detection function can intercept for write down.
+ Each block is rendered through recursive iteration.
+ A unit may be indented; within a label function.


# Basic.

A basic command has a statement and two values

    mov edx, 10

with representation concepts:

    move(10, into=edx)
    mov(edx, 10)

when performing on the CLI, the statements should resolve:

    edx == 10

Other:

    move(-1, ax)
    asm.mov(reg.AX, value=10)

Perhaps even:

    reg.AX = 10

performs write magic.


---

the stack is a heap is setup for calling.

esp: top of the stack
ebp: bottom of the stack


========== END OF asm.md =========


=========== asset.md =========

An asset defines content to be applied through compile time, not at runtime or translation phase.

The source code is converted to a binary through ASM compilation. The original file steps through phases before final compilation.

+ source as `*.py`
    pre-parsed python based statements as source
+ execution phase
    The intial execution of the source generating a AST graph
+ translation phase
    A production of linear executions in graph state for injection and live-reading
+ ASM generation phase
    Create the finished .asm files
+ compiler phase
    convert the ASM to a binary using the chosen compiler
+ runtime
    run the appliction in its native state.

The runtime is the final binary build through the chosen ASM compiler. The ASM is applied through the terse translation of the source code.

An `asset` applies content such as text to "compile time" for the translation phase to read as standard executions. It may point to an external file with content apply into the asm:

    asm.db('message', "Welcome to the first message of th...")

convert to an assert for external appliance; the execution phase will collect an inject the asset accordingly.

    # message.txt
    Welcome to the first ...

    # asm.py
    asm.db('message', asset('assets/message.txt'))

You must consider the content applied to the asm operator - this does not fix data overflows.

========== END OF asset.md =========


=========== binary and.md =========

mov eax, 111010101000b
mov ecx, 111000100101b ; binary const
and eax, ecx
      000100100101110b

========== END OF binary and.md =========


=========== bios-wait.md =========

INT 15h / AH = 86h - BIOS wait function.

input:
    CX:DX = interval in microseconds

return:
    CF clear if successful (wait interval elapsed),
    CF set on error or when wait function is already in progress.

example:

    mov   cx, 0006H   ; CX:DX = 00068480h Pause for about 0.4 sec
    mov   dx, 8480H
    mov   ah, 86h     ; BIOS.Delay

Note:
    the resolution of the wait period is 977 microseconds on many systems (1
        million microseconds - 1 second).
    Windows XP does not support this interrupt (always sets CF=1).

========== END OF bios-wait.md =========


=========== call.md =========

# Call

The call statement binds to a functional call in ASM They may be applied literally, or magically using the asm lib

## Literal

Use the literal functions to print explicit ASM lines.

    asm.call('mylabel')
    lasm = asm.label('mylabel')
    lasm.push(reg.ebp)
    lasm.pop(reg.ebp)
    lasm.ret()

producing:

    call mylabel
    mylabel:
        push ebp
        pop ebp
        ret


## Magic

Apply the call subroutine execution code within a python function and reference. The asm subroutine is applied to the output ASM file automatically

    @asm.label('mylabel')
    def pushpop():
        lasm.push(reg.ebp)
        lasm.pop(reg.ebp)
        lasm.ret()

    asm.call(pushpop)

========== END OF call.md =========


=========== clear_screen.md =========

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

========== END OF clear_screen.md =========


=========== conderations-warnings.md =========

The compile and translate steps should detect usage and perhaps warn on elements (hard coded)

ARM Setting Condition Flags:

    When using the Thumb instruction set, special attention should be given to the use of 16-bit instruction forms. Many of those (moves, adds, shifts, etc) automatically set the condition flags. For best performance, consider using the 32-bit encodings which include forms that do not set the condition flags, within the bounds of the codedensity requirements of the program

As such when a registry flag is switched, the compiler test can verfiy if the flipped flag was accessed. If not, a warning can suggest an edit for performance. in a compiler phase this may be captured.

    mov al, 10
    # flag flipped

    asm.mov(reg.al, 10)


========== END OF conderations-warnings.md =========


=========== dd.md =========

3.2.1 DB and Friends: Declaring Initialized Data
DB, DW, DD, DQ, DT, DO, DY and DZ are used, much as in MASM, to declare initialized data in the output file. They can be invoked in a wide range of ways:

      db    0x55                ; just the byte 0x55
      db    0x55,0x56,0x57      ; three bytes in succession
      db    'a',0x55            ; character constants are OK
      db    'hello',13,10,'$'   ; so are string constants
      dw    0x1234              ; 0x34 0x12
      dw    'a'                 ; 0x61 0x00 (it's just a number)
      dw    'ab'                ; 0x61 0x62 (character constant)
      dw    'abc'               ; 0x61 0x62 0x63 0x00 (string)
      dd    0x12345678          ; 0x78 0x56 0x34 0x12
      dd    1.234567e20         ; floating-point constant
      dq    0x123456789abcdef0  ; eight byte constant
      dq    1.234567e20         ; double-precision float
      dt    1.234567e20         ; extended-precision float
DT, DO, DY and DZ do not accept numeric constants as operands.

========== END OF dd.md =========


=========== equ.md =========

equ is a directive, giving nasm a value to apply

    sys_exit equ 1

write this this to the compiler

    asm.equ('sys_exit', 1)
    asm.equ.sys_exit = 1

Future:

    sys_exit = 1
    # sys_exit equ 1


========== END OF equ.md =========


=========== example hello world.md =========

A simple example usecase to make some ASM:

    section .text
       global _start     ;must be declared for linker (ld)

    _start:             ;tells linker entry point
       mov  edx,len     ;message length
       mov  ecx,msg     ;message to write
       mov  ebx,1       ;file descriptor (stdout)
       mov  eax,4       ;system call number (sys_write)
       int  0x80        ;call kernel

       mov  eax,1       ;system call number (sys_exit)
       int  0x80        ;call kernel

    section .data
    msg db 'Hello, world!', 0xa  ;string to be printed
    len equ $ - msg     ;length of the string

it mat be define literally, but that's no better than ASM

    asm.section('text')
    asm.global(_start')     #must be declared for linker (ld)

    asm.label('_start')
    asm.mov(edx,len)   # message length
    asm.mov(ecx,msg)   # message to write
    asm.mov(ebx,1)   # file descriptor (stdout)
    asm.mov(eax,4)   # system call number (sys_write)
    asm.int(0x80)   # call kernel

    asm.mov(eax, 1)     # system call number (sys_exit)
    asm.int(0x80)   # call kernel

    asm.section('data')
    asm.db('Hello, world!', 0xa  label='msg') # string to be printed
    asm.equ("$ - msg", label='len') # length of the string


With sugar:


    def main():
        with asm.section.text:
           asm.global('_start')

        start()

        with asm.section.data:                    # section .data
            msg = asm.db('msg', 'Hello World')    # msg db 'Hello, world!', 0xa  #string to be printed
            asm.equ('len', asm.$, asm.sub, msg)   # len equ $ - msg     ;length of the string
            # asm.equ('len', f"$ - {msg}")

    def start():

        with asm.label('_start') as _s:     # tells linker entry point
           reg.edx = len                    # mov  edx,len     # message length
           reg.ecx = msg                    # mov  ecx,msg     # message to write
           reg.ebx = 1                      # mov  ebx,1       # file descriptor (stdout)
           reg.eax = 4                      # mov  eax,4       # system call number (sys_write)
           asm.int(128)                     # int  0x80        # call kernel
           reg.eax = 1                      # mov  eax,1       # system call number (sys_exit)
           asm.int(128)                     # int  0x80        # call kernel


A better future scope:

        import asm
        reg = asm.Register('x64')

        @asm.label                          # with asm.label('_start') as _s:
        def _start(name='msg'):             # tells linker entry point
           reg.edx = 'len'                  # mov  edx,len     # message length
           reg.ecx = name                   # mov  ecx,msg     # message to write
           reg.ebx = 1                      # mov  ebx,1       # file descriptor (stdout)
           reg.eax = 4                      # mov  eax,4       # system call number (sys_write)
           asm.interrupt.kernel()           # int  0x80        # call kernel
           reg.eax = 1                      # mov  eax,1       # system call number (sys_exit)
           asm.interrupt.kernel()           # int  0x80        # call kernel

        @asm.section.text
        def text_section():
            asm.global(_start)


        @asm.section.data
        def my_data_section():
            hw = asm.db('msg', 'Hello World')   # msg db 'Hello, world!', 0xa  ;string to be printed
            asm.equ.len = asm.last - hw         # len equ $ - msg     ;length of the string


---

        import asm
        reg = asm.Register('x64')
        sec = asm.section

        def main():
            my_section(sec.data)
            asm.ordered_write(sec.text, _start, sec.data)

        def my_section(data):
            data.msg = 'Hello World'             # # msg db 'Hello, world!', 0xa
            data.len = asm.equ(asm.$ - data.msg) # len equ $ - msg

        @asm.global(sec.text)
        def _start(name='msg'):             # tells linker entry point # with asm.label('_start')
           reg.edx = sec.data.len           # mov  edx,len     # message length
           reg.ecx = name                   # mov  ecx,msg     # message to write
           reg.ebx = 1                      # mov  ebx,1       # file descriptor (stdout)
           reg.eax = 4                      # mov  eax,4       # system call number (sys_write)
           asm.interrupt.kernel()           # int  0x80        # call kernel
           reg.eax = 1                      # mov  eax,1       # system call number (sys_exit)
           asm.interrupt.kernel()           # int  0x80        # call kernel

the global receives a place to write.. As global defines a section, the function is written as a section global can call. In ordered_write stage, the start values are printed to the file after the text section.

        @asm.global(sec.text)

add the incoming function as a `global func_name` statement with the `asm.section.text`. This is held in the until write time. when written the compiler will write the `section .text` section automatically; as it has an attached `global` statement.

It's possible to break the application through automation here; as nothing notes the `_start_` function and its content should be applied to the code. Indeed a _magic_ check of all statements, noting global needs a function and the function is named on the compiler stack. But assuming a block should be written may yield later problems.

As such an explicit method should be applied in the code - or another decorator.

        @asm.global(sec.text)
        @asm.label(write_here=True)
        def _start(name='msg'):
            ...

being a label, it should also write to space, unless explicity defined elsewhere.

A better ordered scope:

        import asm
        reg = asm.Register()

        def main():
            d=asm.section.data
            vitem = d.db('vers', 'version 1.0')
            d.len = asm.last - vitem

            ordered = asm.compile(
                    asm.section.text(),
                    _start(vers),
                    # _start('vers'),
                    asm.section.data(),
                )
            ordered.write('hello.asm')
            # asm.write('hello.asm')


========== END OF example hello world.md =========


=========== generator.md =========

The generator to create a file

+ create a _vm_ on the asm generator
+ receive functional executions in order
+ Keep object tree; possible parse down
+ Recursive flatten
+ make or read/render

========== END OF generator.md =========


=========== goal.md =========

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


========== END OF goal.md =========


=========== inc.md =========

simple addition

    mov rax, 5
    inc rax

+ Does not change carry:

    mov al, 255
    inc al

therefore change to

    mov al, 255
    ad al, 1

This time the add al will provide the carry flag.

    inc
    dec

does not change the carry flag. the above will produce an underflow without a carry flag.
A dec with underflag

    mov al, 0
    sub al, 1


===

the API should expose an inc like a standard increment.

    # literal
    asm.inc(reg.ebx)
    # other
    reg.ebx.inc()
    reg.ebx + 1



========== END OF inc.md =========


=========== instruction types.md =========

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

========== END OF instruction types.md =========


=========== jumps.md =========

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



========== END OF jumps.md =========


=========== magic-functionality.md =========

The magic statements help bridge ASM and python without the user getting involved.

## Decorator

Decororate a functional statement to encompass logic as executable ASM. This means coverting the literal python to literal ASM.

During standard execution the ASM is generated through specific functional calls, to generate a tree of compiled lines. This parsing doesn't include python statements. Essentially a file writer... To bridge this, decorating code will enact a magic convertor, reading python code as ASM logic and generating the correct ASM lines.

    if reg.ax == 1:
        asm.mov(reg.ax, 10)

In the above case, the `if` statement is inert to the ASM output, therefore this attempts a compilation tests on the ax value (not recommended). As an alternative:

    @magic
    def move_ax():
        if reg.ax == 1:
            asm.move(rex.ax, 10)

In this example the function is flagged to compile all the logic as ASM. This will result is more ASM lines than the expected `mov` statement; as the `if` will use full operand and jump execution testing.



========== END OF magic-functionality.md =========


=========== nodes.md =========

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

========== END OF nodes.md =========


=========== python for loops.md =========

At points you can use python to produce asm.

    mov eax, [ebp+8]
    mov esi, [ebp+12]
    mov edi, [ebp+16]

The following ASM can be a for loop:

    regs = [reg.eax, 'esi', reg.edi]
    for index, reg in enumerate(regs):
        i = 8 + (4 * index)
        asm.mov(reg, value_of=reg.ebp + i)

========== END OF python for loops.md =========


=========== reg.md =========

# Register

The registry combines a printer and a useful caller, used by the compiler
to render lines and the _vm_ to monitor registry usage. It allows meta and inline programming

It's a pretty easy thing to conceptualise - A register is split into rows. Each register item is a mutant caller. Certain attributes may be asserted for compliler type. This type may be given late; therefore multiple bay be required

    reg = Registry('x32')
    reg.al = 2

Each mutator action performs a change to the registry entity and applies a write statement to the ASM file.
All mutators define a asm action


    reg.rax = 5     ; mov rax, 5
    reg.rcx = 12    ; mov rcx, 23
    reg.rax + reg.rcx   ; add rax, rcx

The same is applied for all operands.

Special operations to shortcut tasks such as xor:

    # xor rcx, rcx
    reg.rax.xor()
    reg.rax.xor('rax')
    asm.xor(reg.rax)
    asm.xor("rax", 'rax')

clear:

    # mov, rcx, -1
    asm.mov('rax', -1)
    reg.rax.mov(-1)
    reg.rax = -1
    reg.rax.clear()


## Future

It would be nice to extend this. Like equals through xor == `NOT XOR`

    reg.rax.equal(1)
    reg.rax.not.xor()

========== END OF reg.md =========


=========== section.md =========

+ A block on content stored with an inline label

section .data
    labelThing db "some string", 10, 0
    len equ $ - labelThing
    # could hard code string length.
    len equ 40

    otherLabelThing db "some string", 10, 0
    len2 equ $ - otherLabelThing

Same can be done with 'segment'

========== END OF section.md =========


=========== templates.md =========

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

========== END OF templates.md =========


=========== why.md =========

# Discussion

I've been asked the question 'why' - spending a lot of time on a compiler, of which is clearly not as expressive or mature as every other compiler available, listing C/C++, GO, ASM, BASIC... the list continues. Indeed I've already spend many years on the thought, scratching broken concepts and hating code for a few months. However when I was a an egg I was captured with understandig computing at its core and I've always wanted to trully build my own language and stuff. Just for the bragging rights know-doubt but it's an excpetionally fun challenge to attempt a cliff of new ideas when research 'what is a pc'...

One day someone challenged me with a statement "you cannot build a an OS with python". As python is one of my favorite languages I felt jaded by this and set about seeing if it's possible. Indeed I agree it's a silly idea and does weigh with and fortitude; however is it possible?

This question grips me with a lot of theories. When someone stated "it can't be done..." I set about proving to myself if that's true. A simple but obtuse statement; I was once told man will never fly - or course they corrected themselves "without a plane" when I rebuttled. And today we have wing suits and hove boards and jet packs... In a lot of cases I take up this challenge with python.

Can I build an OS with pure python? No. Python needs a runtime environment. But I feel that's a minor proxy to the overall goal. In response, I question - can someone build an OS with C? Technically no. As C also compiled down. So what's the lowest language? I feel you asking - knowning full-well it's ASM. But it's not. Is it HEX? nope. Bits? Binary? Nope; microcode.

So. Aside from Linus and the mad hats at Intel; no one really writes true, core, bare-metal machine code.

##

Therefore why is this a fun project? As I feel code could go as low as I want (ASM is almost bare metal) and  compounding to another case of wanting to own the core machine, I can write it in python.

Why python? It's lovely. I've tried C, C++, ASM, and JS. Surprisingly the JS was a great platform. But linguistically I want to throw my high-level structures into a lower-level, without specifying the throughput on my development process. Although C is the optimal choice, It's still a different language and comes with its own burderns. MS VS Is amazing and deletes much of the build work, but with examples like 'pyMCU', I know it's possible to write low-level code with a cleaner high-level syntax.

Python to ASM, has been done many times and there are a lot of libraries to cater for this. But my end goal is to build a framework allowing me to abstract the terminology of CPU commands into a cleaner call-set, Then use that to write extremely low-level such as bootloaders. In addition I done want to depend on a specific builder or hook tools.

Therefore the compiler should create clean, flat, explicit asm - compiled by the chosen environment builder such as NASM.

========== END OF why.md =========


=========== with-statement.md =========

the python 'with' statement provides indentation to the written asm code, allowing for nested syntax such as `label` and `section`. Each asm module will utilise the with statmemt as required.

    with asm.section('.data'):
        asm.db('some string', 10, 0, label='myString')
        asm.equ('$', op.sub, 'myString', label='len'))

        otherLabelThing db "some string", 10, 0
        len2 equ $ - otherLabelThing

produces asm:

    section .data
        labelThing db "some string", 10, 0
        len equ $ - labelThing
        # len equ 40        # could hard code string length.
<!--
        otherLabelThing db "some string", 10, 0
        len2 equ $ - otherLabelThing
 -->

========== END OF with-statement.md =========


=========== xor.md =========

clearing a register can be doen with mov

    mov rcx, -1

but xor is faster

    xor rcx, rcx

asm block:

    asm.xor(reg.rcx)

xor against none can be the same register.

    sub ax, ax

+ if you NOT the result of an XOR you get an equals.

========== END OF xor.md =========

