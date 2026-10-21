# Ternary Particle Model

> **Status: proposed logical architecture.** This document records an agreed design direction, not an implemented kernel ABI, memory allocator, filesystem, or transport protocol. Read alongside [Memory Definitions](definitions.md), which currently describes the earlier binary-based particle model.

## Why ternary?

VOL Zero is intended to expose a **ternary logical model** above conventional **binary hardware**. Hardware bits still encode physical data; VOL's logical values are trits. This separation makes the conceptual model independent of the underlying machine's byte width.

## Units

| Unit | Definition | Possible values |
| --- | --- | ---: |
| Bit | Hardware binary digit: 0 or 1 | 2 |
| Trit | Logical ternary digit: 0, 1, or 2 | 3 |
| Triplet | Three trits | 3³ = 27 |
| Particle (default) | Two triplets = six trits | 3⁶ = 729 |

A **trit** is the smallest logical *value*. A **particle** is the intended smallest independently *addressable* VOL unit. A **triplet** is a grouping, not a separate addressable unit.

```text
One trit:                  [ t₀ ]            ∈ {0, 1, 2}

One triplet:               [ t₀ ][ t₁ ][ t₂ ]
                              3 trits → 27 states

One particle:              [ t₀ ][ t₁ ][ t₂ ] [ t₃ ][ t₄ ][ t₅ ]
                           └── triplet A ───┘ └── triplet B ───┘
                             3 trits, 27 states each
                             6 trits, 729 states total
```

## Mathematical definition

For a sequence of \(n\) trits with \(t_i \in \{0,1,2\}\), its unsigned base-three interpretation is

\[
V(t_0,\ldots,t_{n-1})=\sum_{i=0}^{n-1}t_i3^{n-1-i},
\qquad 0\le V<3^n.
\]

A triplet has

\[
\underbrace{3\times3\times3}_{\text{three trits}}=3^3=27
\]

possible states. Two independent triplets make one default particle:

\[
\underbrace{27\times27}_{\text{two triplets}}=3^6=729.
\]

Consequently, a default particle's unsigned value ranges from **0 through 728**, inclusive. The representation of signed values is not yet specified.

## Why six trits?

Six trits form **two symmetric three-trit triplets**. This is an intentional grouping choice, not a requirement of ternary arithmetic; three triplets (nine trits) would also be mathematically valid, but are **not** the default selected here.

An existing ternary term, *tryte*, is sometimes used for six trits. The word **particle** in VOL conveys the *addressable unit* abstraction rather than merely a ternary numeral grouping.

## Addressing, files, and communication

The target design is to use particles as the fundamental addressable units in VOL's memory and file-storage abstractions. Operations can interpret or manipulate constituent trits without individually addressing them as standalone allocation units.

- **Empty files** may have logical length zero and allocate no data particles, while still having metadata.
- **Non-empty files** can occupy at least one particle; the file's logical information length and allocated storage length must remain separate.
- **Internal VOL communication** should specify ternary logical data. Binary hardware, networks, and byte-oriented devices will need explicit transport encodings.

The claim that a short text file occupies one particle concerns its **minimum storage allocation**, not a universal encoding for characters, file metadata, or file headers. Those formats require separate specifications.

## Binary encoding and implementation questions

Since \(2^9=512<729\le1024=2^{10}\), storing all possible six-trit values in one fixed-width binary container requires **at least ten physical bits**. One naive ten-bit encoding leaves **295 unused bit patterns**. A practical implementation may choose larger aligned containers or different packing strategies.

Before implementation, VOL must specify:

1. Exact particle packing, trit order, and bit-level serialization.
2. Invalid encodings and conversion into and out of conventional bytes.
3. Addressing granularity and how it relates to actual host-page allocation.
4. Logical file lengths, empty files, metadata, and partially filled particles.
5. Whether subsystem-specific particle widths are allowed and how they are declared and interoperated.
6. Mapping of current binary-oriented **clusters, parcels, volumes, and extents** from [Memory Definitions](definitions.md) to this new model.

**Design invariant for the default architecture:** **one particle = two triplets = six trits = 729 states**.
