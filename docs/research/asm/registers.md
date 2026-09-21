# x86 register reference

This is a register catalog for the x86 target family used by the NASM-style
examples. It is organized by register role and width, not by instruction.
Availability depends on execution mode, CPU feature flags, and encoding rules.

The compiler should expose registers through a target profile instead of
assuming every name is valid in every program.

## General-purpose registers

### Legacy registers

These registers exist in 16-bit, 32-bit, and 64-bit x86 modes. The name selects
the accessible width:

| 64-bit | 32-bit | 16-bit | low 8-bit | high 8-bit |
| --- | --- | --- | --- | --- |
| `rax` | `eax` | `ax` | `al` | `ah` |
| `rbx` | `ebx` | `bx` | `bl` | `bh` |
| `rcx` | `ecx` | `cx` | `cl` | `ch` |
| `rdx` | `edx` | `dx` | `dl` | `dh` |
| `rsi` | `esi` | `si` | `sil` | none |
| `rdi` | `edi` | `di` | `dil` | none |
| `rbp` | `ebp` | `bp` | `bpl` | none |
| `rsp` | `esp` | `sp` | `spl` | none |

The `r8` through `r15` registers are available in 64-bit mode:

| 64-bit | 32-bit | 16-bit | low 8-bit |
| --- | --- | --- | --- |
| `r8` | `r8d` | `r8w` | `r8b` |
| `r9` | `r9d` | `r9w` | `r9b` |
| `r10` | `r10d` | `r10w` | `r10b` |
| `r11` | `r11d` | `r11w` | `r11b` |
| `r12` | `r12d` | `r12w` | `r12b` |
| `r13` | `r13d` | `r13w` | `r13b` |
| `r14` | `r14d` | `r14w` | `r14b` |
| `r15` | `r15d` | `r15w` | `r15b` |

`r8` through `r15` and their aliases are not available in 16-bit or 32-bit
execution mode. The 32-bit write form, such as `eax` or `r8d`, zero-extends
into the corresponding 64-bit register in 64-bit mode.

### Important encoding caveat

In 64-bit mode, the high-byte names `ah`, `bh`, `ch`, and `dh` cannot be encoded
in an instruction that uses a REX prefix. The compiler should validate this at
instruction encoding/rendering time, not merely accept every 8-bit register
combination.

The names `spl`, `bpl`, `sil`, and `dil` require a REX prefix in 64-bit mode.
They are not interchangeable with `ah`, `bh`, `ch`, or `dh`.

## Instruction-pointer registers

| Register | Width | Mode | Purpose |
| --- | ---: | --- | --- |
| `ip` | 16 | 16-bit | instruction pointer |
| `eip` | 32 | 32-bit | instruction pointer |
| `rip` | 64 | 64-bit | instruction pointer |

These are normally implicit. Direct writes to the instruction pointer use
control-flow instructions such as `jmp`, `call`, and `ret`, rather than ordinary
`mov` forms. `rip`-relative memory addressing is a 64-bit addressing feature,
not a normal general-purpose register operand.

## Flags registers

| Register | Width | Common use |
| --- | ---: | --- |
| `flags` | 16 | 16-bit flags register |
| `eflags` | 32 | 32-bit flags register |
| `rflags` | 64 | 64-bit flags register |

Important individual flags include:

| Flag | Bit | Meaning |
| --- | ---: | --- |
| `CF` | 0 | carry or borrow |
| `PF` | 2 | parity |
| `AF` | 4 | auxiliary carry |
| `ZF` | 6 | zero |
| `SF` | 7 | sign |
| `TF` | 8 | trap/single-step |
| `IF` | 9 | interrupt enable |
| `DF` | 10 | string direction |
| `OF` | 11 | signed overflow |

Most flags are read or written implicitly by instructions. The API should
model flag effects on operations rather than expose `rflags` as an ordinary
register for every instruction. For example, `inc` changes many arithmetic
flags but does not change `CF`.

## Segment registers

```text
cs  code segment
ss  stack segment
ds  data segment
es  extra data segment
fs  extra segment, commonly used for thread or system data
gs  extra segment, commonly used for thread or system data
```

Segment registers are 16-bit architectural registers. Segmentation behaves
differently in 16-bit, 32-bit, and 64-bit modes; in 64-bit operating systems,
`fs` and `gs` remain especially relevant while most legacy segmentation is
flat. They are not interchangeable with general-purpose registers.

## x87 floating-point stack

```text
st0  st1  st2  st3  st4  st5  st6  st7
```

The x87 register file is an eight-entry stack of 80-bit floating-point
registers. Instructions may use implicit `st0` and stack-position semantics,
so these should not be represented as ordinary flat registers without tracking
stack effects.

