#[
Monotonic time module for handling TSC-based time measurements.
]#

{.emit: """
static inline unsigned long long nim_read_tsc(void) {
    unsigned int low;
    unsigned int high;
    __asm__ volatile ("lfence\n\trdtsc"
        : "=a"(low), "=d"(high)
        :
        : "memory");
    return ((unsigned long long)high << 32) | low;
}
""".}


proc read_tsc(): culonglong {.importc: "nim_read_tsc".}


proc bootloader_tsc_frequency(): uint64 {.importc: "limine_tsc_frequency".}


proc bootloader_date_at_boot(): int64 {.importc: "limine_date_at_boot".}

#[
Returns the TSC frequency in Hz.
Returns zero when for no TSC frequency.
]#
proc tsc_frequency*(): uint64 =
    result = bootloader_tsc_frequency()


#[
Returns the wall-clock Unix timestamp at boot, in seconds.
This is not monotonic time. 
Zero means no Limine response was available.
]#
proc date_at_boot*(): int64 =
    result = bootloader_date_at_boot()


var
    tsc_start: uint64
    tsc_started: bool


proc read_tsc64*(): uint64 =
    return uint64(read_tsc())


proc record_start*() =
    ## Establishes the starting point for monotonic elapsed time.
    tsc_start = read_tsc64()
    tsc_started = true

#[
Returns monotonic elapsed time since boot, in nanoseconds.
Returns zero when for no usable TSC frequency.
]#
proc delta*(): uint64 =
    let frequency = tsc_frequency()
    if frequency == 0:
        return 0
    let current = read_tsc64()
    if not tsc_started:
        record_start()
        return 0

    let elapsed_ticks = current - tsc_start
    let whole_seconds = elapsed_ticks div frequency
    let remaining_ticks = elapsed_ticks mod frequency
    result = whole_seconds * 1_000_000_000'u64 +
        (remaining_ticks * 1_000_000_000'u64) div frequency
