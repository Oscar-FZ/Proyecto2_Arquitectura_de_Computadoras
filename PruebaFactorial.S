addi x6, x0, 2
addi x7, x0, 3
add x1, x6, x7
addi x2, x0, 1
addi x3, x0, 0
addi x8, x0, 80
loop: beq x3, x1, end
addi x5, x0, 0
addi x3, x3, 1
add x4, x0, x2
sw x4, 0(x8)
addi x8, x8, 4
loop2: beq x5, x3, end2
addi x5, x5, 1
add x2, x2, x4
jal x0, loop2
end2: jal x0, loop
end: X X X
X X X