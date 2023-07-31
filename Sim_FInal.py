import time


#inicio = timer()
instrucciones = []
#defino una matriz de registros de tamaño 32
RegFile = [0,0,0,0,
           0,0,0,0,
           0,0,0,0,
           0,0,0,0,
           0,0,0,0,
           0,0,0,0,
           0,0,0,0,
           0,0,0,0]
#Defino un tamaño de memoria ram
ram = [0]*500

reg_EnUso = ["X","X","X","X","X"]
RegsForwarding = {"0":0}
Dir_Prediccion = {}
reg_IF_ID = ["X","X"]
reg_ID_EX = ["X","X"]
reg_Stall = ["X","X"]
reg_EX_MEM = ["X","X"]
reg_MEM_WB = ["X","X"]
reg_WB_FIN = ["X","X"]

#Defino los operandos que puede realizar cada tipo de instruccion en matrices
tipo_R = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and"]
tipo_I = ["lb", "lh", "lw", "lbu", "lhu", "slli", "srli", "srai", "addi", "slti", "sltiu", "xori", "ori", "andi"]
tipo_S = ["sb", "sh", "sw"]
tipo_SB = ["beq", "bne", "blt", "bge", "bltu", "bgeu"] 
tipo_U = ["lui", "auipc"] 
tipo_UJ = ["jal", "jalr"]



#Hacemos el fetch de la instrucción,toma dos argumentos: "insts" y "i". La función comprueba si el primer elemento de la lista "instrucciones" es igual a "X". 
# Si es así, devuelve una lista con dos elementos "X". Si no, devuelve una lista de cadenas que resultan de dividir la cadena "insts[i]" en los espacios en blanco.
def fetch(insts,i):
    if insts[0] == "X":
        return ["X", "X"]
    
    elif ":" in (insts[i].split())[0]:
        return (insts[i].split())[1:]
    
    else:
        return insts[i].split()

#Hacemos el decode, el if splitea igual que el Fetch con diferencia en que el else, compara el archivo separado por espacios en blanco que se hizo anteriormente en el fetch
# y luego compara la posición 0 de esa matriz y si es algun valor definido en la matriz tipo_I, tipo_R, tipo_S, etc y según el tipo de instrucción que sea sigue la estructura para
#los operandos OP, RD, RS1 y RS2 o IMM y lo que hace es cambiar las X por nada (lo elimina) y y tambien elimina las ","
def decode(inst, aux):
    if inst[0] == "X":
        return ["X","X"], aux

    else:
        if inst[0] in tipo_R:
            OP = inst[0]
            RD = (inst[1].replace("x","")).replace(",","")
            RS1 = (inst[2].replace("x","")).replace(",","")
            RS2 = (inst[3].replace("x","")).replace(",","")

            return ["R", OP, int(RD), int(RS1), int(RS2)], aux
        
        elif inst[0] in tipo_I:
            OP = inst[0]
            RD = (inst[1].replace("x","")).replace(",","")
            RS1 = (inst[2].replace("x","")).replace(",","")
            IMM = inst[3]

            return ["I", OP, int(RD), int(RS1), int(IMM)], aux
        
        elif inst[0] in tipo_S:
            OP = inst[0]
            RS1 = (inst[1].replace("x","")).replace(",","")
            RS2 = (((inst[2].replace("("," ")).replace(")"," ")).replace("x"," ")).split()[1]
            IMM = (((inst[2].replace("("," ")).replace(")"," ")).replace("x"," ")).split()[0]

            return ["S", OP, int(RS1), int(RS2), int(IMM)], aux
        
        elif inst[0] in tipo_SB:
            OP = inst[0]
            RS1 = (inst[1].replace("x","")).replace(",","")
            RS2 = (inst[2].replace("x","")).replace(",","")
            IMM = inst[3]

            return ["SB", OP, int(RS1), int(RS2), IMM], aux

        elif inst[0] in tipo_U:
            return "U", aux
        
        elif inst[0] in tipo_UJ:
            OP = inst[0]
            RD = (inst[1].replace("x","")).replace(",","")
            IMM = inst[2] # se asume que el inmediato está en formato decimal

            return ["UJ", OP, RegFile[int(RD)], IMM], aux

        else:
            return "ERROR", "ERROR"
        
