#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include <flanterm.h>
#include <flanterm_backends/fb.h>

#include "limine_requests.h"

static struct flanterm_context *flantermContext = 0;
static uint64_t terminalColumns = 0;
static uint64_t terminalRows = 0;

int flanterm_terminal_init(int preserve) {
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

    size_t snapshotSize = 0;
    uint8_t *snapshot = 0;
    if (preserve) {
        if ((framebuffer->height != 0 &&
             framebuffer->pitch > SIZE_MAX / framebuffer->height) ||
            !limine_hhdm_available()) {
            return 0;
        }

        snapshotSize = framebuffer->pitch * framebuffer->height;
        uint64_t snapshotPhysical = limine_allocate_physical(snapshotSize);
        if (snapshotPhysical == 0) {
            return 0;
        }

        snapshot = (uint8_t *)(uintptr_t)(
            snapshotPhysical + limine_hhdm_offset());
        uint8_t *source = (uint8_t *)framebuffer->address;
        for (size_t index = 0; index < snapshotSize; index++) {
            snapshot[index] = source[index];
        }
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

    if (preserve && flantermContext != 0) {
        uint8_t *source = (uint8_t *)framebuffer->address;
        for (size_t index = 0; index < snapshotSize; index++) {
            source[index] = snapshot[index];
        }
    }

    if (flantermContext == 0) {
        return 0;
    }

    size_t columns = 0;
    size_t rows = 0;
    flanterm_get_dimensions(flantermContext, &columns, &rows);
    terminalColumns = columns;
    terminalRows = rows;
    return 1;
}

uint64_t flanterm_terminal_columns(void) {
    return terminalColumns;
}

uint64_t flanterm_terminal_rows(void) {
    return terminalRows;
}

void flanterm_terminal_write(const char *message) {
    if (flantermContext == 0 || message == 0) {
        return;
    }

    size_t length = 0;
    while (message[length] != '\0') {
        length++;
    }
    flanterm_write(flantermContext, message, length);
}

void flanterm_terminal_set_cursor_position(uint64_t column, uint64_t row) {
    if (flantermContext == 0) {return; };
    flanterm_set_cursor_pos(flantermContext, column, row);
}

void flanterm_terminal_set_text_fg(uint64_t colour, bool bright) {
    if (flantermContext == 0) {return; };
    flanterm_set_text_fg(flantermContext, colour, bright);
}

void flanterm_terminal_set_text_bg(uint64_t colour, bool bright) {
    if (flantermContext == 0) {return; };
    flanterm_set_text_bg(flantermContext, colour, bright);
}

void flanterm_terminal_reset_text_fg(void) {
    if (flantermContext == 0) {return; };
    flanterm_reset_text_fg(flantermContext);
}

void flanterm_terminal_reset_text_bg(void) {
    if (flantermContext == 0) {return; };
    flanterm_reset_text_bg(flantermContext);
}
