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

```py
    # literal
    asm.mov("al", 2)
    asm.mov(reg.al, 2)
    # pythonic
    move(value=2, into='al')
    # pseudo
    reg.al + 10
    # inline (not compiler safe)
    raw('add eax, edx')
```