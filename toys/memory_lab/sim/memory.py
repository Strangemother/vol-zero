"""Small, addressable physical-memory simulator for VOL experiments."""

PAGE_SIZE = 4096
MEMORY_BASE = 0x100000
UINT64_MAX = (1 << 64) - 1

_pages = {}
_allocations = []
_usable_regions = [(MEMORY_BASE, UINT64_MAX + 1)]
_entry_index = 0
_next_address = 0
_memory_limit = None
_hhdm_available = True
_hhdm_offset = 0xFFFF800000000000


def reset():
    """Reset allocation state without clearing the simulated physical bytes."""
    global _allocations, _entry_index, _next_address
    _allocations = []
    _entry_index = 0
    _next_address = 0


def configure_memory(regions):
    """Set usable ``(base, size)`` regions, like Limine memory-map entries."""
    global _usable_regions
    normalized = []
    for base, size in regions:
        base = _validate_uint64(base)
        size = _validate_uint64(size)
        end = base + size
        if size == 0 or end > UINT64_MAX + 1:
            raise ValueError("memory region is outside the 64-bit address space")
        normalized.append((base, end))
    _usable_regions = normalized
    reset()


def set_memory_limit(size=None):
    """Set a total byte limit, or pass ``None`` for unlimited memory."""
    global _memory_limit
    if size is not None and int(size) < 0:
        raise ValueError("memory limit cannot be negative")
    _memory_limit = None if size is None else int(size)
    reset()


def set_hhdm(offset=0, available=True):
    """Configure the simulated Higher Half Direct Map response."""
    global _hhdm_available, _hhdm_offset
    _hhdm_available = bool(available)
    _hhdm_offset = _validate_uint64(offset)


def hhdm_available():
    return _hhdm_available


def hhdm_offset():
    return _hhdm_offset


def uint8(value):
    """Convert a character or integer to the value of a Nim ``uint8``."""
    if isinstance(value, str):
        if len(value) != 1:
            raise ValueError("uint8 expects one character")
        value = ord(value)
    value = int(value)
    if value < 0 or value > 0xff:
        raise ValueError("uint8 value must be between 0 and 255")
    return value


def current_state():
    """Return the Limine-style allocation cursor state."""
    return {"entry_index": _entry_index, "address": _next_address}


def physical_to_virtual(physical, offset=None):
    physical = _validate_uint64(physical)
    offset = _hhdm_offset if offset is None else _validate_uint64(offset)
    if physical == 0 or offset > UINT64_MAX - physical:
        return 0
    return physical + offset


def allocate_physical_bytes(size):
    """Allocate page-rounded physical memory and return its address."""
    global _entry_index, _next_address
    size = _validate_uint64(size)
    if size == 0 or size > UINT64_MAX - (PAGE_SIZE - 1):
        return 0
    rounded_size = (size + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1)

    while _entry_index < len(_usable_regions):
        region_start, region_end = _usable_regions[_entry_index]
        start = max(_next_address, region_start)
        start = (start + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1)
        end = start + rounded_size
        if end <= region_end:
            allocated_bytes = sum(item[1] - item[0] for item in _allocations)
            if _memory_limit is not None and allocated_bytes + rounded_size > _memory_limit:
                return 0
            for page in range(start, end, PAGE_SIZE):
                _pages.setdefault(page, bytearray(PAGE_SIZE))
            _allocations.append((start, end))
            _next_address = end
            return start
        _entry_index += 1
        _next_address = 0
    return 0


def _validate_uint64(value):
    value = int(value)
    if value < 0 or value > UINT64_MAX:
        raise ValueError("value is outside the uint64 address space")
    return value


def _locate(address, size=1):
    address = _validate_uint64(address)
    size = _validate_uint64(size)
    if address + size > UINT64_MAX + 1:
        raise ValueError("address range is outside the 64-bit address space")
    for start, end in _allocations:
        if start <= address and address + size <= end:
            return address, end
    raise ValueError(f"address 0x{address:x} is not allocated")


def read_byte(address):
    """Read one byte from an allocated physical address."""
    address, _ = _locate(address)
    page = address - (address % PAGE_SIZE)
    return _pages[page][address % PAGE_SIZE]


def write_byte(address, value):
    """Write one byte to an allocated physical address."""
    address, _ = _locate(address)
    page = address - (address % PAGE_SIZE)
    _pages[page][address % PAGE_SIZE] = int(value) & 0xff


def read(address, size):
    """Read bytes from an allocated physical range."""
    if int(size) == 0:
        return b""
    address, _ = _locate(address, size)
    return bytes(read_byte(address + offset) for offset in range(int(size)))


def write(address, data):
    """Write bytes to an allocated physical range."""
    data = bytes(data)
    if not data:
        return
    _locate(address, len(data))
    for offset, value in enumerate(data):
        write_byte(address + offset, value)


def memcpy(destination, source, size):
    """Copy bytes forward, matching the kernel's non-overlapping memcpy."""
    size = _validate_uint64(size)
    if size == 0:
        return int(destination)
    _locate(source, size)
    _locate(destination, size)
    for offset in range(size):
        write_byte(destination + offset, read_byte(source + offset))
    return int(destination)


def memmove(destination, source, size):
    """Copy bytes safely when source and destination overlap."""
    size = _validate_uint64(size)
    if size == 0:
        return int(destination)
    values = read(source, size)
    write(destination, values)
    return int(destination)


def memcmp(first, second, size):
    """Compare two ranges and return -1, 0, or 1."""
    if int(size) == 0:
        return 0
    left = read(first, size)
    right = read(second, size)
    return (left > right) - (left < right)


def memset(address, value, size):
    """Fill an allocated range and return its destination address."""
    if int(size) == 0:
        return int(address)
    _locate(address, size)
    write(address, bytes([int(value) & 0xff]) * int(size))
    return int(address)


def physical_bytes(address):
    """Return a writable view over the allocation beginning at ``address``."""
    if not hhdm_available() or physical_to_virtual(address) == 0:
        return None
    address, end = _locate(address, 1)
    for start, allocation_end in _allocations:
        if start == address:
            return memoryview(_pages[start])[0:allocation_end - start]
    raise ValueError(f"address 0x{address:x} is not an allocation base")


reset()