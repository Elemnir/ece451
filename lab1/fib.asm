        .data
PROMPT: .asciiz "Enter n to calculate the n-th Fibonacci number: "

        .text
        .globl main
main:
    subu    $sp, $sp, 32 
    sw      $ra, 20($sp)
    sw      $fp, 16($sp)
    addiu   $fp, $sp, 28

    li      $v0, 4
    la      $a0, PROMPT
    syscall
    li      $v0, 5
    syscall
    move    $a0, $v0
    
    # Function call
    jal     fib

    # Print result of fib()
    move    $a0, $v0
    li      $v0, 1
    syscall

    # Print newline
    li      $a0, 0xA
    li      $v0, 11
    syscall

    # Return
    move    $v0, $0
    lw      $ra, 20($sp)
    lw      $fp, 16($sp)
    addiu   $sp, $sp, 32
    jr      $ra


fib:
    # Set up frame and save registers
    subu    $sp, $sp, 40
    sw      $ra, 16($sp)
    sw      $fp, 8($sp)
    addiu   $fp, $sp, 36
    sw      $a0, 0($fp)
    sw      $s0, 4($sp)
    sw      $s1, 0($sp)
    
    # Check for base cases
    lw      $s0, 0($fp)
    blez    $s0, fib_base0
    li      $t0, 1
    beq     $s0, $t0, fib_base1

    addi    $a0, $s0, -1
    jal     fib
    move    $s1, $v0

    addi    $a0, $s0, -2
    jal     fib
    add     $v0, $s1, $v0
    j       fib_return

fib_base0:
    add     $v0, $0, $0
    j       fib_return

fib_base1:
    li      $v0, 1
    j       fib_return

fib_return:
    # Deconstruct frame and return
    lw      $ra, 16($sp)
    lw      $fp,  8($sp)
    lw      $s0,  4($sp)
    lw      $s1,  0($sp)
    addiu   $sp, $sp, 40
    jr      $ra

