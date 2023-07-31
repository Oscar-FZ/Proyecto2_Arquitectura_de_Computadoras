addi x1, x0, 0
addi x2, x0, 0 
addi x3, x0, 4 
addi x4, x0, 4 
addi x5, x0, 0
addi x6, x0, 50
fila_loop: bge x1, x3, fin 
addi x2, x0,  0   
columna_loop: bge x2, x4, siguiente_fila
add x5, x1, x2 
slli x7, x1, 2 
add x7, x7, x2 
sw x5, 0(x6)  
addi x6, x6, 4 
addi x2, x2, 1 
jal x0, columna_loop  
siguiente_fila: addi x1, x1, 1 
jal x0, fila_loop 
fin: X X X
X X X 