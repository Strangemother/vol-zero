INT 15h / AH = 86h - BIOS wait function.

input:
    CX:DX = interval in microseconds

return:
    CF clear if successful (wait interval elapsed),
    CF set on error or when wait function is already in progress.

example:

    mov   cx, 0006H   ; CX:DX = 00068480h Pause for about 0.4 sec
    mov   dx, 8480H
    mov   ah, 86h     ; BIOS.Delay

Note:
    the resolution of the wait period is 977 microseconds on many systems (1 million microseconds - 1 second).
    Windows XP does not support this interrupt (always sets CF=1).