#Funcion definada para el execute, compara el la matriz de instanciación (inst) en la posición 0 para ver el tipo de instrucion que es.
#luego compara la posicion 1 para ver que operacion debe realizar y en base a eso retorna la operación
def execute(inst, aux):
    global RegsForwarding
    if inst[0] == "X":
        return ["X","X"]

    else:

        if aux==0:
            if inst[0] == "R":
                if inst[1] == "add":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] + RegFile[inst[4]]]
                elif inst[1] == "sub":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] - RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] - RegFile[inst[4]]]
                elif inst[1] == "sll":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] << RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] << RegFile[inst[4]]]
                elif inst[1] == "slt":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] < RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] < RegFile[inst[4]]]
                elif inst[1] == "sltu":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] < RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] < RegFile[inst[4]]]
                elif inst[1] == "xor":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] ^ RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] ^ RegFile[inst[4]]]
                elif inst[1] == "srl":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] >> RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] >> RegFile[inst[4]]]
                elif inst[1] == "sra":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] >> RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] >> RegFile[inst[4]]]
                elif inst[1] == "or":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] | RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] | RegFile[inst[4]]]
                elif inst[1] == "and":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] & RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegFile[inst[3]] & RegFile[inst[4]]]
                else:
                    return "ERROR"
                
            elif inst[0] == "I":
                if inst[1] == "lb":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "lh":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "lw":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "lbu":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "lhu":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "slli":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] << inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] << inst[4]]
                elif inst[1] == "srli":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] >> inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] >> inst[4]]
                elif inst[1] == "srai":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] >> inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] >> inst[4]]
                elif inst[1] == "addi":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "slti":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] < inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] < inst[4]]
                elif inst[1] == "sltiu":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] < inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] < inst[4]]
                elif inst[1] == "xori":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] ^ inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] ^ inst[4]]
                elif inst[1] == "ori":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] | inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] | inst[4]]
                elif inst[1] == "andi":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] & inst[4]
                    return ["I", inst[1], inst[2], RegFile[inst[3]] & inst[4]]
                else:
                    return "ERROR"
                
            elif inst[0] == "S": 
                if inst[1] == "sb":
                    return ["S", inst[1], RegFile[inst[2]], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "sh":
                    return ["S", inst[1], RegFile[inst[2]], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "sw":
                    print("TIPO 0")
                    return ["S", inst[1], RegFile[inst[2]], RegFile[inst[3]] + inst[4]]
                else:
                    return "ERROR"
        #Agregando instrucciones para branches     
            elif inst[0] == "SB":
                if inst[1] == "beq":
                    if RegFile[inst[2]] == RegFile[inst[3]]:
                        return ["SB", "beq", etiquetas[inst[4]]]
                    else:
                        return ["SB", "beq", "no_hay_salto"]
                    
                elif inst[1] == "bne":
                    if RegFile[inst[2]] != RegFile[inst[3]]:
                        return ["SB", "bne", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bne", "no_hay_salto"]
                
                elif inst[1] == "blt":
                    if RegFile[inst[2]] < RegFile[inst[3]]:
                        return ["SB", "blt", etiquetas[inst[4]]]
                    else:
                        return ["SB", "blt", "no_hay_salto"]
                
                elif inst[1] == "bge":
                    if RegFile[inst[2]] >= RegFile[inst[3]]:
                        return ["SB", "bge", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bge", "no_hay_salto"]
                
                elif inst[1] == "bltu":
                    if RegFile[inst[2]] < RegFile[inst[3]]:
                        return ["SB", "bltu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bltu", "no_hay_salto"]
                
                elif inst[1] == "bgeu":
                    if RegFile[inst[2]] >= RegFile[inst[3]]:
                        return ["SB", "bgeu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bgeu", "no_hay_salto"]
                    
                else:
                    return "ERROR"
                
            #Agregar para el tipo UJ  
            elif inst[0] == "UJ":
                if inst[1] == "jal":
                    return ["UJ", inst[1], inst[2], inst[3]]
                else:
                    return "ERROR"
        if aux==1:
            if inst[0] == "R":
                if inst[1] == "add":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sub":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] - RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sll":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] << RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "slt":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] < RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sltu":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])]< RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "xor":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] ^ RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "srl":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] >> RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sra":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] >> RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "or":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] | RegFile[inst[4]]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "and":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] & RegFile[inst[4]]
                    return ["R", inst[1], inst[2],RegsForwarding[str(inst[2])]]
                else:
                    return "ERROR"
                
            elif inst[0] == "I":
                if inst[1] == "lb":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "lh":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "lw":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "lbu":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "lhu":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "slli":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] << inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "srli":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] >> inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "srai":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] >> inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "addi":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "slti":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] < inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sltiu":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] < inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "xori":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] ^ inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "ori":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] | inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "andi":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] & inst[4]
                    return ["I", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                else:
                    return "ERROR"
                
            elif inst[0] == "S": #Ver bien los registros de los stores
                if inst[1] == "sb":
                    return ["S", inst[1], RegsForwarding[str(inst[3])], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "sh":
                    return ["S", inst[1], RegsForwarding[str(inst[3])], RegFile[inst[3]] + inst[4]]
                elif inst[1] == "sw":
                    print("TIPO 1")
                    return ["S", inst[1], RegsForwarding[str(inst[2])], RegFile[inst[3]]  + inst[4]] 
                else:
                    return "ERROR"
        #Agregando instrucciones para branches     
            elif inst[0] == "SB":
                if inst[1] == "beq":
                    if RegsForwarding[str(inst[2])] == RegFile[inst[3]]:
                        return ["SB", "beq", etiquetas[inst[4]]]
                    else:
                        return ["SB", "beq", "no_hay_salto"]
                    
                elif inst[1] == "bne":
                    if RegsForwarding[str(inst[2])]  != RegFile[inst[3]]:
                        return ["SB", "bne", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bne", "no_hay_salto"]
                
                elif inst[1] == "blt":
                    if RegsForwarding[str(inst[2])]  < RegFile[inst[3]]:
                        return ["SB", "blt", etiquetas[inst[4]]]
                    else:
                        return ["SB", "blt", "no_hay_salto"]
                    
                elif inst[1] == "bge":
                    if RegsForwarding[str(inst[2])] >= RegFile[inst[3]]:
                        return ["SB", "bge", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bge", "no_hay_salto"]
                
                elif inst[1] == "bltu":
                    if RegsForwarding[str(inst[2])] < RegFile[inst[3]]:
                        return ["SB", "bltu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bltu", "no_hay_salto"]
                
                elif inst[1] == "bgeu":
                    if RegsForwarding[str(inst[2])]  >= RegFile[inst[3]]:
                        return ["SB", "bgeu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bgeu", "no_hay_salto"]
                    
                else:
                    return "ERROR"
                
            #Agregar para el tipo UJ  
            elif inst[0] == "UJ":
                if inst[1] == "jal":
                    return ["UJ", inst[1], inst[2], inst[3]]
                else:
                    return "ERROR"
        if aux==2:
            if inst[0] == "R":
                if inst[1] == "add":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] + RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sub":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] - RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sll":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] << RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "slt":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] < RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sltu":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] < RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "xor":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] ^ RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "srl":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] >> RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sra":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] >> RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "or":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] | RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "and":
                    RegsForwarding[str(inst[2])]= RegFile[inst[3]] & RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                else:
                    return "ERROR"
                
            
                
            elif inst[0] == "S":
                if inst[1] == "sb":
                    return ["S", inst[1], RegFile[inst[2]], RegsForwarding[str(inst[3])] + inst[4]]
                elif inst[1] == "sh":
                    return ["S", inst[1], RegFile[inst[2]], RegsForwarding[str(inst[3])] + inst[4]]
                elif inst[1] == "sw":
                    print("TIPO 2")
                    return ["S", inst[1], RegFile[inst[2]], RegsForwarding[str(inst[3])] + inst[4]]
                else:
                    return "ERROR"
        #Agregando instrucciones para branches     
            elif inst[0] == "SB":
                if inst[1] == "beq":
                    if RegFile[inst[2]] == RegsForwarding[str(inst[3])] :
                        return ["SB", "beq", etiquetas[inst[4]]]
                    else:
                        return ["SB", "beq", "no_hay_salto"]
                    
                elif inst[1] == "bne":
                    if RegFile[inst[2]] != RegsForwarding[str(inst[3])]:
                        return ["SB", "bne", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bne", "no_hay_salto"]
                
                elif inst[1] == "blt":
                    if RegFile[inst[2]] < RegsForwarding[str(inst[3])]:
                        return ["SB", "blt", etiquetas[inst[4]]]
                    else:
                        return ["SB", "blt", "no_hay_salto"]
                
                elif inst[1] == "bge":
                    if RegFile[inst[2]] >= RegsForwarding[str(inst[3])]:
                        return ["SB", "bge", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bge", "no_hay_salto"]
                
                elif inst[1] == "bltu":
                    if RegFile[inst[2]] < RegsForwarding[str(inst[3])]:
                        return ["SB", "bltu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bltu", "no_hay_salto"]
                
                elif inst[1] == "bgeu":
                    if RegFile[inst[2]] >= RegsForwarding[str(inst[3])]:
                        return ["SB", "bgeu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bgeu", "no_hay_salto"]
                    
                else:
                    return "ERROR"
                
            #Agregar para el tipo UJ  
            elif inst[0] == "UJ":
                if inst[1] == "jal":
                    return ["UJ", inst[1], inst[2], inst[3]]
                else:
                    return "ERROR"
        if aux==3:
            if inst[0] == "R":
                if inst[1] == "add":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] + RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sub":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] - RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sll":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] << RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "slt":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] < RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sltu":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] < RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "xor":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] ^ RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "srl":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] >> RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "sra":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] >> RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "or":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] | RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                elif inst[1] == "and":
                    RegsForwarding[str(inst[2])]= RegsForwarding[str(inst[3])] & RegsForwarding[str(inst[4])]
                    return ["R", inst[1], inst[2], RegsForwarding[str(inst[2])]]
                else:
                    return "ERROR"
                
                
            elif inst[0] == "S":
                if inst[1] == "sb":
                    return ["S", inst[1], RegsForwarding[str(inst[2])], RegsForwarding[str(inst[3])] + inst[4]]
                elif inst[1] == "sh":
                    return ["S", inst[1], RegsForwarding[str(inst[2])], RegsForwarding[str(inst[3])] + inst[4]]
                elif inst[1] == "sw":
                    print("TIPO 3")
                    return ["S", inst[1], RegsForwarding[str(inst[2])], RegsForwarding[str(inst[3])] + inst[4]]
                else:
                    return "ERROR"
        #Agregando instrucciones para branches     
            elif inst[0] == "SB":
                if inst[1] == "beq":
                    if RegsForwarding[str(inst[2])] == RegsForwarding[str(inst[3])]:
                        return ["SB", "beq", etiquetas[inst[4]]]
                    else:
                        return ["SB", "beq", "no_hay_salto"]
                    
                elif inst[1] == "bne":
                    if RegsForwarding[str(inst[2])] != RegsForwarding[str(inst[3])]:
                        return ["SB", "bne", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bne", "no_hay_salto"]
                
                elif inst[1] == "blt":
                    if RegsForwarding[str(inst[2])] < RegsForwarding[str(inst[3])]:
                        return ["SB", "blt", etiquetas[inst[4]]]
                    else:
                        return ["SB", "blt", "no_hay_salto"]
                
                elif inst[1] == "bge":
                    if RegsForwarding[str(inst[2])] >= RegsForwarding[str(inst[3])]:
                        return ["SB", "bge", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bge", "no_hay_salto"]
                
                elif inst[1] == "bltu":
                    if RegsForwarding[str(inst[2])] < RegsForwarding[str(inst[3])]:
                        return ["SB", "bltu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bltu", "no_hay_salto"]
                
                elif inst[1] == "bgeu":
                    if RegsForwarding[str(inst[2])] >= RegsForwarding[str(inst[3])]:
                        return ["SB", "bgeu", etiquetas[inst[4]]]
                    else:
                        return ["SB", "bgeu", "no_hay_salto"]
                    
                else:
                    return "ERROR"
                
            #Agregar para el tipo UJ  
            elif inst[0] == "UJ":
                if inst[1] == "jal":
                    return ["UJ", inst[1], inst[2], inst[3]]
                else:
                    return "ERROR"

#Fase de guardado en memoria  

#Este código define una función llamada memory que toma un parámetro inst. La función utiliza una variable global llamada ram, que probablemente representa la memoria RAM del sistema.
#La función realiza lo siguiente:

#Si el primer carácter de inst es "X", devuelve una lista con dos elementos "X" y "X".
#Si el primer carácter de inst es "R", devuelve una lista con cuatro elementos "R", el segundo, tercer y cuarto elemento de inst.
#Si el primer carácter de inst es "I", devuelve una lista con cinco elementos "I", el segundo, tercer y cuarto elemento de inst, y el valor almacenado en la posición de memoria especificada por el cuarto elemento de inst.
#Si el primer carácter de inst es "S", almacena el segundo elemento de inst en la posición de memoria especificada por el cuarto elemento de inst, y devuelve una lista con dos elementos "S" y el segundo elemento de inst.
def memory(inst):
    global ram 
    if inst[0] == "X":
        return ["X","X"]

    else:
        if inst[0] == "R":
            return ["R", inst[1], inst[2], inst[3]]
        
        elif inst[0] == "I":
            if inst[1] in ["lb", "lh", "lw", "lbu", "lhu"]:
                return ["I", inst[1], inst[2], inst[3], ram[inst[3]]]
            else:
                return ["I", inst[1], inst[2], inst[3], inst[3]]    
        
        elif inst[0] == "S":    
            ram[inst[3]] = inst[2]
            return ["S", inst[1]]
        
        elif inst[0] == "SB":
            return ["SB", inst[1], inst[2]]
            
        
        elif inst[0] == "UJ":
            return ["UJ", inst[1], inst[2], inst[3]]
        else:
            return "ERROR"

#Fase de escritura toma un parámetro inst. La función utiliza una variable global llamada RegFile, que probablemente representa el archivo de registros del sistema.
#La función realiza lo siguiente:

#Si el primer carácter de inst es "X", devuelve una lista con dos elementos "X" y "X".
#Si el primer carácter de inst es "R", almacena el valor del cuarto elemento de inst en el registro especificado por el tercer elemento de inst, actualizando el valor en el RegFile, y devuelve una lista con el segundo elemento de inst.
#Si el primer carácter de inst es "I", verifica si el segundo elemento de inst es una de las siguientes operaciones de carga de memoria ("lb", "lh", "lw", "lbu", "lhu"), en cuyo caso almacena el valor del quinto elemento de inst en el registro especificado por el tercer elemento de inst, actualizando el valor en el RegFile, y devuelve una lista con el segundo elemento de inst. En caso contrario, almacena el valor del cuarto elemento de inst en el registro especificado por el tercer elemento de inst, actualizando el valor en el RegFile, y devuelve una lista con el segundo elemento de inst.
#Si el primer carácter de inst es "S", devuelve una lista con el segundo elemento de inst.
def writeBack(inst):
    global RegFile 
    if inst[0] == "X":
        return ["X",0]

    else:
        if inst[0] == "R":
            RegFile[inst[2]] = inst[3]
            return [inst[1],1]
        
        elif inst[0] == "I":
            if inst[1] in ["lb", "lh", "lw", "lbu", "lhu"]:
                RegFile[inst[2]] = inst[4]
                return [inst[1],1]
            else:
                RegFile[inst[2]] = inst[3]
                return [inst[1],1]
            
        elif inst[0] == "S":
            return [inst[1],1]
        elif inst[0] == "SB":
            return [inst[1],1,inst[2]]
        elif inst[0] == "UJ":
            return [inst[1],1]
        # al igual que con la instrucción S y SB, la instrucción UJ no modifica ningún registro en el RegFile, por lo que su writeback solo retorna el número de la instrucción.
        else:
            return "ERROR"
        

# 0 = no hay dependencias
# 1 = dependencia en el primer registro
# 2 = dependencia en el segundo registro
# 3 = dependencia en ambos registros
def forwarding(inst): 
    global reg_EnUso

    if len(reg_EnUso) >= 5:
        reg_EnUso.pop(-1)

    else:
        pass
    
    if inst[0] == "X":
        reg_EnUso.insert(0, "X")
        print("(ง ͠° ͟ʖ ͡°)ง")
        return 0

    else:
        if inst[0] in tipo_R:
            if (inst[1].replace("x","")).replace(",","") in reg_EnUso:
                
                print("El registro destino tiene dependencias")
                if (inst[2].replace("x","")).replace(",","") in reg_EnUso and (inst[3].replace("x","")).replace(",","") not in reg_EnUso:
                    print("Solo el primer registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 1

                elif (inst[2].replace("x","")).replace(",","") not in reg_EnUso and (inst[3].replace("x","")).replace(",","") in reg_EnUso:
                    print("Solo el segundo registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 2
                
                elif (inst[2].replace("x","")).replace(",","") in reg_EnUso and (inst[3].replace("x","")).replace(",","") in reg_EnUso:
                    print("Ambos registros tienen dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 3
                    
                else:
                    print("Ningun registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 0

            else:
                
                print("El registro destino no tiene dependencias")
                if (inst[2].replace("x","")).replace(",","") in reg_EnUso and (inst[3].replace("x","")).replace(",","") not in reg_EnUso:
                    print("Solo el primer registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 1

                elif (inst[2].replace("x","")).replace(",","") not in reg_EnUso and (inst[3].replace("x","")).replace(",","") in reg_EnUso:
                    print("Solo el segundo registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 2
                
                elif (inst[2].replace("x","")).replace(",","") in reg_EnUso and (inst[3].replace("x","")).replace(",","") in reg_EnUso:
                    print("Ambos registros tienen dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 3
                    
                else:
                    print("Ningun registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 0

        elif inst[0] in tipo_I:
            if (inst[1].replace("x","")).replace(",","") in reg_EnUso:
                
                print("El registro destino tiene dependencias")
                if (inst[2].replace("x","")).replace(",","") in reg_EnUso:
                    print("Solo el primer registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 1
                
                else:
                    print("Ningun registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 0

            else:
                
                print("El registro destino no tiene dependencias")
                if (inst[2].replace("x","")).replace(",","") in reg_EnUso:
                    print("Solo el primer registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 1
                
                else:
                    print("Ningun registro tiene dependencias")
                    reg_EnUso.insert(0, (inst[1].replace("x","")).replace(",",""))
                    return 0
        
        elif inst[0] in tipo_S: 
            if (inst[1].replace("x","")).replace(",","") in reg_EnUso and (inst[2].replace("x","")).replace(",","") not in reg_EnUso:
                    print("Solo el primer registro tiene dependencias")
                    return 1

            elif (inst[1].replace("x","")).replace(",","") not in reg_EnUso and (inst[2].replace("x","")).replace(",","") in reg_EnUso:
                    print("Solo el segundo registro tiene dependencias")
                    return 2
                
            elif (inst[1].replace("x","")).replace(",","") in reg_EnUso and (inst[2].replace("x","")).replace(",","") in reg_EnUso:
                    print("Ambos registros tienen dependencias")
                    return 3
                    
            else:
                    print("Ningun registro tiene dependencias")
                    return 0


        elif inst[0] in tipo_SB: 
            if (inst[1].replace("x","")).replace(",","") in reg_EnUso and (inst[2].replace("x","")).replace(",","") not in reg_EnUso:
                    print("Solo el primer registro tiene dependencias")
                    return 1

            elif (inst[1].replace("x","")).replace(",","") not in reg_EnUso and (inst[3].replace("x","")).replace(",","") in reg_EnUso:
                    print("Solo el segundo registro tiene dependencias")
                    return 2
                
            elif (inst[1].replace("x","")).replace(",","") in reg_EnUso and (inst[2].replace("x","")).replace(",","") in reg_EnUso:
                    print("Ambos registros tienen dependencias")
                    return 3
                    
            else:
                    print("Ningun registro tiene dependencias")
                    return 0

        elif inst[0] in tipo_UJ:
            return 0

        else:
            reg_EnUso.insert(0, "X")

def Branch_Predictor(estado):
    if estado == "00": #Weakly taken
      print("Weakly taken")
      return 1
    
    elif estado == "01": #Strongly taken
      print("Strongly taken")
      return 1
    
    elif estado == "10": #Weakly not taken
      print("Weakly not taken")
      return 0
    
    elif estado == "11": #Strongly not taken
      print("Strongly not taken")
      return 0
    
    else:
      print("Error")
      pass

def State_machine(estado, salto):
   if estado == "00": #Weakly taken
      if salto == 1:
         return "01"
      else:
         return "10"

   elif estado == "01": #Strongly taken
      if salto == 1:
         return "01"
      else:
         return "00"

   elif estado == "10": #Weakly not taken
      if salto == 1:
         return "00"
      else:
         return "11"

   elif estado == "11": #Strongly not taken
      if salto == 1:
         return "10"
      else:
         return "10"

#Mode
#0: Sin forwarding y sin prediccion de saltos
#1: Con forwarding y sin prediccion de saltos
#2: Sin forwarding y con prediccion de saltos
#3: Con forwarding y con prediccion de saltos





#______________MAIN__________________
#abrimos el archivo de texto donde están contenidas las funciones en ensamblador
#PruebaMatriz4x4.S
#PruebaMultRusa.S
#PruebaFibonacci.S
#PruebaFactorial.S


file = open("PruebaFactorial.S", "r")
#Guardamos linea a linea lo del txt en una matriz llamada instruciones la linea 0 va a la posicion 0 de la matriz y asi sucesivamente
instrucciones.extend(file.readlines())
file.close()

etiquetas = {}


#Lee todo el archivo en busca de etiquetas y las guarda en un diccionario con el formato etiqueta:numero de instruccion
for i in range(len(instrucciones)-1):
    if ':' in instrucciones[i].split()[0]:
        etiquetas[(instrucciones[i].split()[0]).replace(":", "")] = i

num_inst = int(0)
i = int(0)
ii = int(0)
j = int(0)
aux = int(0)
aux2 = int(0)
aux3 = int(0)
prediccion = int(0)
prediccion2 = int(0)
revisar = int(0)
wo = []
lista_aux3 = [int(0), int(0)]
conteosal = 0
conteosal2= 0



##################################################### Menu ##################################################################################
print("###################Menu Principal###################")
print("Presione 1 para ver Ejecución sin forwarding ni Predicción de saltos")
print("Presione 2 para ver Ejecución con forwarding sin Predicción de saltos")
print("Presione 3 para ver Ejecución sin forwarding y con Predicción de saltos")
print("Presione 4 para ver Ejecución con forwarding y con Predicción de saltos")
entrada = int(input("Seleccione una opcion: "))

while True:

    if  entrada not in range(1,5):
        print("Opción inválida, volviendo al menú principal \n\n")
        print("###################Menu Principal###################")
        print("Presione 1 para ver Ejecución sin forwarding ni Predicción de saltos")
        print("Presione 2 para ver Ejecución con forwarding sin Predicción de saltos")
        print("Presione 3 para ver Ejecución sin forwarding y con Predicción de saltos")
        print("Presione 4 para ver Ejecución con forwarding y con Predicción de saltos")
        print(entrada)
        entrada = int(input("Seleccione una opcion: "))

    if entrada == 1:
        input()
        print("\n"*50)

        if i == len(instrucciones):
            instrucciones.append ("X X X")
        
        print("Len Inst: ", len(instrucciones))
        print("Etiquetas: ", etiquetas)
        print("Dependencias: ", reg_EnUso)
        print("Forwarding: ", RegsForwarding)
    
        if (reg_WB_FIN[1]==1):
            print("Se ha completado una instruccion ")
            aux = num_inst 
            num_inst = num_inst + 1

        #------------------------------------------
        reg_WB_FIN = writeBack(reg_MEM_WB)
        reg_MEM_WB = memory(reg_EX_MEM)
        reg_EX_MEM = execute(reg_ID_EX, aux2)
        if lista_aux3[-2] == 0:
            aux2 = forwarding(reg_IF_ID)
        else:
            aux2 = forwarding(["X", "X", "X"])
        lista_aux3.append(aux2)
        

        if lista_aux3[-2] == 0:
            print("TODO NORMAL", lista_aux3[-2])
            reg_ID_EX, aux3 = decode(reg_IF_ID, aux2)
            reg_IF_ID = fetch(instrucciones,i)
        
        else:
            print("STALLS", lista_aux3[-2])
            reg_EX_MEM = ["X","X"]
            print()
            wo, aux3 = decode(reg_IF_ID, aux2)

            reg_EnUso.insert(0, "X")
            if len(reg_EnUso) >= 5:
                reg_EnUso.pop(-1)

            else:
                pass
        #------------------------------------------
        print("RegFile: ", RegFile)
        print("RAM: ", ram)
        print("IF/ID: ", reg_IF_ID)
        print("ID/EX: ", reg_ID_EX, aux2)
        print("EX/MEM: ", reg_EX_MEM)
        print("MEM/WB: ", reg_MEM_WB)
        print("WB/FIN: ", reg_WB_FIN)
        print("Program Counter: ", i)
        print("numero de ciclos:", j)
        print("numero de instrucciones:", num_inst)
        
        if reg_IF_ID[0] in tipo_UJ:
            i = int(etiquetas[reg_IF_ID[2]])
            print("Jump", i)

        if reg_EX_MEM[1] in tipo_SB:
            if reg_EX_MEM[2] != "no_hay_salto":
                print("FLUSH!!!!!!!!")
                i = reg_EX_MEM[2]
                reg_IF_ID = ["X", "X", "X"]
                reg_ID_EX = ["X", "X", "X"]
            elif lista_aux3[-2] != 0:
                i = i
            else:
                i += 1
        elif lista_aux3[-2] != 0:
            i = i
        else:
            if reg_IF_ID[0] in tipo_UJ:
                i = i
            else:
                i = i + int(1)  

        if (num_inst != 0):
            CPI = j/num_inst
            print("CPI:",CPI)

        print("╔════════════╦════════════╦════════════╦════════════╦════════════╗")
        print("║   FETCHS   ║   DECODE   ║  EXECUTES  ║   MEMORY   ║ WRITE BACK ║") #12 espacios
        print("╠════════════╬════════════╬════════════╬════════════╬════════════╣")
        print("║", " "*((8-len(reg_IF_ID [0]))//2),reg_IF_ID [0]," "*((8-len(reg_IF_ID [0]))//2 + (8-len(reg_IF_ID [0]))%2), "║",
                " "*((8-len(reg_ID_EX [1]))//2),reg_ID_EX [1]," "*((8-len(reg_ID_EX [1]))//2 + (8-len(reg_ID_EX [1]))%2), "║",
                " "*((8-len(reg_EX_MEM[1]))//2),reg_EX_MEM[1]," "*((8-len(reg_EX_MEM[1]))//2 + (8-len(reg_EX_MEM[1]))%2), "║",
                " "*((8-len(reg_MEM_WB[1]))//2),reg_MEM_WB[1]," "*((8-len(reg_MEM_WB[1]))//2 + (8-len(reg_MEM_WB[1]))%2), "║", 
                " "*((8-len(reg_WB_FIN[0]))//2),reg_WB_FIN[0]," "*((8-len(reg_WB_FIN[0]))//2 + (8-len(reg_WB_FIN[0]))%2), "║")
        print("╚════════════╩════════════╩════════════╩════════════╩════════════╝")

        j += 1
        if reg_IF_ID[0] == "X" and reg_ID_EX[0] == "X" and reg_EX_MEM[0] == "X" and reg_MEM_WB[0] == "X" and reg_WB_FIN[0] == "X":      
            print("Fin de la ejecucion")

            print("Presione 7 para salir al menu")
            entrada_aux = input("Ingrese una opcion: ")
            if int(entrada_aux) == 7:
                i=0
                j=0
                num_inst=0
                print("###################Menu Principal###################")
                print("Presione 1 para ver Ejecución sin forwarding ni Predicción de saltos")
                print("Presione 2 para ver Ejecución con forwarding sin Predicción de saltos")
                print("Presione 3 para ver Ejecución sin forwarding y con Predicción de saltos")
                print("Presione 4 para ver Ejecución con forwarding y con Predicción de saltos")
                entrada = int(input("Seleccione una opcion: "))
            else:  
                print("Opción inválida")
            
    if entrada == 2:
        input()
        print("\n"*50)

        if i == len(instrucciones):
            instrucciones.append ("X X X")
        
        print("Len Inst: ", len(instrucciones))
        print("Etiquetas: ", etiquetas)
        print("Dependencias: ", reg_EnUso)
        print("Forwarding: ", RegsForwarding)
    
        if (reg_WB_FIN[1]==1):
            print("Se ha completado una instruccion ")
            aux = num_inst 
            num_inst = num_inst + 1

        #---------------Con-Frowarding-Sin-prediccion--------------------------- 
        reg_WB_FIN = writeBack(reg_MEM_WB)
        reg_MEM_WB = memory(reg_EX_MEM)
        reg_EX_MEM = execute(reg_ID_EX, aux2)
        reg_ID_EX, aux3  = decode(reg_IF_ID, aux2)
        if lista_aux3[-2] == 0:
            aux2 = forwarding(reg_IF_ID)
        else:
            aux2 = forwarding(["X", "X", "X"])
        reg_IF_ID = fetch(instrucciones,i)
        #-----------------------------------------------------------------------

        print("RegFile: ", RegFile)
        print("RAM: ", ram)
        print("IF/ID: ", reg_IF_ID)
        print("ID/EX: ", reg_ID_EX, aux2)
        print("EX/MEM: ", reg_EX_MEM)
        print("MEM/WB: ", reg_MEM_WB)
        print("WB/FIN: ", reg_WB_FIN)
        print("Program Counter: ", i)
        print("numero de ciclos:", j)
        print("numero de instrucciones:", num_inst)

        if reg_IF_ID[0] in tipo_UJ:
            i = int(etiquetas[reg_IF_ID[2]])
            print("Jump", i)

        if reg_EX_MEM[1] in tipo_SB:
            if reg_EX_MEM[2] != "no_hay_salto":
                print("FLUSH!!!!!!!!")
                i = reg_EX_MEM[2]
                reg_IF_ID = ["X", "X", "X"]
                reg_ID_EX = ["X", "X", "X"]
            elif lista_aux3[-2] != 0:
                i = i
            else:
                i += 1
        elif lista_aux3[-2] != 0:
            i = i
        else:
            if reg_IF_ID[0] in tipo_UJ:
                i = i
            else:
                i = i + int(1)  

        if (num_inst != 0):
            CPI = j/num_inst
            print("CPI:",CPI)

        print("╔════════════╦════════════╦════════════╦════════════╦════════════╗")
        print("║   FETCHS   ║   DECODE   ║  EXECUTES  ║   MEMORY   ║ WRITE BACK ║") #12 espacios
        print("╠════════════╬════════════╬════════════╬════════════╬════════════╣")
        print("║", " "*((8-len(reg_IF_ID [0]))//2),reg_IF_ID [0]," "*((8-len(reg_IF_ID [0]))//2 + (8-len(reg_IF_ID [0]))%2), "║",
                " "*((8-len(reg_ID_EX [1]))//2),reg_ID_EX [1]," "*((8-len(reg_ID_EX [1]))//2 + (8-len(reg_ID_EX [1]))%2), "║",
                " "*((8-len(reg_EX_MEM[1]))//2),reg_EX_MEM[1]," "*((8-len(reg_EX_MEM[1]))//2 + (8-len(reg_EX_MEM[1]))%2), "║",
                " "*((8-len(reg_MEM_WB[1]))//2),reg_MEM_WB[1]," "*((8-len(reg_MEM_WB[1]))//2 + (8-len(reg_MEM_WB[1]))%2), "║", 
                " "*((8-len(reg_WB_FIN[0]))//2),reg_WB_FIN[0]," "*((8-len(reg_WB_FIN[0]))//2 + (8-len(reg_WB_FIN[0]))%2), "║")
        print("╚════════════╩════════════╩════════════╩════════════╩════════════╝")

        j += 1
        if reg_IF_ID[0] == "X" and reg_ID_EX[0] == "X" and reg_EX_MEM[0] == "X" and reg_MEM_WB[0] == "X" and reg_WB_FIN[0] == "X":      
            print("Fin de la ejecucion")
            print("Presione 7 para salir al menu")
            entrada_aux = int(input("Ingrese una opcion: "))
            if entrada_aux == 7:
                i=0
                j=0
                num_inst=0
                print("###################Menu Principal###################")
                print("Presione 1 para ver Ejecución sin forwarding ni Predicción de saltos")
                print("Presione 2 para ver Ejecución con forwarding sin Predicción de saltos")
                print("Presione 3 para ver Ejecución sin forwarding y con Predicción de saltos")
                print("Presione 4 para ver Ejecución con forwarding y con Predicción de saltos")
                entrada = int(input("Seleccione una opcion: "))
            else:
                print("Opción inválida")

    elif entrada == 3:
        input()
        print("\n"*50)

        if i == len(instrucciones):
            instrucciones.append ("X X X")
        
        print("Len Inst: ", len(instrucciones))
        print("Etiquetas: ", etiquetas)
        print("Dependencias: ", reg_EnUso)
        print("Direcciones de salto: ", Dir_Prediccion)
        print("Forwarding: ", RegsForwarding)
    
        if (reg_WB_FIN[1]==1):
            print("Se ha completado una instruccion ")
            aux = num_inst 
            num_inst = num_inst + 1
        
    #--------------------Logica-Sin-Forwarding-Con-Prediccion---------------------   
        reg_WB_FIN = writeBack(reg_MEM_WB)
        reg_MEM_WB = memory(reg_EX_MEM)
        reg_EX_MEM = execute(reg_ID_EX, aux2)
        if lista_aux3[-2] == 0:
            aux2 = forwarding(reg_IF_ID)
        else:
            aux2 = forwarding(["X", "X", "X"])

        lista_aux3.append(aux2)

        if lista_aux3[-2] == 0:
            print("TODO NORMAL", lista_aux3[-2])
            reg_ID_EX, aux3 = decode(reg_IF_ID, aux2)
            reg_IF_ID = fetch(instrucciones,i)
        
        else:
            print("STALLS", lista_aux3[-2])
            reg_EX_MEM = ["X","X"]
            wo, aux3 = decode(reg_IF_ID, aux2)

            reg_EnUso.insert(0, "X")
            if len(reg_EnUso) >= 5:
                reg_EnUso.pop(-1)

            else:
                pass

        if reg_IF_ID[0] in tipo_SB:
            if i not in Dir_Prediccion:
                Dir_Prediccion[i] = [reg_IF_ID[3],"10"]
            else:
                pass
        else:
            if i in Dir_Prediccion:
                Dir_Prediccion.pop(i)
   
        

        
        print("RegFile: ", RegFile)
        print("RAM: ", ram)
        print("IF/ID: ", reg_IF_ID)
        print("ID/EX: ", reg_ID_EX, aux2)
        print("EX/MEM: ", reg_EX_MEM)
        print("MEM/WB: ", reg_MEM_WB)
        print("WB/FIN: ", reg_WB_FIN)
        print("Program Counter: ", i)
        print("numero de ciclos:", j)
        print("numero de instrucciones:", num_inst)

    #--------------------PC-Con/Sin-Forwarding-Con-Prediccion---------------------   
        if reg_IF_ID[0] in tipo_SB and lista_aux3[-2] == 0:
            prediccion = Branch_Predictor(Dir_Prediccion[i][1])
            if prediccion == 1:
                ii = i
                i = int(etiquetas[Dir_Prediccion[i][0]]) - int(1)
            else:
                ii = i
                i = i
            

        if reg_IF_ID[0] in tipo_UJ:
            i = int(etiquetas[reg_IF_ID[2]])
            print("Jump", i)

        if reg_EX_MEM[1] in tipo_SB:
            print("BUENas")
            if lista_aux3[-2] != 0:
                i = i

            elif reg_EX_MEM[2] != "no_hay_salto":
                Dir_Prediccion[ii][1] = State_machine(Dir_Prediccion[ii][1], 1)
                if prediccion == 1:
                    print("Prediccion CORRECTA 1")
                    conteosal = conteosal + 1
                    if reg_IF_ID[0] in tipo_UJ:
                        i = i    
                    else:
                        i = i + int(1) 

                else:
                    print("Prediccion INCORRECTA 1")
                    conteosal2 = conteosal2 + 1
                    print("FLUSH!!!!!!!!")
                    reg_EnUso[0] = "X"
                    reg_EnUso[1] = "X"
                    i = reg_EX_MEM[2]
                    reg_IF_ID = ["X", "X", "X"]
                    reg_ID_EX = ["X", "X", "X"]
                    

            elif reg_EX_MEM[2] == "no_hay_salto":
                Dir_Prediccion[ii][1] = State_machine(Dir_Prediccion[ii][1], 0)
                if prediccion == 0:
                    print("Prediccion CORRECTA 2")
                    conteosal = conteosal + 1
                    i = i + int(1)
                else:
                    print("Prediccion INCORRECTA 2")
                    conteosal2 = conteosal2 + 1
                    print("FLUSH!!!!!!!!")
                    reg_EnUso[0] = "X"
                    reg_EnUso[1] = "X"
                    i = ii + 1 
                    reg_IF_ID = ["X", "X", "X"]
                    reg_ID_EX = ["X", "X", "X"]
                    
            
            else:
                i = i + int(1)
        elif lista_aux3[-2] != 0:
            i = i
        else:
            if reg_IF_ID[0] in tipo_UJ:
                i = i    
            else:
                i = i + int(1) 
    #------------------------------------------ 
        conteototalsal = conteosal + conteosal2
        print("CONTEOTOTAL",conteototalsal)
        if conteototalsal != 0:
            PA=(conteosal*100)/conteototalsal # Porcentaje de aciertos
            print("Numero de predicciones: ", conteototalsal)
            print("Porcentaje de aciertos: ",PA)

        if (num_inst != 0):
            CPI = j/num_inst
            print("CPI:",CPI)

        print("╔════════════╦════════════╦════════════╦════════════╦════════════╗")
        print("║   FETCHS   ║   DECODE   ║  EXECUTES  ║   MEMORY   ║ WRITE BACK ║") #12 espacios
        print("╠════════════╬════════════╬════════════╬════════════╬════════════╣")
        print("║", " "*((8-len(reg_IF_ID [0]))//2),reg_IF_ID [0]," "*((8-len(reg_IF_ID [0]))//2 + (8-len(reg_IF_ID [0]))%2), "║",
                " "*((8-len(reg_ID_EX [1]))//2),reg_ID_EX [1]," "*((8-len(reg_ID_EX [1]))//2 + (8-len(reg_ID_EX [1]))%2), "║",
                " "*((8-len(reg_EX_MEM[1]))//2),reg_EX_MEM[1]," "*((8-len(reg_EX_MEM[1]))//2 + (8-len(reg_EX_MEM[1]))%2), "║",
                " "*((8-len(reg_MEM_WB[1]))//2),reg_MEM_WB[1]," "*((8-len(reg_MEM_WB[1]))//2 + (8-len(reg_MEM_WB[1]))%2), "║", 
                " "*((8-len(reg_WB_FIN[0]))//2),reg_WB_FIN[0]," "*((8-len(reg_WB_FIN[0]))//2 + (8-len(reg_WB_FIN[0]))%2), "║")
        print("╚════════════╩════════════╩════════════╩════════════╩════════════╝")

        j += 1

        print("Ultimo i: ", i)

        if reg_IF_ID[0] == "X" and reg_ID_EX[0] == "X" and reg_EX_MEM[0] == "X" and reg_MEM_WB[0] == "X" and reg_WB_FIN[0] == "X":      
            print("Fin de la ejecucion")
            print("Presione 7 para salir al menu")
            entrada_aux = int(input("Ingrese una opcion: "))
            if entrada_aux == 7:
                i=0
                j=0
                num_inst=0
                PA = 0
                conteosal = 0 
                conteosal2 = 0
                print("###################Menu Principal###################")
                print("Presione 1 para ver Ejecución sin forwarding ni Predicción de saltos")
                print("Presione 2 para ver Ejecución con forwarding sin Predicción de saltos")
                print("Presione 3 para ver Ejecución sin forwarding y con Predicción de saltos")
                print("Presione 4 para ver Ejecución con forwarding y con Predicción de saltos")
                entrada = int(input("Seleccione una opcion: "))
            else:
                print("Opción inválida")
                  
    elif entrada == 4:
        
        input()
        print("\n"*50)
        if i == len(instrucciones):
            instrucciones.append ("X X X")
        
        print("Len Inst: ", len(instrucciones))
        print("Etiquetas: ", etiquetas)
        print("Dependencias: ", reg_EnUso)
        print("Direcciones de salto: ", Dir_Prediccion)
        print("Forwarding: ", RegsForwarding)
    
        if (reg_WB_FIN[1]==1):
            print("Se ha completado una instruccion ")
            aux = num_inst 
            num_inst = num_inst + 1
        
     

        #---------------Con-Frowarding-Con-Prediccion--------------------------- 
        reg_WB_FIN = writeBack(reg_MEM_WB)
        reg_MEM_WB = memory(reg_EX_MEM)
        reg_EX_MEM = execute(reg_ID_EX, aux2)
        reg_ID_EX, aux3  = decode(reg_IF_ID, aux2)
        if lista_aux3[-2] == 0:
            aux2 = forwarding(reg_IF_ID)
        else:
            aux2 = forwarding(["X", "X", "X"])
        reg_IF_ID = fetch(instrucciones,i)

        if reg_IF_ID[0] in tipo_SB:
            if i not in Dir_Prediccion:
                Dir_Prediccion[i] = [reg_IF_ID[3],"10"]
            else:
                pass
        else:
            if i in Dir_Prediccion:
                Dir_Prediccion.pop(i)
        #-----------------------------------------------------------------------
        

        
        print("RegFile: ", RegFile)
        print("RAM: ", ram)
        print("IF/ID: ", reg_IF_ID)
        print("ID/EX: ", reg_ID_EX, aux2)
        print("EX/MEM: ", reg_EX_MEM)
        print("MEM/WB: ", reg_MEM_WB)
        print("WB/FIN: ", reg_WB_FIN)
        print("Program Counter: ", i)
        print("numero de ciclos:", j)
        print("numero de instrucciones:", num_inst)


    #--------------------PC-Con/Sin-Forwarding-Con-Prediccion---------------------   
        if reg_IF_ID[0] in tipo_SB and lista_aux3[-2] == 0:
            if reg_IF_ID[0] in tipo_SB and reg_EX_MEM[1] in tipo_SB:
                prediccion2 = prediccion
                prediccion = Branch_Predictor(Dir_Prediccion[i][1])
            else:
                prediccion = Branch_Predictor(Dir_Prediccion[i][1])

            if reg_EX_MEM[1] in tipo_SB:
                if prediccion2 == 1 and reg_EX_MEM[2] == "no_hay_salto":
                    ii = ii
                    i = i
                else:
                    if prediccion == 1:
                        ii = i
                        i = int(etiquetas[Dir_Prediccion[i][0]]) - int(1)
                    else:
                        ii = i
                        i = i
            else:
                if prediccion == 1:
                    ii = i
                    i = int(etiquetas[Dir_Prediccion[i][0]]) - int(1)
                else:
                    ii = i
                    i = i
            

        if reg_IF_ID[0] in tipo_UJ:
            i = int(etiquetas[reg_IF_ID[2]])
            print("Jump", i)

        if reg_EX_MEM[1] in tipo_SB:
            if reg_IF_ID[0] in tipo_SB and reg_EX_MEM[1] in tipo_SB:
                revisar = prediccion2

            else:
                revisar = prediccion

            if lista_aux3[-2] != 0:
                i = i

            elif reg_EX_MEM[2] != "no_hay_salto":
                Dir_Prediccion[ii][1] = State_machine(Dir_Prediccion[ii][1], 1)
                if revisar == 1:
                    print("Prediccion CORRECTA 1")
                    conteosal = conteosal + 1
                    if reg_IF_ID[0] in tipo_UJ:
                        i = i    
                    else:
                        i = i + int(1) 

                else:
                    print("Prediccion INCORRECTA 1")
                    conteosal2 = conteosal2 + 1
                    print("FLUSH!!!!!!!!")
                    reg_EnUso[0] = "X"
                    reg_EnUso[1] = "X"
                    i = reg_EX_MEM[2]
                    reg_IF_ID = ["X", "X", "X"]
                    reg_ID_EX = ["X", "X", "X"]

            elif reg_EX_MEM[2] == "no_hay_salto":
                Dir_Prediccion[ii][1] = State_machine(Dir_Prediccion[ii][1], 0)
                if revisar == 0:
                    print("Prediccion CORRECTA 2")
                    conteosal = conteosal + 1
                    i = i + int(1)
                else:
                    print("Prediccion INCORRECTA 2")
                    conteosal2 = conteosal2 + 1
                    print("FLUSH!!!!!!!!")
                    reg_EnUso[0] = "X"
                    reg_EnUso[1] = "X"
                    i = ii + 1 
                    reg_IF_ID = ["X", "X", "X"]
                    reg_ID_EX = ["X", "X", "X"]

            
            else:
                i = i + int(1)
        elif lista_aux3[-2] != 0:
            i = i
        else:
            if reg_IF_ID[0] in tipo_UJ:
                i = i    
            else:
                i = i + int(1) 
    #------------------------------------------  
        conteototalsal = conteosal + conteosal2
        print("CONTEOTOTAL",conteototalsal)
        if conteototalsal != 0:
            PA=(conteosal*100)/conteototalsal # Porcentaje de aciertos
            print("Numero de predicciones: ", conteototalsal)
            print("Porcentaje de aciertos: ",PA)
        

        if (num_inst != 0):
            CPI = j/num_inst
            print("CPI:",CPI)

        print("╔════════════╦════════════╦════════════╦════════════╦════════════╗")
        print("║   FETCHS   ║   DECODE   ║  EXECUTES  ║   MEMORY   ║ WRITE BACK ║") #12 espacios
        print("╠════════════╬════════════╬════════════╬════════════╬════════════╣")
        print("║", " "*((8-len(reg_IF_ID [0]))//2),reg_IF_ID [0]," "*((8-len(reg_IF_ID [0]))//2 + (8-len(reg_IF_ID [0]))%2), "║",
                " "*((8-len(reg_ID_EX [1]))//2),reg_ID_EX [1]," "*((8-len(reg_ID_EX [1]))//2 + (8-len(reg_ID_EX [1]))%2), "║",
                " "*((8-len(reg_EX_MEM[1]))//2),reg_EX_MEM[1]," "*((8-len(reg_EX_MEM[1]))//2 + (8-len(reg_EX_MEM[1]))%2), "║",
                " "*((8-len(reg_MEM_WB[1]))//2),reg_MEM_WB[1]," "*((8-len(reg_MEM_WB[1]))//2 + (8-len(reg_MEM_WB[1]))%2), "║", 
                " "*((8-len(reg_WB_FIN[0]))//2),reg_WB_FIN[0]," "*((8-len(reg_WB_FIN[0]))//2 + (8-len(reg_WB_FIN[0]))%2), "║")
        print("╚════════════╩════════════╩════════════╩════════════╩════════════╝")

        j += 1

        print("Ultimo i: ", i)

        if reg_IF_ID[0] == "X" and reg_ID_EX[0] == "X" and reg_EX_MEM[0] == "X" and reg_MEM_WB[0] == "X" and reg_WB_FIN[0] == "X":      
            print("Fin de la ejecucion")
            print("Presione 7 para salir al menu")
            entrada_aux = int(input("Ingrese una opcion: "))
            if entrada_aux == 7:
                i = 0
                j = 0
                num_inst = 0
                PA = 0
                conteosal = 0 
                conteosal2 = 0
                print("###################Menu Principal###################")
                print("Presione 1 para ver Ejecución sin forwarding ni Predicción de saltos")
                print("Presione 2 para ver Ejecución con forwarding sin Predicción de saltos")
                print("Presione 3 para ver Ejecución sin forwarding y con Predicción de saltos")
                print("Presione 4 para ver Ejecución con forwarding y con Predicción de saltos")
                entrada = int(input("Seleccione una opcion: "))
            elif entrada_aux == input():
                print("Digite un número")
            
            else:
                print("Opción inválida")    