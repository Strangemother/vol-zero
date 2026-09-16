"""Stream the VirtualBox TCP serial console to the current terminal."""

from __future__ import annotations

import os
import socket
import sys
import time


SERIAL_PORT = 1234


def serial_host() -> str:
    if os.name == "nt":
        return "127.0.0.1"
    try:
        with open("/etc/resolv.conf", encoding="utf-8") as resolv_conf:
            for line in resolv_conf:
                fields = line.split()
                if len(fields) >= 2 and fields[0] == "nameserver":
                    return fields[1]
    except OSError:
        pass
    return "127.0.0.1"


def main() -> int:
    host = serial_host()
    print(f"Waiting for VirtualBox serial console at {host}:{SERIAL_PORT}...", file=sys.stderr)
    try:
        while True:
            try:
                with socket.create_connection((host, SERIAL_PORT), timeout=1) as connection:
                    print("Connected.", file=sys.stderr)
                    while data := connection.recv(4096):
                        sys.stdout.buffer.write(data)
                        sys.stdout.buffer.flush()
                    return 0
            except (ConnectionRefusedError, TimeoutError, OSError):
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nDisconnected.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())