# Instruction signature reference

This is a shape reference, not an exhaustive instruction list. It answers:

- how many explicit operands an operation may expose;
- what kinds of operands may occupy each position;
- which operations have implicit operands or results;
- how the same idea changes between target families.

The compiler should model these signatures as structured metadata. A mnemonic
alone is not enough: `mov`, `add`, and `call` each have target- and mode-
specific forms.

## Notation

```text
<reg>       register
<reg8>      8-bit register
<reg32>     32-bit register
<reg64>     64-bit register
<mem>       memory operand
<imm>       immediate constant
<label>     symbolic address or branch target
<port>      I/O port
<shift>     immediate or register shift count
<mask>      immediate or vector mask
```

A comma separates explicit operands. The leftmost operand is the destination
for Intel/NASM-style examples unless the target says otherwise. These are
signatures, not Python function signatures: a variadic Python API may still
need to reject a particular operand combination.

## The main operand shapes

### Zero explicit operands

```text
ret
iret
nop
hlt
clc | stc | cmc
cli | sti
```

These may still have implicit effects. For example, `ret` reads the stack and
changes the instruction pointer, while `clc` changes flags.

### One explicit operand

```text
inc <reg|mem>
dec <reg|mem>
neg <reg|mem>
not <reg|mem>
push <reg|mem|imm>
pop <reg|mem>
call <label|reg|mem>
jmp <label|reg|mem>
```

Unary instructions often mutate their operand. `push`, `pop`, `call`, and
`jmp` also have implicit stack or instruction-pointer operands.

### Two explicit operands

This is the common destination/source shape:

```text
mov <reg|mem>, <reg|mem|imm>
add <reg|mem>, <reg|mem|imm>
sub <reg|mem>, <reg|mem|imm>
and <reg|mem>, <reg|mem|imm>
or  <reg|mem>, <reg|mem|imm>
xor <reg|mem>, <reg|mem|imm>
cmp <reg|mem>, <reg|mem|imm>
test <reg|mem>, <reg|mem|imm>
```

Each mnemonic still has restrictions. For example, x86 generally disallows a
memory-to-memory form for `mov`, `add`, and similar instructions, and `cmp`
has no destination value even though it has two operands.

Other two-operand shapes include:

```text
shl <reg|mem>, <shift>
shr <reg|mem>, <shift>
rol <reg|mem>, <shift>
cmov<cc> <reg>, <reg|mem>
set<cc> <reg8|mem>
lea <reg>, <mem>
```

`lea` does not load memory contents; it computes an address. `set<cc>` writes
one byte based on flags.

### Three explicit operands

Some instruction families add an explicit destination or a third control
operand:

```text
imul <reg>, <reg|mem>, <imm>
shld <reg|mem>, <reg>, <shift>
shrd <reg|mem>, <reg>, <shift>
blend<variant> <xmm>, <xmm|mem>, <mask>
```

Three operands are less common in classic x86 integer instructions. The
signature registry must not assume every instruction is unary or binary.

### Variable-length operand lists

Data and macro-like directives commonly accept one or more values:

```text
db <value>...
dw <value>...
dd <value>...
dq <value>...
```

The API should represent these as a list of operands, while validating each
item and the directive's element width. An empty list should normally be
rejected.

## Implicit-operand families

Some instructions look like one- or two-operand operations but read or write
fixed architectural locations:

```text
mul <reg|mem>       ; implicit accumulator, produces a wider result
imul <reg|mem>      ; one-operand signed multiply form
idiv <reg|mem>      ; implicit dividend and quotient/remainder registers
in <reg>, <port|imm>
out <port|imm>, <reg>
loop <label>        ; implicit counter register
```

These should carry explicit metadata such as `implicit_reads` and
`implicit_writes`. Hiding these effects would make register tracking and
validation unreliable.

String instructions are another special family. Their source, destination,
count, and flags are implicit in the instruction encoding:

```text
movs<width>
cmps<width>
scas<width>
lods<width>
stos<width>
```

A useful API may expose a width and repeat modifier rather than pretending that
these are ordinary two-operand moves.

## Control-flow signatures

Conditional branches have one explicit target and an implicit condition:

```text
j<condition> <label>
call <label|reg|mem>
jmp <label|reg|mem>
ret [<imm>]
```

The condition belongs in the operation type or opcode metadata, not as an
ordinary runtime boolean operand. `asm.jump_if_carry("carry_path")` should
therefore lower to `jc carry_path`, while Python `if` remains build-time
control flow unless a separate runtime control-flow API is used.

## Directives are not instructions

Assemblers also accept directives. They have signatures, but they do not
execute on the CPU:

```text
section <name>
global <symbol>
extern <symbol>
equ <symbol>, <expression>
org <address>
bits <width>
 times <count>, <value>
```

Data directives are usually variadic as shown above. Directives should be a
separate operation category so the compiler does not apply CPU instruction
rules to them.

## NASM and x86 target profile

NASM uses Intel operand order and syntax. A useful initial profile can support
these signature families:

