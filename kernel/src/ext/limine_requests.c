#include <stdint.h>
#include <limine.h>
#include <flanterm.h>
#include <flanterm_backends/fb.h>

__attribute__((used, section(".limine_requests")))
volatile uint64_t limineBaseRevision[] = LIMINE_BASE_REVISION(6);

__attribute__((used, section(".limine_requests")))
volatile struct limine_hhdm_request hhdmRequest = {
    .id = LIMINE_HHDM_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests")))
volatile struct limine_framebuffer_request framebufferRequest = {
    .id = LIMINE_FRAMEBUFFER_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests")))
volatile struct limine_flanterm_fb_init_params_request flantermRequest = {
    .id = LIMINE_FLANTERM_FB_INIT_PARAMS_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests")))
volatile struct limine_memmap_request memoryMapRequest = {
    .id = LIMINE_MEMMAP_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests")))
volatile struct limine_tsc_frequency_request tscFrequencyRequest = {
    .id = LIMINE_TSC_FREQUENCY_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests")))
volatile struct limine_date_at_boot_request dateAtBootRequest = {
    .id = LIMINE_DATE_AT_BOOT_REQUEST_ID,
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

static struct flanterm_context *flantermContext = 0;

uint64_t limine_allocate_physical(uint64_t size);

int limine_terminal_init(void) {
    if (flantermRequest.response == 0 ||
        flantermRequest.response->entry_count == 0 ||
        flantermRequest.response->entries[0] == 0 ||
        framebufferRequest.response == 0 ||
        framebufferRequest.response->framebuffer_count == 0 ||
        framebufferRequest.response->framebuffers[0] == 0) {
        return 0;
    }

    struct limine_flanterm_fb_init_params *params =
        flantermRequest.response->entries[0];
    struct limine_framebuffer *framebuffer =
        framebufferRequest.response->framebuffers[0];

    if ((framebuffer->height != 0 &&
         framebuffer->pitch > SIZE_MAX / framebuffer->height) ||
        !limine_hhdm_available()) {
        return 0;
    }

    size_t snapshotSize = framebuffer->pitch * framebuffer->height;
    uint64_t snapshotPhysical = limine_allocate_physical(snapshotSize);
    if (snapshotPhysical == 0) {
        return 0;
    }

    uint8_t *snapshot = (uint8_t *)(uintptr_t)(
        snapshotPhysical + limine_hhdm_offset());
    uint8_t *source = (uint8_t *)framebuffer->address;
    for (size_t index = 0; index < snapshotSize; index++) {
        snapshot[index] = source[index];
    }

    flantermContext = flanterm_fb_init(
        0,
        0,
        framebuffer->address,
        framebuffer->width,
        framebuffer->height,
        framebuffer->pitch,
        framebuffer->red_mask_size,
        framebuffer->red_mask_shift,
        framebuffer->green_mask_size,
        framebuffer->green_mask_shift,
        framebuffer->blue_mask_size,
        framebuffer->blue_mask_shift,
        params->canvas,
        params->ansi_colours,
        params->ansi_bright_colours,
        &params->default_bg,
        &params->default_fg,
        &params->default_bg_bright,
        &params->default_fg_bright,
        params->font,
        params->font_width,
        params->font_height,
        params->font_spacing,
        params->font_scale_x,
        params->font_scale_y,
        params->margin,
        params->rotation,
        true
    );

    for (size_t index = 0; index < snapshotSize; index++) {
        source[index] = snapshot[index];
    }

    return flantermContext != 0;
}

void limine_terminal_write(const char *message) {
    if (flantermContext == 0 || message == 0) {
        return;
    }

    size_t length = 0;
    while (message[length] != '\0') {
        length++;
    }
    flanterm_write(flantermContext, message, length);
}

void limine_terminal_set_cursor_position(uint64_t column, uint64_t row) {
    if (flantermContext == 0) {
        return;
    }

    flanterm_set_cursor_pos(flantermContext, column, row);
}

__attribute__((used, section(".limine_requests_start")))
volatile uint64_t limine_requests_start_marker[] = LIMINE_REQUESTS_START_MARKER;

__attribute__((used, section(".limine_requests_end")))
volatile uint64_t limine_requests_end_marker[] = LIMINE_REQUESTS_END_MARKER;


#define PAGE_SIZE 4096

static uint64_t allocation_entry_index = 0;
static uint64_t allocation_address = 0;


void limine_allocator_reset(void) {
    allocation_entry_index = 0;
    allocation_address = 0;
}

struct allocation_state {
    uint64_t entry_index;
    uint64_t address;
};

struct allocation_state limine_get_allocation_state(void) {
    return (struct allocation_state) {
        .entry_index = allocation_entry_index,
        .address = allocation_address
    };
}

uint64_t limine_allocate_physical(uint64_t size) {
    if (memoryMapRequest.response == 0 || size == 0) {
        return 0;
    }

    if (size > UINT64_MAX - (PAGE_SIZE - 1)) {
        return 0;
    }

    size = (size + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1);

    while (allocation_entry_index < memoryMapRequest.response->entry_count) {
        struct limine_memmap_entry *entry =
            memoryMapRequest.response->entries[allocation_entry_index];

        if (entry->type != LIMINE_MEMMAP_USABLE) {
            allocation_entry_index++;
            allocation_address = 0;
            continue;
        }

        uint64_t region_end = entry->base + entry->length;
        if (region_end < entry->base) {
            allocation_entry_index++;
            allocation_address = 0;
            continue;
        }

        uint64_t start = allocation_address;
        if (start < entry->base) {
            start = entry->base;
        }

        start = (start + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1);

        if (start <= region_end && size <= region_end - start) {
            allocation_address = start + size;
            return start;
        }

        allocation_entry_index++;
        allocation_address = 0;
    }

    return 0;
}