# VOL Memory Lab

A standalone browser proxy for the VOL physical allocator and pure memory operations.

## Run

From this directory:

```sh
python3 -m http.server 8080
```

Open <http://127.0.0.1:8080/>. The page uses the Vue 3 browser build from unpkg and Google Fonts (`SN Pro` and `Staatliches`).

The visualizer is intentionally independent from the kernel build. It models page-rounded allocation, HHDM address translation, bounded byte access, and `memset`, `memcpy`, `memmove`, and `memcmp` in `src/model.js`.

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
