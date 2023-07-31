addi x5, x0, 12
addi x6, x0, 37
addi x8, x0, 1 
addi x7, x0, 0 
LOOP: beq x6, x8, END
slli x10, x5, 1 
andi x11, x6, 1 
beq x11, x8, SUMA
return: add x5, x0, x10 
srli x12, x6, 1 
add x6, x0, x12 
jal x0, LOOP
SUMA: add x7, x7, x5 
jal x0, return
END: add x31, x7, x5 
X X X X