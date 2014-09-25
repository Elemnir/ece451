        .data
str:    .asciiz "Hello World!\n"

        .text

        .globl main
main:
    li $v0, 4
    la $a0, str
    syscall
    jr $ra
