# Roadmap and open decisions

## Recommended build order

1. Define immutable operands and ordered operations.
2. Implement `Program` recording for `mov`, `add`, and `ret`.
3. Render one assembler dialect and test exact output.
4. Add instruction signatures and structured diagnostics.
5. Add labels, sections, `db`, and `equ`.
6. Add calls and reusable Python build-time functions.
7. Add memory operands and a second target renderer.
8. Add abstract register state and flag tracking as optional analysis.
9. Add convenience methods such as `clear()` and `inc()`.
10. Add decorators and operator sugar only after the explicit API is stable.

## Decisions to make

### What is the first target?

The notes mix x86-64, x86-32, x86-16 BIOS, Linux system calls, NASM syntax,
and AT&T syntax. Select one initial profile, for example x86-64 Intel syntax
with NASM, and label every other example as target-specific.

### What is the intermediate representation?

The current proposal is an ordered list of typed operations with nested source
metadata for sections and labels. A graph can be added if control-flow or
macro expansion needs it, but a graph should not be assumed merely because the
larger VOL project is graph-oriented.

### Is there a simulator?

There are three different features in the notes:

- abstract register tracking for diagnostics;
- a full instruction simulator;
- an external emulator such as Unicorn.

Start with abstract tracking. Treat full simulation and Unicorn integration as
separate tools with separate correctness expectations.

### How much Python should become assembly?

Normal Python is build-time metaprogramming. It may generate repeated
operations and choose branches while building. Runtime assembly control flow
requires explicit API calls or a future restricted DSL. The `@magic` proposal
should remain experimental until this boundary is specified.

### Which sugar is safe?

Explicit calls such as `asm.mov(reg.rax, 5)` are unambiguous. Methods such as
`reg.rax.clear()` are manageable sugar. Bare expressions such as `reg.rax +
reg.rcx` and assignment such as `reg.rax = 5` are attractive but can conflict
with Python evaluation and should not define core semantics.

## Historical proposal status

- **Keep:** typed registers, ordered recording, explicit renderer, sections,
  labels, data directives, diagnostics, build-time Python loops.
- **Prototype later:** decorators, `with`-based block syntax, asset injection,
  reverse parsing, flag-use analysis, and alternate renderers.
- **Defer:** automatic translation of arbitrary Python control flow, implicit
  function capture, and a complete CPU VM.
- **Treat as target demos:** BIOS wait, screen clearing, boot-sector templates,
  Linux hello world, and architecture-specific register tables.

## Definition of done for the concept phase

The concept is ready for implementation when the first target, operation model,
validation policy, renderer contract, and build-time/runtime boundary are
written down and demonstrated by the arithmetic and diagnostic demos.