## MMX registers

```text
mm0  mm1  mm2  mm3  mm4  mm5  mm6  mm7
```

MMX registers are 64-bit integer/vector registers that alias the x87 register
storage. Mixing MMX and x87 instructions requires care because the shared state
must be cleared before returning to x87 use.

## SIMD registers

### XMM

SSE provides 128-bit registers:

```text
xmm0 - xmm7       32-bit mode and 64-bit mode
xmm8 - xmm15      64-bit mode
```

Some processors and operating-system configurations expose additional XMM
registers in 64-bit mode. The target profile should use the selected CPU and
ABI feature set when deciding the valid range.

### YMM

AVX extends the SIMD register width to 256 bits:

```text
ymm0 - ymm7       32-bit mode and 64-bit mode
ymm8 - ymm15      64-bit mode
```

The low 128 bits overlap the corresponding XMM register. A YMM operand is not a
new independent register name in the same sense as a general-purpose register;
it is a wider view of the SIMD state.

### ZMM and mask registers

AVX-512 provides 512-bit registers and opmask registers:

```text
zmm0 - zmm31
k0 - k7
```

Availability depends on AVX-512 hardware, operating-system support, and the
selected instruction form. `k0` often has special semantics and is not always
usable as a writable mask operand.

## System and implementation registers

These are useful for operating-system and kernel code, but should be placed in
a privileged register namespace rather than the ordinary user register list.

### Control registers

Common names are:

```text
cr0  cr2  cr3  cr4
cr8              ; available in 64-bit mode
```

`cr1` is reserved. Other control registers may exist on particular processors.
Access generally requires privileged execution, and each register has
instruction-specific read/write rules.

### Debug registers

```text
dr0  dr1  dr2  dr3
dr6  dr7
```

`dr4` and `dr5` are obsolete aliases or reserved depending on configuration.
Debug registers are privileged and have special breakpoint semantics.

### Test registers

Older x86 processors defined test registers such as `tr6` and `tr7`. They are
obsolete and should not be part of a modern default target profile.

## Register namespaces for the compiler

A practical internal model can classify registers like this:

```text
GeneralRegister(name="rax", width=64, mode="x64")
SubRegister(name="eax", parent="rax", width=32)
FlagRegister(name="rflags", width=64, implicit=True)
SegmentRegister(name="fs", width=16, privileged=False)
SimdRegister(name="xmm0", width=128, feature="sse")
MaskRegister(name="k1", width=64, feature="avx512")
ControlRegister(name="cr3", width=64, privileged=True)
```

Each register entry should record at least:

- canonical name and aliases;
- width in bits;
- architecture and execution-mode availability;
- parent or overlapping register, if any;
- required CPU feature;
- whether it is implicit, privileged, or special-purpose.

## Target notes

### NASM and x86

NASM uses these names directly in Intel-style operands:

```asm
mov eax, 10
mov rax, rbx
movdqu xmm0, [rdi]
```

The active `bits 16`, `bits 32`, or `bits 64` directive changes which names and
encodings are legal. CPU feature declarations and instruction selection also
affect SIMD register availability.

### GAS / AT&T x86

GAS typically prefixes register names with `%`:

```asm
movl $10, %eax
movq %rbx, %rax
movdqu (%rdi), %xmm0
```

The register model is the same x86 model; the renderer changes prefixes,
operand order, mnemonic suffixes, and memory syntax.

### AArch64

AArch64 has a different register file and should use a separate target profile:

```text
x0 - x30       64-bit general-purpose registers
w0 - w30       low 32-bit views of x0 - x30
sp             stack pointer
xzr / wzr      zero registers
v0 - v31       SIMD/floating-point registers
```

`x31` is context-dependent in instruction syntax and may represent `sp` or the
zero register; the target profile must retain that distinction. `pc` is not a
general-purpose operand in ordinary AArch64 instructions.

### WebAssembly

WebAssembly has no named CPU register file. It uses an operand stack, typed
locals, typed globals, and linear memory. A WASM target should expose locals
and stack values as compiler IR operands rather than pretending that `eax` or
`xmm0` exists.

## Recommended initial profile

For the first NASM-oriented implementation, expose only:

```text
x64: rax rbx rcx rdx rsi rdi rbp rsp r8-r15
     al ah bl bh cl ch dl dh
     sil dil bpl spl
     ax bx cx dx si di bp sp
     eax ebx ecx edx esi edi ebp esp
     rip rflags cs ss ds es fs gs
```

Add XMM, control, debug, and other special registers as feature-gated
namespaces. This keeps ordinary instruction validation small while leaving a
clear path to kernel and SIMD support.
