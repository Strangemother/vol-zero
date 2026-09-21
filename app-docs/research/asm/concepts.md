# Compiler concepts

## Purpose

The compiler lets Python describe low-level programs while emitting explicit,
ordinary assembly for a selected assembler. Python is the authoring and build
language; the output assembly remains the inspectable product.

The project is intentionally an abstraction layer, not a replacement CPU
language. A user should be able to choose between literal assembly, structured
API calls, and concise register syntax without losing control of the emitted
instructions.

## Pipeline

```text
Python source
    -> recorded operations (IR)
    -> validation and optional abstract-machine state
    -> target syntax renderer
    -> .asm text
    -> external assembler and linker
    -> binary
```

The recorder is the important boundary. Every supported API operation creates
an operation in order; rendering and validation happen after recording. This
makes output deterministic and allows the same program to be inspected,
rendered in Intel syntax, or rendered in AT&T syntax.

Python control flow runs at build time. It generates operations, selects
operations, or repeats operations. It is not automatically runtime assembly
control flow. Runtime `if`, loops, and jumps must be represented by explicit
assembly operations or a future compiler construct.

## Core objects

### Operand

An operand is a typed value such as a register, immediate, label, memory
reference, or expression. It should retain enough information to validate
instruction forms and render target syntax.

Suggested initial forms:

```python
Register("rax", width=64)
Immediate(5)
LabelRef("message")
Memory(base=Register("ebp"), offset=8)
```

### Operation

An operation is an instruction or directive with an opcode and operands.
Examples include `mov`, `add`, `inc`, `xor`, `call`, `section`, `db`, and `equ`.
An operation should be printable without requiring the simulator.

### Program and blocks

A program owns ordered operations. Sections and labels provide structure and
indentation for the authoring API, but the final output is a flat ordered
assembly file. A block may be built by a Python function and inserted explicitly
into a program.

### Register file

The register file has two roles:

1. It provides typed operand objects such as `reg.rax`.
2. It optionally tracks abstract state for diagnostics, such as the known
   value of `rax` after `mov rax, 5`.

Register state is meta-time information. It must never be confused with the
runtime value in the generated binary.

## API levels

These forms should describe the same operation where possible:

```python
asm.mov(reg.rax, 5)                 # explicit API
asm.mov(value=5, into=reg.rax)      # named operands
reg.rax.set(5)                      # register convenience API
```

Assignment and operator overloading are attractive sugar, but they should be
added only after the explicit API is stable. Python assignment cannot be
intercepted reliably for every desired assembly meaning, so `reg.rax = 5`
should remain a proposal rather than a foundation.

Raw assembly is an escape hatch, not a normal API:

```python
asm.raw("bits 16")
```

Raw text should be marked as target-specific and should bypass only the checks
that the compiler cannot understand.

## Validation

Instruction signatures describe legal operand combinations and widths. The
full shape reference, including NASM, GAS, AArch64, and WebAssembly profiles,
is in [Instruction signatures](instruction-signatures.md).

For the initial x86 profile, the basic `mov` forms are:

```text
mov <reg>, <reg>
mov <reg>, <mem>
mov <mem>, <reg>
mov <reg>, <const>
mov <mem>, <const>
```

Validation should report errors before invoking the external assembler when it
can. Examples include using `rax` in a 16-bit program, using an invalid memory
form, or referencing an unknown label. Warnings can cover less certain issues,
such as a flag being written and never read.

## Target syntax

The operation model is target-neutral where possible. The renderer owns syntax:

```text
Intel: mov eax, 10
AT&T:  movl $10, %eax
```

The same operation should not be represented as a preformatted string. This is
what makes multiple renderers, validation, and later architecture support
possible.

## Scope boundary

The first useful compiler should support one architecture, one assembler, and
a small instruction set. The historical notes mention x86, ARM, BIOS, NASM,
AT&T, and multiple assembler conventions; these are research inputs, not a
requirement for the first implementation.
