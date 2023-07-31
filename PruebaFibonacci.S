addi x1, x0, 0
addi x2, x0, 1
addi x4, x0, 10
addi x3, x0, 0
loop: beq x3, x4, exit 
add x5, x1, x2
add x1, x2, x0
add x2, x5, x0
addi x3, x3, 1
jal x0, loop
exit: add x10, x2, x0
X X X