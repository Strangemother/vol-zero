(function (global) {
    class Scenario {
        constructor(runtime) {
            this.runtime = runtime;
            this.model = this.createModel(runtime);
        }

        name() { return this.constructor.name; }
        desc() { return 'No description provided.'; }
        run() { throw new Error(`${this.name()} must implement run(model)`); }

        createModel(runtime) {
            let lastAllocation = 0n;
            const address = value => value === undefined ? lastAllocation : runtime.toBigInt(value);
            const model = {
                allocate: size => {
                    lastAllocation = runtime.allocate(size);
                    return lastAllocation;
                },
                memset: (value, size, destination) => runtime.memset(address(destination), value, size),
                memcpy: (source, size, destination) => runtime.memcpy(address(destination), source, size),
                memmove: (source, size, destination) => runtime.memmove(address(destination), source, size),
                memcmp: (source, size, destination) => runtime.memcmp(address(destination), source, size),
                writeByte: (value, offset = 0, destination) => runtime.writeByte(address(destination) + runtime.toBigInt(offset), value),
                hhdmAddress: destination => runtime.model.physicalToVirtual(address(destination)),
            };
            Object.defineProperty(model, 'lastAllocation', { get: () => lastAllocation });
            return model;
        }

        reset() { return this.runtime.reset(); }
        allocate(size) { return this.model.allocate(size); }
        memset(value, size, destination) { return this.model.memset(value, size, destination); }
        memcpy(source, size, destination) { return this.model.memcpy(source, size, destination); }
        memmove(source, size, destination) { return this.model.memmove(source, size, destination); }
        memcmp(source, size, destination) { return this.model.memcmp(source, size, destination); }
        writeByte(value, offset = 0, destination) { return this.model.writeByte(value, offset, destination); }
        hhdmAddress(destination) { return this.model.hhdmAddress(destination); }
    }

    class ScenarioOne extends Scenario {
        name() { return 'Fill an allocation'; }
        desc() { return 'Allocate two pages and fill the first 48 bytes with 0x2a.'; }
        run(model = this.model) {
            model.allocate(8192);
            model.memset(0x2a, 48);
        }
    }

    class PageRoundingScenario extends Scenario {
        name() { return 'Page rounding'; }
        desc() { return 'Compare allocations of 1 byte, one page, and one page plus one byte.'; }
        run(model = this.model) {
            model.allocate(1);
            model.allocate(4096);
            model.allocate(4097);
        }
    }

    class CopyAndCompareScenario extends Scenario {
        name() { return 'Copy and compare'; }
        desc() { return 'Fill a source region, copy it, then compare both regions.'; }
        run(model = this.model) {
            const source = model.allocate(4096);
            const destination = model.allocate(4096);
            model.memset(0x7f, 16, source);
            model.memcpy(source, 16, destination);
            model.memcmp(source, 16, destination);
        }
    }

    class OverlappingMoveScenario extends Scenario {
        name() { return 'Overlapping move'; }
        desc() { return 'Write a short pattern and move it one byte forward.'; }
        run(model = this.model) {
            const allocation = model.allocate(4096);
            model.memset(1, 8, allocation);
            model.memmove(allocation, 7, allocation + 1n);
        }
    }

    class ByteWritesScenario extends Scenario {
        name() { return 'Byte writes'; }
        desc() { return 'Allocate a page and write values at selected byte offsets.'; }
        run(model = this.model) {
            model.allocate(4096);
            model.writeByte(0xff, 0);
            model.writeByte(0x80, 1);
            model.writeByte(0x2a, 2);
        }
    }

    class HhdmViewScenario extends Scenario {
        name() { return 'HHDM address view'; }
        desc() { return 'Allocate a page and calculate its higher-half virtual address.'; }
        run(model = this.model) {
            model.allocate(4096);
            model.hhdmAddress();
        }
    }

    function createScenarios(runtime) {
        return [
            new ScenarioOne(runtime),
            new PageRoundingScenario(runtime),
            new CopyAndCompareScenario(runtime),
            new OverlappingMoveScenario(runtime),
            new ByteWritesScenario(runtime),
            new HhdmViewScenario(runtime),
        ];
    }

    global.VOLScenarios = { Scenario, ScenarioOne, createScenarios };
}(window));
