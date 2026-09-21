# `mov` design reference

This document is the single design reference for `mov` in LAT (Literal ASM
Transpiler). It extracts the `mov` and `move` ideas scattered through the
research archive and turns them into one model that can later generalize to
other two-parameter instructions such as `add`, `sub`, `cmp`, `xor`, and
`test`.

The examples use x86 Intel/NASM terminology unless a target is named
explicitly.

## Purpose and semantics

`mov` copies a source value into a destination. It does not perform arithmetic
and it does not read memory merely because an operand is written using memory
syntax: the operand type determines whether the value is a register, an
immediate, a label address, or memory contents.

```text
mov <destination>, <source>
```

For x86, the destination is the first operand in Intel/NASM syntax. The source
is the second operand. Direct memory-to-memory `mov` is not a valid x86 form.

The operation should be represented semantically as:

```text
Operation(
    opcode="mov",
    destination=<operand>,
    source=<operand>,
)
```

The renderer, rather than the operation model, decides whether this becomes
Intel syntax, AT&T syntax, or another target representation.

## Supported x86 operand shapes

These are the core x86 forms to support in the first target profile:

```text
mov <reg>, <reg>
mov <reg>, <mem>
mov <mem>, <reg>
mov <reg>, <imm>
mov <mem>, <imm>
```

Additional x86-specific forms should be represented as separate signatures or
feature-gated extensions:

```text
mov <seg>, <reg16|mem16>
mov <reg16|mem16>, <seg>
mov <control-reg>, <reg>
mov <reg>, <control-reg>
mov <debug-reg>, <reg>
mov <reg>, <debug-reg>
```

These special forms have privilege, mode, width, and encoding restrictions.
They should not be accepted merely because both operands can be printed as
strings.

The following form is invalid for ordinary x86 `mov`:

```text
mov <mem>, <mem>
```

The compiler should report this before invoking NASM. A caller can still use
`raw()` when intentionally emitting target-specific text that the current
model does not understand.

## Operand categories

The `mov` signature needs typed operands rather than unconstrained values:

| Category | Examples | Meaning |
| --- | --- | --- |
| Register | `rax`, `eax`, `al`, `r8d` | CPU register, with a defined width and target availability. |
| Immediate | `5`, `-1`, `0xff`, binary literal | Literal value encoded into the instruction. |
| Memory | `[rax]`, `[ebp + 8]`, `[message]` | Addressed storage; size may need an explicit qualifier. |
| Label/reference | `message`, `message_length` | Symbolic address or assembler expression; interpretation is target-specific. |
| Segment/control/debug register | `ds`, `cr3`, `dr0` | Special register forms with additional constraints. |

A Python string such as `"eax"` is ambiguous until the target operand parser
classifies it. The long-term API should prefer `Register`, `Immediate`, `Memory`,
and `LabelRef` objects. String operands may remain a convenient shorthand for
simple examples.

## Current LAT API

The canonical current form is positional and preserves destination/source order:

```python
from lat import ASM, Reader, Registers

asm = ASM()
reg = Registers()
asm.mov(reg.eax, 10)
asm.mov(reg.eax, reg.edx)
print(Reader(asm).flat_resolve())
```

Expected output:

```asm
mov eax, 10
mov eax, edx
```

The current recorder dynamically creates an instruction object when `asm.mov`
is accessed. It records the call and the reader resolves it later. At present,
this is recording and text rendering, not instruction validation or machine
simulation.

## Proposed API forms from the archive

The research notes describe several equivalent authoring levels:

### Explicit positional form

```python
asm.mov(reg.eax, 10)
asm.mov("eax", 10)
```

This is the recommended foundation because the two semantic roles are visible
and it maps directly to the operation model.

### Named semantic form

```python
asm.mov(value=10, into=reg.eax)
asm.mov(value=10, into="eax")
```

The names `value` and `into` express source and destination more clearly for
some callers. The implementation should normalize this into
`destination=reg.eax, source=10` before recording.

The archive also contains `to=...`:

