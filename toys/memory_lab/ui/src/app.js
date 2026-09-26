const { createApp } = Vue;
const { MemoryModel, PAGE_SIZE, formatAddress, toBigInt } = window.VOLMemory;
const { createScenarios } = window.VOLScenarios;

createApp({
    data() {
        const model = new MemoryModel();
        return {
            model,
            pageCount: model.pageCount,
            hhdmOffsetInput: formatAddress(model.hhdmOffset),
            allocationSize: 4096,
            operation: 'memset',
            operationAddress: '0x00000000',
            operationSource: '0x00000000',
            operationSize: 32,
            operationValue: 0x2a,
            selectedPage: null,
            changedBytes: new Set(),
            log: [],
            nextLogId: 1,
            recording: false,
            replaying: false,
            recordedActions: [],
            showFunctionsOnly: false,
            nextActionId: 1,
            editingByte: null,
            byteEditValue: '',
            scenarios: [],
            selectedScenarioIndex: 0,
        };
    },
    created() {
        this.scenarios = createScenarios(this.scenarioRuntime());
    },
    computed: {
        allocatedPageCount() { return this.model.pages.filter(page => page.allocated).length; },
        allocatedBytes() { return this.model.allocations.reduce((sum, item) => sum + item.rounded, 0n); },
        selectedScenario() { return this.scenarios[this.selectedScenarioIndex] || this.scenarios[0]; },
        visibleEvents() {
            if (!this.showFunctionsOnly) return this.log;
            return this.recordedActions.map(action => ({
                id: action.id,
                actionId: action.id,
                kind: 'success',
                call: action.call,
            }));
        },
    },
    methods: {
        rebuild() {
            this.model.hhdmOffset = toBigInt(this.hhdmOffsetInput);
            this.model.configure(this.pageCount);
            this.selectedPage = null;
            this.changedBytes = new Set();
            this.addLog('system', 'configure_memory_map', `${this.pageCount} usable pages available`, { pageCount: this.pageCount, hhdmOffset: this.hhdmOffsetInput, hhdmAvailable: this.model.hhdmAvailable }, 'map rebuilt');
        },
        reset() {
            this.model.reset();
            this.selectedPage = null;
            this.changedBytes = new Set();
            this.addLog('system', 'limine_allocator_reset', 'Allocation cursor returned to the first page', {}, 'arena reset');
        },
        allocate() {
            const address = this.model.allocatePhysicalBytes(this.allocationSize);
            if (address === 0n) {
                this.addLog('error', 'allocate_physical_bytes', `${this.allocationSize} bytes could not fit in the usable map`, { size: this.allocationSize }, '0x00000000 (failure)');
                return;
            }
            this.operationAddress = formatAddress(address);
            this.selectPage(this.model.pages.find(page => page.base === address));
            this.addLog('success', 'allocate_physical_bytes', `${this.allocationSize} requested, ${this.roundedSize(this.allocationSize)} reserved`, { size: this.allocationSize }, formatAddress(address));
        },
        runOperation() {
            try {
                const address = toBigInt(this.operationAddress);
                const size = toBigInt(this.operationSize);
                if (this.operation === 'memset') this.model.memset(address, this.operationValue, size);
                if (this.operation === 'memcpy') this.model.memcpy(address, toBigInt(this.operationSource), size);
                if (this.operation === 'memmove') this.model.memmove(address, toBigInt(this.operationSource), size);
                const result = this.operation === 'memcmp' ? this.model.memcmp(address, toBigInt(this.operationSource), size) : 'destination returned';
                this.markChanged(address, size);
                const args = this.operation === 'memset'
                    ? { destination: formatAddress(address), value: this.operationValue, size: Number(size) }
                    : { destination: formatAddress(address), source: this.operationSource, size: Number(size) };
                this.addLog('success', this.operation, `${size} bytes at ${formatAddress(address)}`, args, String(result));
                this.refreshSelection();
            } catch (error) {
                this.addLog('error', this.operation, error.message, { destination: this.operationAddress, size: this.operationSize }, 'rejected');
            }
        },
        runScenario() {
            this.runSelectedScenario();
        },
        runSelectedScenario() {
            const scenario = this.selectedScenario;
            this.model.reset();
            this.selectedPage = null;
            this.changedBytes = new Set();
            this.log = [];
            this.editingByte = null;
            this.addLog('system', scenario.name(), scenario.desc(), {}, 'scenario started');
            try {
                scenario.run(scenario.model);
                this.refreshSelection();
                this.addLog('system', scenario.name(), scenario.desc(), {}, 'scenario complete');
            } catch (error) {
                this.addLog('error', scenario.name(), error.message, {}, 'scenario failed');
            }
        },
        scenarioRuntime() {
            return {
                model: this.model,
                toBigInt,
                reset: () => this.model.reset(),
                allocate: size => {
                    const address = this.model.allocatePhysicalBytes(size);
                    if (address === 0n) throw new Error(`allocate(${size}) failed: no usable pages remain`);
                    this.operationAddress = formatAddress(address);
                    this.selectPage(this.model.pages.find(page => page.base === address));
                    this.addLog('success', 'allocate', `reserved ${this.roundedSize(size)} at ${formatAddress(address)}`, { size: Number(size) }, formatAddress(address));
                    return address;
                },
                memset: (destination, value, size) => this.runScenarioOperation('memset', destination, size, { value }),
                memcpy: (destination, source, size) => this.runScenarioOperation('memcpy', destination, size, { source }),
                memmove: (destination, source, size) => this.runScenarioOperation('memmove', destination, size, { source }),
                memcmp: (destination, source, size) => this.runScenarioOperation('memcmp', destination, size, { source }),
                writeByte: (address, value) => {
                    const target = toBigInt(address);
                    this.model.writeByte(target, value);
                    this.markChanged(target, 1n);
                    this.addLog('success', 'write_byte', `${formatAddress(target)} changed to ${Number(value).toString(16).padStart(2, '0')}`, { address: formatAddress(target), value: Number(value) }, 'byte written');
                    return target;
                },
            };
        },
        runScenarioOperation(functionName, destination, size, extra = {}) {
            const target = toBigInt(destination);
            const length = toBigInt(size);
            const source = extra.source === undefined ? undefined : toBigInt(extra.source);
            let result;
            if (functionName === 'memset') result = this.model.memset(target, extra.value, length);
            if (functionName === 'memcpy') result = this.model.memcpy(target, source, length);
            if (functionName === 'memmove') result = this.model.memmove(target, source, length);
            if (functionName === 'memcmp') result = this.model.memcmp(target, source, length);
            this.markChanged(target, length);
            const args = functionName === 'memset'
                ? { destination: formatAddress(target), value: extra.value, size: Number(length) }
                : { destination: formatAddress(target), source: formatAddress(source), size: Number(length) };
            this.addLog('success', functionName, `${length} bytes at ${formatAddress(target)}`, args, String(result));
            return result;
        },
        selectPage(page) { this.selectedPage = page || null; },
        refreshSelection() {
            if (!this.selectedPage) return;
            const base = this.selectedPage.base;
            this.selectedPage = this.model.pages.find(page => page.base === base) || null;
        },
        setByte(index) {
            this.beginByteEdit(index);
        },
        byteAddress(index) {
            if (!this.selectedPage) return '';
            return formatAddress(this.selectedPage.base + BigInt(index));
        },
        async copyByteAddress(index) {
            const address = this.byteAddress(index);
            if (!address) return;
            if (navigator.clipboard) {
                await navigator.clipboard.writeText(address);
                return;
            }
            const field = document.createElement('textarea');
            field.value = address;
            document.body.appendChild(field);
            field.select();
            document.execCommand('copy');
            field.remove();
        },
        beginByteEdit(index) {
            if (!this.selectedPage || !this.selectedPage.allocated) return;
            this.editingByte = index;
            this.byteEditValue = this.selectedPage.bytes[index].toString(16).padStart(2, '0');
            this.$nextTick(() => {
                const editor = this.$el.querySelector('.byte-editor');
                if (editor) {
                    editor.focus();
                    editor.select();
                }
            });
        },
        commitByteEdit(index) {
            if (this.editingByte !== index || !this.selectedPage) return;
            const text = this.byteEditValue.trim();
            let value;
            if (!text) {
                this.addLog('error', 'write_byte', 'Byte value cannot be empty', { address: this.byteAddress(index), value: text }, 'rejected');
                this.editingByte = null;
                return;
            }
            try {
                value = Number(toBigInt(text));
            } catch (error) {
                this.addLog('error', 'write_byte', `Invalid byte value: ${text}`, { address: this.byteAddress(index), value: text }, 'rejected');
                this.editingByte = null;
                return;
            }
            if (!Number.isInteger(value) || value < 0 || value > 255) {
                this.addLog('error', 'write_byte', `Byte value must be between 0 and 255`, { address: this.byteAddress(index), value: text }, 'rejected');
                this.editingByte = null;
                return;
            }
            const address = this.selectedPage.base + BigInt(index);
            this.model.writeByte(address, value);
            this.changedBytes = new Set(this.changedBytes).add(address);
            this.addLog('success', 'write_byte', `${formatAddress(address)} changed to ${value.toString(16).padStart(2, '0')}`, { address: formatAddress(address), value }, 'byte written');
            this.editingByte = null;
            this.refreshSelection();
        },
        cancelByteEdit() {
            this.editingByte = null;
        },
        markChanged(address, size) {
            const next = new Set(this.changedBytes);
            for (let index = 0n; index < size; index += 1n) next.add(address + index);
            this.changedBytes = next;
        },
        addLog(kind, functionName, detail, args = {}, result = '') {
            const call = this.formatCall(functionName, args);
            let actionId = null;
            if (this.recording && !this.replaying && !['run_demo_scenario', 'record_start', 'record_stop'].includes(functionName)) {
                actionId = this.nextActionId++;
                this.recordedActions.push({ id: actionId, functionName, args: JSON.parse(JSON.stringify(args)), call });
            }
            this.log.unshift({ id: this.nextLogId++, actionId, kind, functionName, call, detail, result });
            this.log = this.log.slice(0, 40);
        },
        toggleRecording() {
            this.recording = !this.recording;
            this.addLog('system', this.recording ? 'record_start' : 'record_stop', this.recording ? 'New actions will be saved for replay' : `${this.recordedActions.length} actions captured`, {}, this.recording ? 'recording' : 'paused');
        },
        clearEvents() {
            this.log = [];
            this.recordedActions = [];
            this.nextLogId = 1;
            this.nextActionId = 1;
        },
        removeEvent(entry) {
            const actionId = entry.actionId;
            this.log = this.log.filter(item => item.id !== entry.id && (actionId === null || actionId === undefined || item.actionId !== actionId));
            if (actionId !== null && actionId !== undefined) {
                this.recordedActions = this.recordedActions.filter(action => action.id !== actionId);
            }
        },
        formatCall(functionName, args) {
            const values = {
                limine_allocator_reset: [],
                allocate_physical_bytes: [args.size],
                configure_memory_map: [args.pageCount, args.hhdmOffset, args.hhdmAvailable],
                memset: [args.destination, args.value, args.size],
                memcpy: [args.destination, args.source, args.size],
                memmove: [args.destination, args.source, args.size],
                memcmp: [args.destination, args.source, args.size],
                write_byte: [args.address, args.value],
            }[functionName] || Object.values(args);
            return `${functionName}(${values.map(value => typeof value === 'string' ? value : JSON.stringify(value)).join(', ')})`;
        },
        functionsText() {
            return this.recordedActions.map(action => action.call).join('\n');
        },
        async copyFunctions() {
            if (!this.functionsText()) return;
            if (navigator.clipboard) {
                await navigator.clipboard.writeText(this.functionsText());
                return;
            }
            const field = document.createElement('textarea');
            field.value = this.functionsText();
            document.body.appendChild(field);
            field.select();
            document.execCommand('copy');
            field.remove();
        },
        downloadFunctions() {
            if (!this.functionsText()) return;
            const blob = new Blob([`${this.functionsText()}\n`], { type: 'text/plain' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'vol-memory-actions.txt';
            link.click();
            URL.revokeObjectURL(link.href);
        },
        replay() {
            if (!this.recordedActions.length || this.replaying) return;
            const actions = JSON.parse(JSON.stringify(this.recordedActions));
            this.replaying = true;
            this.recording = false;
            this.addLog('system', 'replay_start', `Applying ${actions.length} recorded actions to the current state`, {}, 'replay started');
            actions.forEach(action => this.executeRecordedAction(action));
            this.replaying = false;
            this.addLog('system', 'replay_complete', `${actions.length} recorded actions executed`, {}, 'replay complete');
        },
        executeRecordedAction(action) {
            if (action.functionName === 'limine_allocator_reset') return this.reset();
            if (action.functionName === 'configure_memory_map') {
                this.pageCount = action.args.pageCount;
                this.hhdmOffsetInput = action.args.hhdmOffset;
                this.model.hhdmAvailable = action.args.hhdmAvailable;
                return this.rebuild();
            }
            if (action.functionName === 'allocate_physical_bytes') {
                this.allocationSize = action.args.size;
                return this.allocate();
            }
            if (['memset', 'memcpy', 'memmove', 'memcmp'].includes(action.functionName)) {
                this.operation = action.functionName;
                this.operationAddress = action.args.destination;
                this.operationSource = action.args.source || this.operationSource;
                this.operationSize = action.args.size;
                this.operationValue = action.args.value === undefined ? this.operationValue : action.args.value;
                return this.runOperation();
            }
            if (action.functionName === 'write_byte') {
                const address = toBigInt(action.args.address);
                this.model.writeByte(address, action.args.value);
                this.markChanged(address, 1n);
                this.addLog('success', 'write_byte', `replayed ${formatAddress(address)}`, action.args, 'byte written');
                return this.refreshSelection();
            }
        },
        roundedSize(size) { return `${Math.ceil(Number(size) / 4096) * 4096} bytes`; },
        formatAddress,
        formatBytes(value) {
            const number = Number(value);
            return number >= 1024 ? `${(number / 1024).toFixed(1)} KiB` : `${number} B`;
        },
        virtualAddress(physical) {
            if (!this.model.hhdmAvailable) return 'unavailable';
            const virtual = this.model.physicalToVirtual(physical);
            return virtual === 0n ? 'overflow' : formatAddress(virtual);
        },
        pageFill(page) {
            const allocation = this.model.allocations.find(item => page.base >= item.base && page.base < item.base + item.rounded);
            if (!allocation) return 0;
            return Math.min(100, Math.round(Number(allocation.requested) / 4096 * 100));
        },
        exportSnapshot() {
            const snapshot = JSON.stringify({ version: 1, pageCount: this.model.pageCount, hhdmAvailable: this.model.hhdmAvailable, hhdmOffset: this.model.hhdmOffset.toString(), allocations: this.model.allocations.map(item => ({ base: item.base.toString(), requested: item.requested.toString() })) }, null, 2);
            const blob = new Blob([snapshot], { type: 'application/json' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'vol-memory-snapshot.json';
            link.click();
            URL.revokeObjectURL(link.href);
        },
    },
}).mount('#app');
