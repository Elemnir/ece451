        .data
PROMPT: .asciiz "Enter value to take the factorial of: "

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
    jal     fact

    #print result of fact()
    move    $a0, $v0
    li      $v0, 1
    syscall

    #print newline
    li      $a0, 0xA
    li      $v0, 11
    syscall

    #return
    lw      $ra, 20($sp)
    lw      $fp, 16($sp)
    addiu   $sp, $sp, 32
    jr      $ra

fact:
    subu    $sp, $sp, 32
    sw      $ra, 20($sp)
    sw      $fp, 16($sp)
    addiu   $fp, $sp, 28
    sw      $a0, 0($fp)
    
    lw      $v0, 0($fp)
    bgtz    $v0, $L2
    li      $v0, 1
    jr      $L1

$L2:
    lw      $v1, 0($fp)
    subu    $v0, $v1, 1
    move    $a0, $v0
    jal     fact
    lw      $v1, 0($fp)
    mul     $v0, $v0, $v1

$L1:
    lw      $ra, 20($sp)
    lw      $fp, 16($sp)
    addiu   $sp, $sp, 32
    jr      $ra

