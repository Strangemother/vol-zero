# Literal ASM Transpiler

`lat` is a small Python package for recording assembly-like operations and
rendering them as ordered text.

## Development setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest
```

## Example

```python
from lat import ASM, Reader, Registers

asm = ASM()
reg = Registers()
asm.mov(reg.eax, 1)
asm.ret()

print(Reader(asm).flat_resolve())
```

## Instruction reference

Regenerate the de-duplicated instruction list from the Felix Cloutier and C9x
indexes with:

```bash
cd asm_tool
python tools/build_instruction_reference.py
```

The command writes `docs/instructions.md`. Use `--output` to write another
Markdown file, or `--felix-url` and `--c9x-url` to point at saved/local index
pages when working offline.


- https://ref.x86asm.net/coder64.html
- https://cs.brown.edu/courses/cs033/docs/guides/x64_cheatsheet.pdf
- https://www.felixcloutier.com/x86/
- https://www.cs.virginia.edu/~evans/cs216/guides/x86.html
- https://intel.github.io/SDM/sdm.html
- https://c9x.me/x86/

- https://tonybaloney.github.io/posts/extending-python-with-assembly.html