```python
asm.mov(10, to=reg.eax)
```

Choose one canonical keyword vocabulary. Recommended names are
`destination` and `source`; `into` and `value` may be accepted aliases at the
API boundary, but aliases should not create different operation types.

### Register convenience form

```python
reg.eax.set(10)
reg.eax.mov(10)
```

These are convenience methods that lower to the same `mov` operation. They
should be implemented after the explicit API and must retain the destination
register as structured data.

### Assignment sugar, deferred

The notes repeatedly propose:

```python
reg.eax = 10       # intended output: mov eax, 10
```

Ordinary Python assignment cannot be intercepted reliably by a register object.
Treat this as a future DSL or proxy design, not as the semantic foundation.

### Expression sugar, deferred

The archive also proposes:

```python
move(10, into=reg.eax)
reg.eax + reg.ecx       # intended output: add eax, ecx
```

`move()` can be a named helper, but bare expressions have Python evaluation
semantics and should not silently emit assembly until their behavior is
specified.

### Literal/raw form

```python
asm.raw("mov eax, 10")
```

Raw text is an escape hatch for unsupported directives, dialect-specific
syntax, or experiments. It should be visibly target-specific and should not be
used as the normal representation of `mov`.

## Two-parameter instruction contract

`mov` establishes the reusable contract for ordinary binary instructions:

```text
instruction(destination, source)
```

The shared operation layer should provide:

1. two semantic operand slots, `destination` and `source`;
2. operand classification and width information;
3. target-specific legality constraints;
4. explicit read/write effects;
5. a renderer that may reorder operands for the target dialect;
6. stable source metadata for diagnostics and tests.

The instruction-specific signature supplies the differences:

| Instruction | Destination effect | Source effect | Typical flags |
| --- | --- | --- | --- |
| `mov` | overwritten | read | no arithmetic flags changed |
| `add` | replaced with destination + source | read | arithmetic flags written |
| `sub` | replaced with destination - source | read | arithmetic flags written |
| `cmp` | not retained as a value | read | flags written only |
| `xor` | replaced with bitwise XOR | read | flags written |
| `test` | not retained as a value | read | flags written only |

This table describes semantic roles, not necessarily the target's printed
operand order.

## Validation rules

A `mov` validator should check, in order:

1. **Arity:** exactly two explicit operands.
2. **Operand categories:** both operands are supported for the selected form.
3. **Destination capability:** the destination can be written.
4. **Memory rule:** reject memory-to-memory x86 forms.
5. **Width:** register, immediate, and memory widths are compatible.
6. **Mode:** register and address forms are legal in `bits 16`, `bits 32`, or
   `bits 64` mode.
7. **Feature/privilege:** special registers and SIMD forms meet target profile
   requirements.
8. **Symbol resolution:** labels and expressions are valid or deferred in a
   documented way.
9. **Encoding caveats:** for example, high-byte registers cannot be used with
   a REX-prefixed x86-64 instruction.

Examples:

```text
mov rax, 5                 valid in x86-64
mov rax, rbx               valid in x86-64
mov [rax], rbx             valid when the memory width is known
mov [rax], 5               valid when the memory width can be inferred
mov [rax], [rbx]           invalid x86 memory-to-memory form
mov rax, 5                 invalid in a 16-bit-only profile
```

Diagnostics should identify the operation, operand position, expected category,
actual category, and target profile. They should be structured before being
formatted for a command line.

## Abstract state and effects

The notes propose tracking register values in a Python-side pseudo-VM. For
`mov`, the minimal abstract effect is:

```text
before:  rax = unknown
apply:   mov rax, 5
after:   rax = known(5)
```

For a register copy:

```text
before:  rax = unknown, rbx = known(7)
apply:   mov rax, rbx
after:   rax = known(7), rbx = known(7)
```

This state is compile-time analysis only. It does not replace runtime CPU
execution. Unknown values, memory aliases, calls, and raw instructions must be
allowed to invalidate or widen the tracked state.

