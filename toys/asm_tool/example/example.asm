section .data
num1 db 0
num2 db 0
result db 0
error_message db 'Error: Division by zero', 10
error_message_length equ $ - error_message

section .bss
temp resb 1

section .text
global _start

_start:
    ; Read the first number, operation, and second number.
    mov eax, 3
    mov ebx, 0
    lea ecx, [num1]
    mov edx, 1
    int 0x80

    mov eax, 3
    mov ebx, 0
    lea ecx, [temp]
    mov edx, 1
    int 0x80

    mov eax, 3
    mov ebx, 0
    lea ecx, [num2]
    mov edx, 1
    int 0x80

    mov al, [temp]
    cmp al, '+'
    je add_numbers
    cmp al, '-'
    je subtract_numbers
    cmp al, '*'
    je multiply_numbers
    cmp al, '/'
    je divide_numbers

    mov eax, 1
    xor ebx, ebx
    int 0x80

add_numbers:
    mov al, [num1]
    add al, [num2]
    jmp finish

subtract_numbers:
    mov al, [num1]
    sub al, [num2]
    jmp finish

multiply_numbers:
    mov al, [num1]
    mul byte [num2]
    jmp finish

divide_numbers:
    mov al, [num2]
    cmp al, 0
    je divide_by_zero
    mov al, [num1]
    cdq
    idiv byte [num2]
    jmp finish

divide_by_zero:
    mov eax, 4
    mov ebx, 1
    lea ecx, [error_message]
    mov edx, error_message_length
    int 0x80
    jmp _start

finish:
    mov [result], al

    mov eax, 4
    mov ebx, 1
    lea ecx, [result]
    mov edx, 1
    int 0x80

    mov eax, 1
    xor ebx, ebx
    int 0x80