# LAT examples

These scripts are small review examples based on the current test suite. Run
from `asm_tool` after installing the package with `pip install -e .`.

## Examples

- `01_dynamic_zero_args.py`: `ASM` creates an instruction for an attribute that
  was not declared ahead of time.
- `02_single_arg.py`: instructions with one operand.
- `03_multi_arg.py`: instructions with two operands and preserved order.
- `04_raw_and_registers.py`: raw assembly and lazy, case-insensitive registers.

`asm.hlt()` works because `ASM.__getattr__` treats an unknown attribute as a
mnemonic. This is dynamic instruction lookup, not a missing `ASM` object. The
`raw` mnemonic is different: it is explicitly installed with
`install_instruction(RawInstruction)` so its text bypasses normal formatting.