`mov` does not change arithmetic flags on x86. This effect should be explicit
so later optimizations do not treat it like `add`, `sub`, or `inc`.

## Rendering targets

### Intel/NASM

```text
mov eax, 10
mov eax, ebx
```

The first operand is the destination. Register names have no prefix, and
memory syntax uses brackets.

### GAS/AT&T

```text
movl $10, %eax
movl %ebx, %eax
```

The semantic destination/source pair is reversed in printed operand order.
Immediate and register prefixes, mnemonic width suffixes, and memory syntax
belong to the renderer.

### AArch64

AArch64 has a different `mov` encoding family but retains a destination/source
shape for basic register and immediate forms:

```text
mov x0, x1
mov w0, #10
```

Loads and stores are separate instructions:

```text
ldr x0, [x1]
str x0, [x1]
```

The shared binary-operation abstraction can be reused, but the target profile
must not import x86 memory forms into AArch64 `mov`.

### WebAssembly

WebAssembly has no register-form `mov`. Equivalent operations use locals and a
typed operand stack:

```text
local.get 0
local.set 1
```

A cross-target compiler should lower an abstract copy into target-specific
operations rather than inventing `mov eax, ...` for WASM.

## Labels, data, and addresses

The research examples use `mov` with labels and data:

```asm
mov edx, message_length
mov ecx, message
```

These are not the same as loading memory contents through `[message]`. The
operand model should distinguish:

```text
LabelRef("message")       ; symbolic address/reference
Memory(LabelRef("message")) ; contents at the address
```

The exact relocation and address-size rules belong to the target profile and
object format. `db`, `equ`, `section`, and `global` are directives, not `mov`
operands, but they participate in resolving these references.

## Source inventory

The extracted ideas come from these notes:

| Source | Contribution |
| --- | --- |
| [api.md](api.md) | Positional, named, parse/reverse-parse, string rendering, target dialects, raw and mixed API levels. |
| [asm.md](asm.md) | `move(value, into=...)`, basic two-value commands, pseudo-VM, statement capture. |
| [concepts.md](concepts.md) | Typed operands, operation IR, register state, explicit API baseline, validation. |
| [goal.md](goal.md) | Literal abstraction, register placeholders, compile-time checks, sugar, raw blocks, target syntax. |
| [instruction types.md](instruction types.md) | x86 operand categories and legal `mov` shape families. |
| [instruction-signatures.md](instruction-signatures.md) | Operand arity, implicit effects, target profiles, and initial coverage. |
| [nodes.md](nodes.md) | Architectural `mov` semantics and memory-to-memory restriction. |
| [reg.md](reg.md) | Register mutation, `asm.mov`, register sugar, inspection, and typed errors. |
| [registers.md](registers.md) | Register aliases, widths, modes, and special-register constraints. |
| [python-poc.md](python-poc.md) | Minimal `Program.mov(destination, source)` recorder and abstract state. |
| [examples.md](examples.md) | Concrete positional and register-convenience examples. |
| [demos.md](demos.md) | Arithmetic, hello-world, diagnostics, and platform-specific pressure tests. |
| [example/](example/) | Historical bootloader and BIOS-oriented register assignment ideas. |
| [combined.md](combined.md) | Preserved archive containing the earlier variants and examples. |

## Recommended implementation order

1. Keep positional `asm.mov(destination, source)` as the canonical API.
2. Represent operands and semantic roles instead of preformatted strings.
3. Add exact output tests for zero-width-known register/immediate examples.
4. Add x86 memory operands and reject memory-to-memory forms.
5. Add width and mode validation.
6. Add named argument normalization with one canonical vocabulary.
7. Add Intel/NASM rendering, then an AT&T renderer over the same operation.
8. Add abstract register state and invalidation rules.
9. Add labels, addresses, and data directives.
10. Add register methods and other sugar only after the explicit path is stable.

Every two-parameter instruction can then reuse the operation, operand, target
profile, diagnostic, and renderer infrastructure while supplying its own
constraints and effects.
