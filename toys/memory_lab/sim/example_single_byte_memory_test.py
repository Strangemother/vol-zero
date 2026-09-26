from toys.memory_lab.sim.memory import *


def perform_single_byte_memory_test():
    physical = allocate_physical_bytes(PAGE_SIZE)
    bytes_view = physical_bytes(physical)

    if bytes_view is None:
        return 1  # allocation or HHDM mapping failed

    bytes_view[3] = uint8("X")
    if bytes_view[3] == uint8("X"):
        return 0  # allocation and HHDM mapping succeeded
    return 1  # allocation succeeded but HHDM mapping failed


if __name__ == "__main__":
    reset()
    result = perform_single_byte_memory_test()
    print(f"perform_single_byte_memory_test() -> {result}")
    raise SystemExit(result)
