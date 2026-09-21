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


# Base types

The registry item is usually printed as a string, used inline as a statement for asm

    asm.mov(value=2, into=reg.rax)
    # mov rax, 2

printing the value alone would break the code:

    raw(rex.rax)
    # rax
    ## Error

As python accepts many base forms they may be presented as standard form:

+ int
    standard form for all input
+ binary
    as an int, but printed literally `11010110`.
+ hex

    hex(0x10)


# Inspection

For debugging and compilation, the registry is tracked as a runtime object; to analyse for actions. Understanding this this functionality does not apply to the final asm file, this is generally called the 'meta scope'

    reg.rax = 5 # mov
    reg.rax + 10 # add

    print(reg.rax.changed, reg.changes)


## Spy

watch actions taken on the registry for compilation stage and meta scopes by spying on the registry key

@spy.write(reg.rax)
def rax_write(reg, value):
    print('Registry change', reg, value)

@spy(reg.rax):
def rax_change(reg, event):
    asm.mov(reg.name, -1)


# Errors

Compilation errors can detect typed errors through expected types before the ASM file is finished:

    reg = Reg('x16')
    asm.mov(10, into=reg.rax)
    # Error: cannot use 64 bit RAX with 16Bit Register

Silence these:

    from asm import errors

    asm.mov('rax', 10, errors=errors.warn_only) # print warning
    asm.mov('rax', 10, errors=errors.ignore) # scrub line

    # or via command line
    ./to_asm --file myfile.py --errors=warn_only

## Future

It would be nice to extend this. Like equals through xor == `NOT XOR`

    reg.rax.equal(1)
    reg.rax.not.xor()
