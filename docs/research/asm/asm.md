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

