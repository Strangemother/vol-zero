# Ternary Particle Model

> **Status: proposed logical architecture.** This document records an agreed design direction, not an implemented kernel ABI, memory allocator, filesystem, or transport protocol. Read alongside [Memory Definitions](definitions.md), which currently describes the earlier binary-based particle model.

## Why ternary?

VOL Zero is intended to expose a **ternary logical model** above conventional **binary hardware**. Hardware bits still encode physical data; VOL's logical values are trits. This separation makes the conceptual model independent of the underlying machine's byte width.

## Units

| Unit | Definition | Possible values |
| --- | --- | ---: |
| Bit | Hardware binary digit: 0 or 1 | 2 |
| Trit | Balanced logical ternary digit: −1, 0, or +1 | 3 |
| Triplet | Three trits | 3³ = 27 |
| Particle (default) | Two triplets = six trits | 3⁶ = 729 |

A **trit** is the smallest logical *value*. A **particle** is the intended smallest independently *addressable* VOL unit. A **triplet** is a grouping, not a separate addressable unit.

```text
One trit:                  [ t₀ ]            ∈ {−1, 0, +1}

One triplet:               [ t₀ ][ t₁ ][ t₂ ]
                              3 trits → 27 states

One particle:              [ t₀ ][ t₁ ][ t₂ ] [ t₃ ][ t₄ ][ t₅ ]
                           └── triplet A ───┘ └── triplet B ───┘
                             3 trits, 27 states each
                             6 trits, 729 states total
```

## Mathematical definition

For a sequence of $n$ **balanced** trits with $t_i \in \{-1,0,+1\}$, its signed base-three interpretation is

```math
V(t_0,\ldots,t_{n-1})=\sum_{i=0}^{n-1}t_i3^{n-1-i},
\qquad -\frac{3^n-1}{2}\le V\le\frac{3^n-1}{2}.
```

A triplet has

```math
\underbrace{3\times3\times3}_{\text{three trits}}=3^3=27
```

possible states. Two independent triplets make one default particle:

```math
\underbrace{27\times27}_{\text{two triplets}}=3^6=729.
```

Consequently, a default balanced particle represents integer values from **−364 through +364**, inclusive. Its 729 states may be mapped bijectively to unsigned codes **0 through 728** for physical storage. This mapping is an encoding choice, not a reinterpretation of the particle as inherently unsigned.

## Why six trits?

Six trits form **two symmetric three-trit triplets**. This is an intentional grouping choice, not a requirement of ternary arithmetic; three triplets (nine trits) would also be mathematically valid, but are **not** the default selected here.

An existing ternary term, *tryte*, is sometimes used for six trits. The word **particle** in VOL conveys an *addressable unit of quantity*, analogous to a byte: it does **not** inherently describe a data type, instruction, reference, control flag, or semantic meaning. Any interpretation belongs to a separate schema or context.

## Addressing, files, and communication

The target design is to use particles as the fundamental addressable units in VOL's memory and file-storage abstractions. Operations can interpret or manipulate constituent trits without individually addressing them as standalone allocation units.

- **Empty files** may have logical length zero and allocate no data particles, while still having metadata.
- **Non-empty files** can occupy at least one particle; the file's logical information length and allocated storage length must remain separate.
- **Internal VOL communication** should specify ternary logical data. Binary hardware, networks, and byte-oriented devices will need explicit transport encodings.

The claim that a short text file occupies one particle concerns its **minimum storage allocation**, not a universal encoding for characters, file metadata, or file headers. Those formats require separate specifications.

## Worked example: balanced ternary on binary hardware

Balanced ternary is the **preferred VOL logical representation**. Each trit is one of $-1$, $0$, or $+1$. The following *illustrative mapping* is reversible and preserves all 729 states; it does not mandate the final physical layout.

Take the six-trit particle

```text
     triplet A       triplet B
    [ +1,  0, −1 ] [ 0, +1, −1 ]
       1   0  -1     0   1  -1
```

With the leftmost trit most significant, its signed numeric value is:

```math
V = 1\cdot3^5 + 0\cdot3^4 - 1\cdot3^3
  + 0\cdot3^2 + 1\cdot3^1 - 1\cdot3^0
  = 243-27+3-1=218.
```

The maximum magnitude is $(3^6-1)/2=364$. Offset the signed value to a nonnegative storage code:

```math
C=V+364=218+364=582.
```

Then convert **582** to a fixed-width ten-bit unsigned binary representation:

```text
balanced trits:     +1   0  −1   0  +1  −1
signed value V:     +218
biased code C:       582
10-bit binary:        1001000110
```

Decoding reverses this exactly: binary `1001000110` → 582 → subtract 364 → +218 → balanced six-trit vector `[+1,0,−1,0,+1,−1]`. This is a **numerical encoding** of the whole particle, not a one-to-one correspondence between individual trits and binary bits.

For an arbitrary particle, **encode** by evaluating the balanced-base-three sum, adding 364, and writing a ten-bit unsigned code. **Decode** by reading the code, rejecting values 729 through 1023 as invalid, subtracting 364, and recovering the six balanced digits. Both the trit ordering and binary bit ordering must be fixed in the final format.

As a simple implementation option, place each ten-bit code inside a **16-bit physical container** and leave the upper six bits zero. This is easier to index but uses 16 physical bits per particle. Dense ten-bit packing saves space but can cause particles to straddle byte boundaries; neither layout is adopted as a final ABI here.

## Binary encoding and implementation questions

Since $2^9=512<729\le1024=2^{10}$, storing all possible six-trit values in one fixed-width binary container requires **at least ten physical bits**. One naive ten-bit encoding leaves **295 unused bit patterns**. A practical implementation may choose larger aligned containers or different packing strategies.

Before implementation, VOL must specify:

1. Exact particle packing, trit order, and bit-level serialization (the mapping above is a worked example, not yet a mandated wire format).
2. Invalid encodings and conversion into and out of conventional bytes.
3. Addressing granularity and how it relates to actual host-page allocation.
4. Logical file lengths, empty files, metadata, and partially filled particles.
5. Whether subsystem-specific particle widths are allowed and how they are declared and interoperated.
6. Mapping of current binary-oriented **clusters, parcels, volumes, and extents** from [Memory Definitions](definitions.md) to this new model.

**Design invariant for the default architecture:** **one particle = two triplets = six trits = 729 states**.
