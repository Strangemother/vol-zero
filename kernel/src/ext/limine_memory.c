#include <stdint.h>
#include <limine.h>

#include "limine_requests.h"

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

uint64_t limine_hhdm_offset(void) {
    if (hhdmRequest.response == 0) {
        return 0;
    }
    return hhdmRequest.response->offset;
}

uint64_t limine_hhdm_available(void) {
    return hhdmRequest.response != 0;
}

uint64_t limine_usable_memory_bytes(void) {
    return limine_memory_bytes_by_type(LIMINE_MEMMAP_USABLE);
}

uint64_t limine_tsc_frequency(void) {
    if (tscFrequencyRequest.response == 0) {
        return 0;
    }
    return tscFrequencyRequest.response->frequency;
}

int64_t limine_date_at_boot(void) {
    if (dateAtBootRequest.response == 0) {
        return 0;
    }
    return dateAtBootRequest.response->timestamp;
}