| Family | Signature shapes | Notes |
| --- | --- | --- |
| Move/data | `reg, reg`; `reg, mem`; `mem, reg`; `reg, imm`; `mem, imm` | Usually no memory-to-memory move; size may need `byte`, `word`, `dword`, or `qword`. |
| Arithmetic/logic | `dst, src` | Destination is mutated; flags are usually affected. |
| Unary | `reg|mem` | `inc`, `dec`, `neg`, and `not` differ in flag behavior. |
| Shift/rotate | `dst, imm|cl` | Some forms use the implicit `cl` register. |
| Compare/test | `lhs, rhs` | Writes flags, not a destination value. |
| Conditional set | `reg8|mem` | Reads flags and writes one byte. |
| Branch | `label` or `reg|mem` | Direct and indirect forms differ by mnemonic/encoding. |
| Stack | `reg|mem|imm` for push; `reg|mem` for pop | Stack pointer is implicit. |
| Multiply/divide | `reg|mem`, or explicit three-operand `imul` | Accumulator and high/low result registers may be implicit. |
| I/O | `reg, port` or `port, reg` | Port may be immediate or in `dx`. |
| Data | `value...` | `db`, `dw`, `dd`, and `dq` are assembler directives. |

NASM is an assembler, not a CPU architecture. The same x86 operation will have
different spelling or availability depending on `bits 16`, `bits 32`, or
`bits 64` and on the selected object/output format.

## GAS and other x86 syntax

GNU assembler can use AT&T syntax or Intel syntax. The operation shapes are
mostly the same as NASM for x86, but the renderer must account for:

```text
AT&T:   addq %rcx, %rax       # source, destination
Intel:  add rax, rcx          # destination, source
AT&T:   movq $5, %rax         # immediate and register markers
Intel:  mov rax, 5
```

Do not encode operand order in the shared operation. Store semantic roles such
as `destination` and `source`, then let the renderer choose spelling, suffixes,
and markers. GAS directives and object-format rules also differ from NASM.

## AArch64 and other register machines

The same broad shapes recur, but the legal combinations are different:

```text
mov <reg>, <reg|imm>
add <reg>, <reg>, <reg|imm>
ldr <reg>, <mem>
str <reg>, <mem>
cmp <reg>, <reg|imm>
b.<condition> <label>
bl <label|reg>
```

AArch64 commonly uses a three-operand arithmetic form with a distinct
 destination. It also has load/store instructions rather than x86-style
arithmetic directly against most memory operands. This is why signatures must
belong to an architecture profile, not to a global mnemonic table.

## WebAssembly target profile

WebAssembly is not an assembly language with register operands. It is a typed,
stack-machine bytecode format. Its instruction signatures are best written as
stack effects:

```text
unreachable                 (--) -> unreachable
nop                         (--) -> (--)
i32.const <imm>             (--) -> (i32)
i32.add                     (i32, i32) -> (i32)
i32.load [memarg]           (i32) -> (i32)
i32.store [memarg]          (i32, i32) -> (--)
local.get <localidx>         (--) -> (type)
local.set <localidx>         (type) -> (--)
call <funcidx>               (params...) -> (results...)
br_if <labelidx>             (i32) -> (--)
return                      (results...) -> return
```

The values before the arrow are consumed from the operand stack and the values
after it are produced. `local.get`, `local.set`, `global.get`, and
`global.set` use explicit indices, but the values still move through the
stack. Memory instructions additionally have a `memarg` immediate containing
an alignment and offset.

WebAssembly blocks introduce another signature shape:

```text
block <blocktype> ... end
loop <blocktype> ... end
if <blocktype> ... else ... end
```

A block type declares the values it accepts and returns. This is closer to a
function type than to x86's comma-separated operands. A shared compiler API
should therefore use an abstract operation plus a target-specific lowering,
not render `mov <reg>, <imm>` into WASM directly.

## Proposed signature data model

A compact internal description could look like this:

```python
Signature(
    mnemonic="mov",
    operands=[OperandRole("destination", {REG, MEM}),
              OperandRole("source", {REG, MEM, IMM})],
    constraints=["not_memory_to_memory"],
    implicit_reads=[],
    implicit_writes=[],
    effects=["writes_destination"],
    targets=["x86"],
)
```

For WebAssembly, use a stack-effect signature instead:

```python
StackSignature(
    mnemonic="i32.add",
    pops=[I32, I32],
    pushes=[I32],
    targets=["wasm32", "wasm64"],
)
```

This gives the library a stable validation vocabulary without pretending that
all targets have the same operand model.

## Recommended initial coverage

For the first implementation, support only the signature families needed by
the arithmetic, hello-world, and diagnostic demos:

```text
mov:   reg, reg|imm|mem; mem, reg|imm
add:   reg|mem, reg|imm
sub:   reg|mem, reg|imm
cmp:   reg|mem, reg|imm
xor:   reg|mem, reg|imm
inc:   reg|mem
call:  label
jmp:   label
j<cc>: label
ret:   [imm]
db:    value...
section: name
global:  symbol
equ:     symbol, expression
```

Expand the table only when a demo or target requires it. This keeps the
signature system useful without turning the first compiler milestone into a
complete instruction encyclopedia.
