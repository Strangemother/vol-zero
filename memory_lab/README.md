# VOL Memory Lab

A standalone browser proxy for the VOL physical allocator and pure memory operations.

## Run

From this directory:

```sh
python3 -m http.server 8080
```

Open <http://127.0.0.1:8080/>. The page uses the Vue 3 browser build from unpkg and Google Fonts (`SN Pro` and `Staatliches`).

The visualizer is intentionally independent from the kernel build. It models page-rounded allocation, HHDM address translation, bounded byte access, and `memset`, `memcpy`, `memmove`, and `memcmp` in `src/model.js`.

## Python simulator

`memory.py` is a standalone physical-memory simulator for experimenting with
the same addressable API before moving code into Nim:

```python
from memory import *

reset()
address = allocate_physical_bytes(1)
write_byte(address, 0x2a)
assert read_byte(address) == 0x2a

memset(address + 1, 0, 3)
assert read(address, 4) == bytes([0x2a, 0, 0, 0])
```

Run an experiment from this directory so `memory.py` is importable:

```sh
cd memory_lab
python3 experiment.py
```

Allocations are rounded up to `PAGE_SIZE` (4096 bytes), begin at physical
address `0x100000`, and return `0` when the request is non-positive. Accessing
unallocated memory or crossing an allocation boundary raises `ValueError`.
`physical_bytes(address)` returns a writable `memoryview` for the allocation.
Memory is unlimited by default; opt into a fixed arena when needed:

```python
set_memory_limit(1024 * 1024)  # 1 MiB from 0x100000
assert allocate_physical_bytes(1024 * 1024) == 0x100000
assert allocate_physical_bytes(1) == 0
set_memory_limit(None)  # unlimited again
```

Changing the limit resets the arena.

Small runnable examples sit beside `memory.py`:

```sh
python3 example_allocate.py
python3 example_addressing.py
python3 example_limit.py
python3 example_kernel_parity.py
```

The parity example demonstrates usable-region gaps, reset-preserved bytes,
overlapping `memmove`, and HHDM availability. `configure_memory` accepts
Limine-style `(base, size)` usable regions. `set_hhdm` controls the simulated
HHDM response, while `current_state` exposes the allocation cursor.

## Scenarios

Scenario definitions live independently in `src/scenarios.js`. Each scenario
inherits a small memory facade with familiar calls. The destination defaults to
the most recent allocation, so a focused scenario can read naturally:

```javascript
class ScenarioOne extends Scenario {
	name() { return 'Fill an allocation'; }
	desc() { return 'Allocate two pages and fill the first 48 bytes.'; }
	run(model = this.model) {
		model.allocate(8192);
		model.memset(0x2a, 48);
	}
}
```

The picker includes allocation rounding, copy and compare, overlapping moves,
byte writes, and HHDM address examples. Add a scenario to the `scenarios` list
in `src/scenarios.js` to make it available in the UI.
