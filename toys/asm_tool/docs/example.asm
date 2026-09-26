section .data
num1 db 0
num2 db 0
result db 0

section .bss
temp resb 1

section .text
global _start

_start:

; Input first number
mov eax, 3 ; system call number (sys_read)
mov ebx, 0 ; file descriptor (stdin)
lea ecx, [num1] ; buffer
mov edx, 1 ; length
int 0x80 ; call kernel

; Input operation
mov eax, 3 ; system call number (sys_read)
mov ebx, 0 ; file descriptor (stdin)
lea ecx, [temp] ; buffer
mov edx, 1 ; length
int 0x80 ; call kernel

; Input second number
mov eax, 3 ; system call number (sys_read)
mov ebx, 0 ; file descriptor (stdin)
lea ecx, [num2] ; buffer
mov edx, 1 ; length
int 0x80 ; call kernel

; Perform operation
mov al, [temp] ; operation
cmp al, '+' ; compare with addition
je add
cmp al, '-' ; compare with subtraction
je subtract
cmp al, '*' ; compare with multiplication
je multiply
cmp al, '/' ; compare with division
je divide

; If invalid operation, exit
mov eax, 1 ; system call number (sys_exit)
xor ebx, ebx ; exit code
int 0x80 ; call kernel

add:
mov al, [num1] ; first number
add al, [num2] ; add second number
jmp finish

subtract:
mov al, [num1] ; first number
sub al, [num2] ; subtract second number
jmp finish

multiply:
mov al, [num1] ; first number
mul byte [num2] ; multiply by second number
jmp finish

divide:
mov al, [num2] ; second number
cmp al, 0 ; compare with zero
je divide_by_zero
mov al, [num1] ; first number
cdq ; convert to doubleword
idiv byte [num2] ; divide by second number
jmp finish

divide_by_zero:
mov eax, 4 ; system call number (sys_write)
mov ebx, 1 ; file descriptor (stdout)
lea ecx, [error_message] ; message to print
mov edx, 15 ; message length
int 0x80 ; call kernel
jmp _start ; prompt for input again

error_message db 'Error: Division by zero'

finish:
mov [result], al ; store result

; Output result
mov eax, 4 ; system call number (sys_write)
mov ebx, 1 ; file descriptor (stdout)
lea ecx, [result] ; buffer
mov edx, 1 ; length
int 0x80 ; call kernel

; Exit
mov eax, 1 ; system call number (sys_exit)
xor ebx, ebx ; exit code
int 0x80 ; call kernel