# Balanced Ternary and Binary Particle Mapping

> **Status: proposed implementation model.** Companion to [Ternary Particle Model](ternary-particles.md). This document does not replace the original particle definition, and does not claim the mapping is already implemented.

## Purpose and terminology

A **particle** measures a quantity of VOL information, analogous to a byte. It is **not** a type tag or semantic descriptor. A default particle comprises **two triplets**, each with three trits: six trits total, or **729 possible states**. Type, meaning, and interpretation belong to the surrounding context.

The companion particle document illustrates conventional unbalanced ternary digits (0, 1, 2). VOL's *preferred computational interpretation* is **balanced ternary**: each trit is −1, 0, or +1. Both alphabets have three states per trit and can describe the same 729 physical code points. The encoding convention must be explicit at an interface boundary.

## Balanced representation

A balanced six-trit particle is a vector $t=(t_0,\ldots,t_5)$ with $t_i\in\{-1,0,+1\}$. With the leftmost trit most significant, its signed value is:

```math
V(t)=\sum_{i=0}^{5}t_i 3^{5-i}
\qquad\text{where}\qquad -364\le V(t)\le364.
```

The state count remains:

```math
3^6=729=2\times364+1.
```

This is a **signed interpretation**, not metadata embedded in a particle.

## Worked example: six logical trits to binary

Consider the particle:

```text
Triplet A         Triplet B
[ +1, 0, −1 ]     [ 0, +1, −1 ]
└──── 3 trits ─┘  └──── 3 trits ─┘
          6 trits total
```

Its signed balanced-ternary value is:

```math
V=1\cdot3^5+0\cdot3^4-1\cdot3^3+0\cdot3^2+1\cdot3^1-1\cdot3^0
=243-27+3-1=218.
```

To store *every* possible signed particle value in a nonnegative binary code, bias by **364**:

```math
C=V+364=582.
```

Convert 582 into exactly **10 binary bits**:

```text
Logical particle: [+1, 0, −1] [0, +1, −1]
Signed integer:    +218
Biased code:        582
Binary encoding:    1001000110
```

This maps an entire particle to one binary code: it does **not** map each trit individually to a fixed number of bits.

### Decoding

Read `1001000110` as unsigned binary → **582**. Subtract the offset of **364** → **218**. Express 218 in balanced base three with exactly six trits → **[+1, 0, −1, 0, +1, −1]**. The conversion is reversible.

Because ten bits can represent 1024 values but the particle has only 729 valid states, codes **729–1023** are invalid in this example scheme.

## Physical packing choices

A single particle needs **at least 10 bits** since $2^9=512<729\le1024=2^{10}$.

- **Aligned container example:** store the ten-bit code in a 16-bit word, with six high bits zero. Simpler indexing and updates; 6 bits unused per particle.
- **Dense packing example:** concatenate ten-bit codes. More compact, but particle boundaries can cross byte boundaries and require masks, shifts, or read-modify-write.
- **Other representations:** possible, but must preserve all 729 values unambiguously.

These are **illustrations**, not an adopted ABI or wire format. To make the format operational, specify bit order, endianness, packing order, invalid-code behavior, atomic update rules, and conversion at binary transport boundaries. Variable-width particles require explicit width negotiation or conversion to a canonical interchange width.

## Relationship to the particle definition

See [Ternary Particle Model](ternary-particles.md) for the *unit hierarchy, addressability, and storage model*. This document explains *balanced numerical meaning and one concrete binary encoding*.

**Invariant:** one default particle = **2 triplets = 6 trits = 729 states**, independent of the chosen value interpretation or physical packing.
