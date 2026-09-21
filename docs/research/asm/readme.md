 # ASM compiler research

 This directory is the design notebook for a Python-to-assembly compiler. The
 original notes remain in the small topic files and in `combined.md`; the
 documents below are the organized working view.

 ## Start here

 - [Concepts](concepts.md): the proposed architecture and vocabulary.
 - [Instruction signatures](instruction-signatures.md): operand shapes,
	 target profiles, and WebAssembly stack effects.
 - [`mov` design reference](mov.md): the consolidated operation model,
	 operand forms, API ideas, validation, and two-parameter generalization.
 - [Registers](registers.md): x86 register names, aliases, widths, and
	 target-specific availability.
 - [Examples](examples.md): small source-to-assembly examples, from literal
	 instructions to register sugar.
 - [Demos](demos.md): end-to-end demonstrations that can become acceptance
	 tests for the compiler.
 - [Python PoC](python-poc.md): a deliberately small implementation path for
	 testing the intermediate representation, register model, and renderer.
 - [Roadmap](roadmap.md): decisions, open questions, and an incremental build
	 order.

 ## Historical notes

 The files `asm.md`, `reg.md`, and `add.md` are the primary source notes. The
 remaining material in `combined.md` contains earlier experiments covering
 calls, sections, assets, jumps, templates, flags, and boot examples. Keep
 those files as an archive: new design decisions should be copied into the
 organized documents with a source note, rather than silently rewriting the
 history.

 ## References

 - https://www.felixcloutier.com/x86/
 - https://github.com/unicorn-engine/unicorn
 - https://azeria-labs.com/writing-arm-assembly-part-1/
 - https://wiki.osdev.org/Creating_a_64-bit_kernel
 - https://prosepoetrycode.potterpcs.net/2023/01/a-barebones-kernel-in-nim/
 - https://gitlab.com/momikey/nim-limine-barebones/-/tree/master?ref_type=heads
 - https://0xc0ffee.netlify.app/osdev/22-elf-loader-p2
 - https://github.com/dom96/nimkernel
 - https://tonybaloney.github.io/posts/extending-python-with-assembly.html



