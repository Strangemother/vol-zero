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
