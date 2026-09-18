# Root Fundamentals

Some core components for the root to function. A Base system would require these before yielding a functional VOL

+ Graph machine
  A representation of a graph for the entire system to aquire.
+ Address resolver
  A Utility to request incoming graph keys, yielding _paths_ for "apps".
+ virtual memory
  Conigious memory allocation, with addressing

For implementation of these core utils:

+ A Pointer class
  requires the peristent and virtual memory

+ A Stepper class
  Requires the graph machine for subsets and an address resolver, to move a pointer.
+ A Stepper machine
  Requires the graph machine a the ability to generate new contexts for cells.

---

Beneath these components the root VOL runtime hosts features to _run_ the base graph, pointer, and stepper. The root may utilise these components but generally will live isolated as a turing complete BIOD (basic input output device).

Similar to a standard monotlith, the _kernel_ runs above a _BIOS_ to execute the root runtime procedures. In our case the BIOD hosts a monolith to generate subsets of the base sytem, concatenating additional _layers_ for a resolved solution.

The result acts like a complete system build has been built for a specific task. The monolith may dispatch new kernels to other BIOD's, convert them to a _functioning utility for the target device_ by recompiling the kernel with additional graph features. This occures before the pointer actuates the SES


## Core apps

+ Import lib
  A system importer based upon _synthetic_ modelling
+ Eval lib
  Execute source for live system changes; pointer collections from a graph
+ Stepping lib
  The graph key stepping functionality, utilised by the stepper machine
