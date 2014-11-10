        .data
PROMPT: .asciiz "How many Fibonacci primes should be calculated: "
DELMT:  .asciiz ", "
        .text
        .globl main
main:
    subu    $sp, $sp, 44 
    sw      $ra, 20($sp)
    sw      $fp, 12($sp)
    addiu   $fp, $sp, 40
    sw      $s0, 8($sp)
    sw      $s1, 4($sp)
    sw      $s2, 0($sp)

    li      $v0, 4
    la      $a0, PROMPT
    syscall
    li      $v0, 5
    syscall
    move    $s0, $v0
    move    $s1, $0

main_loop:
    sub     $t0, $s1, $s0
    bgez    $t0, main_ret

    jal     fib
    move    $s2, $v0
    move    $a0, $v0
    
    jal     prime
    beq     $v0, $0, main_skip
    
    addi    $s1, $s1, 1
    move    $a0, $s2 
    li      $v0, 1
    syscall
    li      $v0, 4
    la      $a0, DELMT
    syscall

main_skip:
    j       main_loop

main_ret:
    # Print newline
    li      $a0, 0xA
    li      $v0, 11
    syscall

    # Return
    move    $v0, $0
    lw      $ra, 20($sp)
    lw      $fp, 12($sp)
    lw      $s0, 8($sp)
    lw      $s1, 4($sp)
    lw      $s2, 0($sp)
    addiu   $sp, $sp, 44
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

    # Compute the LHS
    addi    $a0, $s0, -1
    jal     fib
    move    $s1, $v0
    
    # Compute the RHS
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


prime:
    addi    $t2, $a0, -1
    blez    $t2, prime_false
    li      $t0, 2

prime_loop:
    beq     $t0, $a0, prime_true
    div     $a0, $t0
    mfhi    $t1
    beqz    $t1, prime_false
    addi    $t0, $t0, 1
    j       prime_loop

prime_true:
    li      $v0, 1
    jr      $ra

prime_false:
    li      $v0, 0
    jr      $ra
