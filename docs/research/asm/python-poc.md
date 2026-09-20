# Python proof of concept

The PoC should answer one question first: can a small typed operation model
record instructions and render valid, deterministic assembly? It should not
start with decorators, operator overloading, parsing, or a CPU emulator.

## Setup

Create an isolated environment and install only the test runner if desired:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install pytest
```

A minimal PoC can live in `poc/asm.py` with tests in `poc/test_asm.py`. Keep it
independent of the kernel build until the model is useful.

## Smallest useful model

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Register:
    name: str
    width: int


@dataclass(frozen=True)
class Immediate:
    value: int


@dataclass(frozen=True)
class Instruction:
    opcode: str
    destination: object
    source: object


class Program:
    def __init__(self):
        self.operations = []

    def mov(self, destination, source):
        self.operations.append(Instruction("mov", destination, source))

    def add(self, destination, source):
        self.operations.append(Instruction("add", destination, source))

    def render(self):
        return "\n".join(
            f"{operation.opcode} "
            f"{format_operand(operation.destination)}, "
            f"{format_operand(operation.source)}"
            for operation in self.operations
        )


def format_operand(operand):
    if isinstance(operand, Register):
        return operand.name
    if isinstance(operand, Immediate):
        return str(operand.value)
    raise TypeError(f"unsupported operand: {operand!r}")


rax = Register("rax", 64)
rcx = Register("rcx", 64)
```

The first test should be:

```python
def test_arithmetic_renders_in_order():
    program = Program()
    program.mov(rax, Immediate(5))
    program.mov(rcx, Immediate(12))
    program.add(rax, rcx)

    assert program.render() == "\n".join([
        "mov rax, 5",
        "mov rcx, 12",
        "add rax, rcx",
    ])
```

## Add validation second

Once recording works, validate instruction signatures before rendering:

```python
def validate_mov(destination, source):
    if not isinstance(destination, Register):
        raise TypeError("mov destination must be a register in the first PoC")
    if isinstance(source, Register) and source.width != destination.width:
        raise ValueError("register widths must match")
```

The real compiler should replace these exceptions with structured diagnostics,
but early failures are enough to test the concept.

## Add a target renderer third

Keep the operation unchanged and add a renderer function:

```python
def render_att(operation):
    destination = format_operand(operation.destination)
    source = format_operand(operation.source)
    if isinstance(operation.source, Immediate):
        source = "$" + source
    return f"{operation.opcode} {source}, %{destination}"
```

The exact mnemonic suffix rules can be added with the target profile. The
important experiment is that Intel and AT&T renderers consume the same
operation object.

## Optional abstract state

After the renderer is stable, add a separate state tracker:

```python
class AbstractState:
    def __init__(self):
        self.registers = {}

    def apply(self, operation):
        if operation.opcode == "mov" and isinstance(operation.destination, Register):
            self.registers[operation.destination.name] = operation.source
```

This state is useful for diagnostics and tests. It is not a promise that the
runtime register contains a Python value, and it should not be needed to render
ordinary instructions.

## PoC exit criteria

The PoC is successful when it can:

- record `mov` and `add` in order;
- render Intel syntax deterministically;
- reject at least one invalid operand combination;
- render the same operations with a second syntax function;
- expose enough operation data for a test to inspect it;
- keep Python build-time control flow separate from runtime assembly flow.

Only then should the project explore labels, sections, memory operands, calls,
assets, decorators, operator sugar, reverse parsing, or a Unicorn-backed
simulator.
