(function (global) {
    const PAGE_SIZE = 4096n;
    const MEMORY_BASE = 0x100000n;
    const UINT64_MAX = (1n << 64n) - 1n;

    function toBigInt(value) {
        if (typeof value === 'bigint') return value;
        if (typeof value === 'number') return BigInt(Math.trunc(value));
        const text = String(value).trim();
        return BigInt(text || '0');
    }

    class MemoryModel {
        constructor({ pageCount = 12, hhdmAvailable = true, hhdmOffset = '0xffff800000000000' } = {}) {
            this.hhdmAvailable = hhdmAvailable;
            this.hhdmOffset = toBigInt(hhdmOffset);
            this.configure(pageCount);
        }

        get allocatedPageCount() {
            return this.pages.filter(page => page.allocated).length;
        }

        get allocatedBytes() {
            return this.allocations.reduce((total, allocation) => total + allocation.rounded, 0n);
        }

        configure(pageCount) {
            this.pageCount = Math.max(1, Math.min(256, Number(pageCount) || 1));
            this.pages = Array.from({ length: this.pageCount }, (_, index) => ({
                index,
                base: MEMORY_BASE + BigInt(index) * PAGE_SIZE,
                allocated: false,
                allocationLabel: 'available',
                bytes: new Uint8Array(Number(PAGE_SIZE)),
            }));
            this.allocations = [];
            this.nextAddress = 0n;
        }

        reset() {
            this.configure(this.pageCount);
        }

        allocatePhysicalBytes(size) {
            const requested = toBigInt(size);
            if (requested <= 0n) return 0n;
            const pagesNeeded = (requested + PAGE_SIZE - 1n) / PAGE_SIZE;
            const start = this.pages.findIndex((page, index) => {
                return index + Number(pagesNeeded) <= this.pages.length && this.pages.slice(index, index + Number(pagesNeeded)).every(item => !item.allocated);
            });
            if (start < 0) return 0n;
            const base = this.pages[start].base;
            const allocation = { base, requested, pages: Number(pagesNeeded), rounded: pagesNeeded * PAGE_SIZE };
            for (let index = start; index < start + allocation.pages; index += 1) {
                this.pages[index].allocated = true;
                this.pages[index].allocationLabel = `${requested} bytes requested`;
            }
            this.allocations.push(allocation);
            this.nextAddress = base + allocation.rounded;
            return base;
        }

        physicalToVirtual(physical, offset = this.hhdmOffset) {
            const address = toBigInt(physical);
            const hhdm = toBigInt(offset);
            if (address === 0n || hhdm > UINT64_MAX - address) return 0n;
            return address + hhdm;
        }

        physicalBytes(physical) {
            if (!this.hhdmAvailable || this.physicalToVirtual(physical) === 0n) return null;
            const allocation = this.allocations.find(item => item.base === toBigInt(physical));
            if (!allocation) return null;
            return { base: allocation.base, length: allocation.rounded };
        }

        locate(address, size = 1) {
            const start = toBigInt(address);
            const length = toBigInt(size);
            const allocation = this.allocations.find(item => start >= item.base && start + length <= item.base + item.rounded);
            if (!allocation) throw new Error(`Address ${formatAddress(start)} is not inside an allocation`);
            return { allocation, offset: start - allocation.base };
        }

        bytesAt(address, size) {
            const { offset } = this.locate(address, size);
            const output = new Uint8Array(Number(size));
            for (let index = 0; index < output.length; index += 1) output[index] = this.byteAt(offset + toBigInt(address) - toBigInt(address) + BigInt(index), address);
            return output;
        }

        byteAt(offset, address) {
            const { allocation } = this.locate(toBigInt(address), 1);
            const page = this.pages.find(item => toBigInt(address) >= item.base && toBigInt(address) < item.base + PAGE_SIZE);
            return page.bytes[Number(toBigInt(address) - page.base)];
        }

        writeByte(address, value) {
            const { allocation } = this.locate(address, 1);
            const page = this.pages.find(item => toBigInt(address) >= item.base && toBigInt(address) < item.base + PAGE_SIZE);
            page.bytes[Number(toBigInt(address) - page.base)] = Number(value) & 0xff;
        }

        memset(address, value, size) {
            const length = toBigInt(size);
            this.locate(address, length);
            for (let index = 0n; index < length; index += 1n) this.writeByte(toBigInt(address) + index, value);
            return toBigInt(address);
        }

        memcpy(destination, source, size) {
            const length = toBigInt(size);
            const values = Array.from({ length: Number(length) }, (_, index) => this.byteAt(0n, toBigInt(source) + BigInt(index)));
            values.forEach((value, index) => this.writeByte(toBigInt(destination) + BigInt(index), value));
            return toBigInt(destination);
        }

        memmove(destination, source, size) {
            const length = toBigInt(size);
            const values = Array.from({ length: Number(length) }, (_, index) => this.byteAt(0n, toBigInt(source) + BigInt(index)));
            values.forEach((value, index) => this.writeByte(toBigInt(destination) + BigInt(index), value));
            return toBigInt(destination);
        }

        memcmp(first, second, size) {
            const length = toBigInt(size);
            for (let index = 0n; index < length; index += 1n) {
                const left = this.byteAt(0n, toBigInt(first) + index);
                const right = this.byteAt(0n, toBigInt(second) + index);
                if (left !== right) return left < right ? -1 : 1;
            }
            return 0;
        }
    }

    function formatAddress(value) {
        return `0x${toBigInt(value).toString(16).padStart(8, '0')}`;
    }

    global.VOLMemory = { MemoryModel, PAGE_SIZE, formatAddress, toBigInt };
}(window));
