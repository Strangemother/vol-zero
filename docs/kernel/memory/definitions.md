# Memory Definitions

VOL redefines computing primitives to align with the new concepts applied in this Operating System. In this first section, definitions align with classic computing but with modifications to fit the VOL architecture.

## Binary Digits

Binary digits, or `bits`, are the most fundamental unit of information in computing. We don't redefine their basic concept in VOL; a `bit` still represents a binary value of either 0 or 1. 

## Particle

Aligning with standard computing terminology, a `particle` can be considered _a byte_; being composed of 8 `bits`. In VOL, we adopt the term `particle` HOWEVER a particle is not strictly limited to 8 `bits` and may vary depending on the architecture and context within the VOL system.

Therefore 1 `particle` typically represents 8 `bits`, but will grow depending on the base computing unit value (e.g., 16 `bits` or 32 `bits`) in the VOL system.

## Cluster

A `cluster` in VOL represents a collection of `particles`. While in traditional computing, a cluster might refer to a group of bytes or memory blocks, in VOL, it is a higher-level abstraction that groups multiple `particles` together. 

A single `cluster` typically contains 2x `particles` (though this can vary)  and counting of multiple clusters is defines a `X cluster`. 

In the core definition, a 2x Cluster would be a `Duo Cluster` continuing through `Tri`, `Quad`, `Quint`, and so on. Though through a doubling sequence, `Duo`, `Quad`, `Octo`, `Hexadeca`, and so forth would be used to represent X clusters.

---

Where in a standard 8 bit particle, is a 1x `cluster`, a `Quad Cluster` is 4x `particles` or 32 `bits`.

In a 32 `bit` particle, a 1x `cluster` would still be 2x `particles`, but the actual bit count would be 64 `bits`. Consequently, a `Quad Cluster` in this context would be 4x `particles` or 128 `bits`.

## 1D Parcel 

A Parcel is single contiguous block of particles.
In a standard setup this is 256 clusters or 32 `particles` in a standard 8 `bit` particle setup. This changes depending on the particle size and the architecture of the VOL system.

Allocation may occur at the Parcel level. Once allocated the clusters and particles within the Parcel are accessible.

## Volume

A `Volume` is composed of multiple (non contigious) `Parcels`. A volume can be any size within the possible extent. It may be static or dynamic, and its allocation can span across different memory regions as needed.

By default, a `Volume` can be at minimum a single `Parcel` but has an undefined size and can grow dynamically as more memory is allocated to it.

## Extent

An `Extent` defines the total possible memory supplied to the current VOL runtime. It is the encompassing boundary within which all `Volumes`, `Parcels`, `Clusters`, and `Particles` must reside. 

It doesn't define the maximum amount of memory VOL can actually allocate at any given time. for example if the system has 8GB of physical memory, the `Extent` will define a smaller value, based upon live resources. 

The maximum size of an `Extent` is the total addressable memory space of the system. This may _spill_ to persistent disk memory - however currently this is not implemented.



