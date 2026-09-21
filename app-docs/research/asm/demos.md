# Demonstrations

Demos are small, end-to-end targets. Each should eventually be runnable,
rendered, assembled, and compared with an expected artifact. They are not API
specifications; they are user-facing pressure tests for the concepts.

## Demo 1: render arithmetic

Goal: prove that the recorder and Intel renderer preserve operation order.

Input:

```python
asm.mov(reg.rax, 5)
asm.mov(reg.rcx, 12)
asm.add(reg.rax, reg.rcx)
```

Expected output:

```asm
mov rax, 5
mov rcx, 12
add rax, rcx
```

## Demo 2: hello world

Goal: prove sections, labels, data declarations, constants, and a platform
specific system-call example.

The historical 32-bit Linux example is retained as a target-specific demo:

```python
with asm.section(".text"):
    asm.global_("_start")
    with asm.label("_start"):
        asm.mov(reg.edx, LabelRef("message_length"))
        asm.mov(reg.ecx, LabelRef("message"))
        asm.mov(reg.ebx, 1)
        asm.mov(reg.eax, 4)
        asm.interrupt(0x80)
        asm.mov(reg.eax, 1)
        asm.interrupt(0x80)

with asm.section(".data"):
    message = asm.db("Hello, world!", 10, label="message")
    asm.equ("message_length", asm.current_location() - message)
```

The demo must declare its ABI and assembler dialect. It should not be presented
as portable assembly or as a bootloader example.

## Demo 3: boot-sector template

Goal: test raw directives, origin, labels, calls, memory operands, padding, and
an output-size assertion.

The historical template uses `bits 16`, `org 0x7c00`, BIOS interrupt `0x10`,
and the `0xaa55` boot signature. This should become a separate target profile,
not part of the generic API demo. Acceptance checks:

- output has the expected origin and mode directives;
- the boot signature is at offset 510;
- the generated image is exactly 512 bytes;
- the external assembler accepts the file.

## Demo 4: flag-sensitive arithmetic

Goal: ensure an optimization does not change observable flags.

```python
asm.mov(reg.al, 255)
asm.inc(reg.al)
asm.jump_if_carry("carry_path")
```

The compiler must preserve `inc` here because the demo is explicitly about the
carry flag. A separate `add al, 1` example should show the different behavior.

## Demo 5: invalid operand diagnostics

Goal: prove validation is useful before assembly.

```python
asm.mov(reg.rax, 10, mode="x16")
```

The expected result is a structured compiler error, not an assembler crash and
not silently generated invalid output.

## Demo order

Implement and run the demos in order: arithmetic, diagnostics, sections and
hello world, reusable blocks, then boot-sector and flag-sensitive targets. This
keeps platform-specific details from determining the core design too early.
