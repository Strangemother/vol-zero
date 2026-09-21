# Examples

These examples are syntax sketches. They show the intended API and emitted
assembly; they are not yet claims about an implemented compiler.

## 1. Literal API

```python
from asm import ASM, reg

program = ASM()
program.mov(reg.eax, 10)
program.add(reg.eax, reg.ecx)
print(program.render())
```

```asm
mov eax, 10
add eax, ecx
```

This is the baseline API. It should be implemented before syntactic sugar.

## 2. A small arithmetic program

```python
asm.mov(reg.rax, 5)
asm.mov(reg.rcx, 12)
asm.add(reg.rax, reg.rcx)
```

```asm
mov rax, 5
mov rcx, 12
add rax, rcx
```

The historical shorthand `rax = 5; rcx = 12; rax + rcx` is useful as a design
idea, but it needs explicit semantics for discarded expression results.

## 3. Register convenience methods

```python
reg.rax.set(5)
reg.rax.add(reg.rcx)
reg.rax.clear()             # implementation may choose xor rax, rax
reg.rax.inc()
```

Possible output:

```asm
mov rax, 5
add rax, rcx
xor rax, rax
inc rax
```

`inc` and `dec` deserve a warning in the design: unlike `add` and `sub`, they
do not update the carry flag on x86. A compiler optimization must not silently
replace one with the other when flags are observable.

## 4. Sections, labels, and data

```python
with asm.section(".text"):
    asm.global_("_start")
    with asm.label("_start"):
        asm.mov(reg.eax, 1)
        asm.call("exit")

with asm.section(".data"):
    message = asm.db("Hello, world!", 10, label="message")
    asm.equ("message_length", asm.current_location() - message)
```

The `with` statement is an authoring convenience for nesting. The renderer
still owns the final section and label syntax.

## 5. Calls and reusable blocks

```python
def clear_screen(asm):
    with asm.label("clear_screen"):
        asm.push(reg.bp)
        asm.mov(reg.bp, reg.sp)
        asm.raw("; body supplied by the target-specific demo")
        asm.pop(reg.bp)
        asm.ret()

clear_screen(asm)
asm.call("clear_screen")
```

A decorator may be added later, but a normal function that receives the program
is easier to inspect and test first.

## 6. Build-time generation

Python is useful for repetitive assembly generation:

```python
registers = [reg.eax, reg.esi, reg.edi]
for index, destination in enumerate(registers):
    asm.mov(destination, reg.ebp.memory(offset=8 + 4 * index))
```

The loop runs during compilation and emits three explicit `mov` operations.

## 7. Errors and warnings

```python
program = ASM(mode="x16")
program.mov(reg.rax, 10)
```

Expected diagnostic:

```text
error: rax is a 64-bit register and cannot be used in x16 mode
```

A command-line policy may later select `error`, `warn`, or `ignore`, but the
internal diagnostic should remain structured rather than printed immediately.
