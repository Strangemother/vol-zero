#include <stdint.h>
#include <limine.h>

__attribute__((used, section(".limine_requests")))
volatile uint64_t limineBaseRevision[] = LIMINE_BASE_REVISION(6);

__attribute__((used, section(".limine_requests")))
volatile struct limine_framebuffer_request framebufferRequest = {
    .id = LIMINE_FRAMEBUFFER_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests")))
volatile struct limine_memmap_request memoryMapRequest = {
    .id = LIMINE_MEMMAP_REQUEST_ID,
    .revision = 0
};

uint64_t limine_memory_bytes_by_type(uint64_t memoryType) {
    if (memoryMapRequest.response == 0) {
        return 0;
    }

    uint64_t total = 0;
    for (uint64_t index = 0; index < memoryMapRequest.response->entry_count; ++index) {
        struct limine_memmap_entry *entry = memoryMapRequest.response->entries[index];
        if (entry->type != memoryType) {
            continue;
        }
        if (UINT64_MAX - total < entry->length) {
            return UINT64_MAX;
        }
        total += entry->length;
    }
    return total;
}

uint64_t limine_usable_memory_bytes(void) {
    return limine_memory_bytes_by_type(LIMINE_MEMMAP_USABLE);
}

__attribute__((used, section(".limine_requests_start")))
volatile uint64_t limine_requests_start_marker[] = LIMINE_REQUESTS_START_MARKER;

__attribute__((used, section(".limine_requests_end")))
volatile uint64_t limine_requests_end_marker[] = LIMINE_REQUESTS_END_MARKER;