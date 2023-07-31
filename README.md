# Proyecto 2: Predictor de saltos en simulador de procesador RISC-V
### EL4314 - Arquitectura de Computadoras I
### Escuela de Ingeniería Electrónica
### Tecnológico de Costa Rica

<br/><br/>

### Preámbulo
En este proyecto, usted implementará un predictor de saltos dinámico para su simulador de un procesador RISC-V, escalar y de ejecución en orden, desarrollado en el proyecto 1. Su modelo de predictor de saltos deberá implementarse empleando un _Branch Target Buffer_ (BTB) para almacenar direcciones de salto calculadas así como determinar si se trata, a partir del _Program Counter_ (PC), de una instrucción de salto, y un predictor de dirección basado en un contador de 2 bits; todo esto tal y como se explicó en clase.

simulador, simple, para un procesasor RISC-V escalar, en orden, y con 5 etapas de _pipeline_. Para ello considere el diseño que se propone y describe en el capítulo 4 del Patterson y Hennessy. Dicho simulador deberá ser capaz de recibir un programa en lenguaje ensamblador y ejecutarlo, produciendo el resultado correcto. Deberá indicar en cada momento de la ejecución qué instrucción se está ejecutando en cuál etapa del _pipeline_ y proveer métricas de evaluación.


### Requisitos
Considere las siguientes características para el modelado e incorporación del predictor de saltos dinámico en su simulador:

- Deberá realizar la implementación del predictor de saltos dinámico empleado Python como lenguaje de programación.
- El simulador debera contar con la posibilidad de activar o desactivar la predicción de saltos antes de la ejecución de un programa. De igual manera, el simulador deberá permitir activar o desactivar la detección de riesgos de datos y su corrección mediante _forwarding_. En caso de que ninguna técnica de mitigación de riesgos de datos y/o control se active, el simulador deberá introducir _stalls_ o realizar _flush_ de manera apropiada para permitir la correcta ejecución.
- Considere que el cálculo de la direccion de salto se realiza en la etapa de _Execute_ del procesador. 
- En la etapa de _Instruction Fetch_, al mismo tiempo que se toma el valor del PC para acceder a la memoria de programa y extraer la instrucción, el valor del PC se emplea para acceder la BTB y extraer la dirección de salto (_target address_) en caso de que ya dicha dirección se haya calculado y almacenado en la BTB. Si el acceso a la BTB resulta en un _miss_ y se trata de una instrucción de salto, lo cual se conoce hasta la etapa de _Instruction Decode_, la dirección de salto que se calcula en la etapa de _Execute_ se almacena de forma correspondiente en la BTB.
- En la etapa de _Execute_, además de calcular la dirección de salto, se confirma si el salto se toma o no. Esta información es importante para actualizar el contador de 2 bits de acuerdo con la máquina de estados vista en clase. Si, por ejemplo, la predicción estableció que el salto se tomaba pero en la etapa de _Execute_ se determinó que el salto no debía tomarse, el simulador deberá realizar un _flush_ del _pipeline_ para las instrucciones anteriores al salto y deberá cargar en PC el valor correcto de la dirección d ela instrucción que se deberá ejecutar.
- Desarrolle 1 programa de prueba, suficientemente complejo, y con sentido algorítmico (no solamente un poco de instrucciones juntas) con el que pueda evaluar los siguientes 4 casos: a) ejecución sin _forwarding_ ni predicción de saltos, b) ejecución con _forwarding_ pero sin predicción de saltos, c) ejecución con predicción de saltos pero sin _forwarding_, y d) ejecución con _forwarding_ y predicción de saltos activos. Reporte los resultados de instrucciones ejecutadas, ciclos de reloj y CPI para cada uno de estos escenarios de ejecución.

### Advertencia
Aún cuando existen implementaciones disponibles que realizan, en una u otra medida, lo que aquí se les solicita, está prohibido utilizar código existente de algún repositorio (aún cuando este se encuentre abierto y el licenciamiento de que posea permita su utilización).


## Evaluación
Este proyecto se evaluará con la siguiente rúbrica:


| Rubro | % | C | EP | D | NP |
|-------|---|---|----|---|----|
|Implementación del predictor de saltos | 40| X  |    |   |    |
|Integración en simulador | 30| X  |    |   |    |
|Evaluación con benchmark propuesto | 20| X  |    |   |    |
|Uso de repositorio|10| X  |    |   |    |

C: Completo,
EP: En progreso ($\times 0,8$),
D: Deficiente ($\times 0,5$),
NP: No presenta ($\times 0$)

## Importante
- El uso del repositorio implica que existan contribuciones de todos los miembros del equipo. 
- La revisión del simulador con el predictor de saltos se deberá realizar antes de las 17:00 del jueves 15 de junio. Para dicha revisión, deberá agendar una cita con antelación.

## Resultados obtenidos para instrucciones ejecutadas, ciclos de reloj y CPI para cada escenario

## Ejecución de código Matriz 4x4 
|                   | 1.Ejecución sin forwarding ni predicción de saltos | 2.Ejecución con forwarding pero sin predicción de saltos  | 3.Ejecución sin forwarding con predicción de saltos     | 4.Ejecución con forwarding y predicción de saltos|
| ------------------| --------------------------- | ------------------------------| -------------------------------| ---------------------------|
| Num de instruc    | 159                         | 159                           | 159                            | 159                        |
| Num de ciclos     | 283                         | 171                           | 285                            | 177                        |
| CPI               | 1.77                        | 1.075                         | 1.79                           | 1.11                       |
| % Aciertos        | No aplica                   | No aplica                     | 72%                            | 68%                        |
| Num de predicc    | No aplica                   | No aplica                     | 25                             | 25                         |

Puede verse que para los 4 modos de ejecución el número de instrucciones ejecutadas es la misma. En los casos donde no hay forwarding implementado (columnas 1 y 3) se observa un incremento en el número de ciclos de reloj transcurridos para terminar el programa. Para los casos donde sí se implementa el forwarding (columnas 2 y 4) es evidente que el número de ciclos de reloj disminuye significativamente, 112 ciclos de diferencia entre el caso 1 y 2 y 108 ciclos de diferencia entre el caso 3 y 4.

En cuanto al número de Ciclos por Instrucción aquellos casos que presentan mayor cantidad de ciclos (tablas 1 y 3) presentan un CPI mayor (1.77 y 1.79 respectivamente). Los casos que presetan menor cantidad de ciclos (tablas 2 y 4) presentan CPI menor (1.075 y 1.11). Puede destacarse el hecho que activar o desactivar la predicción de saltos no genera cambios significativos en el CPI.


## Ejecución de código Multiplicación Rusa
|                   | 1.Ejecución sin forwarding ni predicción de saltos | 2.Ejecución con forwarding pero sin predicción de saltos  | 3.Ejecución sin forwarding con predicción de saltos     | 4.Ejecución con forwarding y predicción de saltos|
| ------------------| --------------------------- | ------------------------------| -------------------------------| ---------------------------|
| Num de instruc    | 50                          | 50                            | 50                             | 50                         |
| Num de ciclos     | 94                          | 60                            | 96                             | 62                         |
| CPI               | 1.88                        | 1.2                           | 1.92                           | 1.24                       |
| % Aciertos        | No aplica                   | No aplica                     | 54%                            | 63%                        |
| Num de predicc    | No aplica                   | No aplica                     | 11                             | 11                         |


Al igual que para el caso del código de la matriz 4x4, el número de ciclos de reloj es mayor para los casos donde no hay forwarding, la implementación de predicción de saltos incrementa ligeramente el número de ciclos esto se observa comparando las columnas 1 y 3 (94 y 96 ciclos respectivamente). El mismo  fenómeno se observa comparando el número de ciclos de las columnas 2 y 4 (60 y 62 respectivamente).

Para el caso del CPI este es mayor en los escenarios donde no hay forwarding como consecuecia de que hay mayor número de ciclos. El efecto de activar o desactivar la predicción de saltos no produce grandes diferencias en el valor del CPI, comparando las columnas 2 y 4 (con valores de CPI 1.2 y 1.24 respectivamente).

El porcentaje de aciertos solo aplica para los escenarios donde hay predicción de saltos implementada (columnas 3 y 4). El porcentaje de predicción de saltos es menor para la Ejecución sin forwarding pero con predicción de saltos 54% comparado con el 63% que arroja la Ejecución con forwarding y predicción de saltos. Lo que indica que el forwarding incide de forma positiva en la predicción de saltos. El número de predicciones realizadas por los 2 escenarios es 11 y tiene sentido que sea igual puesto que es el mismo programa el que se está ejecutando.


## Ejecución de código Fibonacci
|                   | 1.Ejecución sin forwarding ni predicción de saltos | 2.Ejecución con forwarding pero sin predicción de saltos  | 3.Ejecución sin forwarding con predicción de saltos     | 4.Ejecución con forwarding y predicción de saltos|
| ------------------| --------------------------- | ------------------------------| -------------------------------| ---------------------------|
| Num de instruc    | 66                          | 66                            | 66                             | 66                         |
| Num de ciclos     | 104                         | 72                            | 106                            | 72                         |
| CPI               | 1.58                        | 1.09                          | 1.6                            | 1.09                       |
| % Aciertos        | No aplica                   | No aplica                     | 81%                            | 90%                        |
| Num de predicc    | No aplica                   | No aplica                     | 11                             | 11                         |


El  número de ciclos de reloj es mayor para los casos donde no hay forwarding, la implementación de predicción de saltos en este caso incrementa un poco  el número de ciclos esto se observa comparando las columnas 1 y 3 (104 y 106 respectivamente). Comparando las columnas 2 y 4 no hay un incremento en el número de ciclos (72 para ambas). 

Para el caso del CPI este es mayor en los escenarios donde no hay forwarding como consecuecia de que hay mayor número de ciclos. El efecto de activar o desactivar la predicción de saltos no produce grandes diferencias en el valor del CPI, comparando las columnas 2 y 4 (ambos tienen valores de 1.09).

En cuanto al porcentaje de predicción de saltos, ocurre el mismo comportamiento que con los códigos anteriores, la ejecución con forwarding y predicción de saltos brinda un mejor porcentaje 90% contra un 81%  de la ejecución sin forwarding y con predicción de saltos.


## Ejecución de código Factorial 
|                   | 1.Ejecución sin forwarding ni predicción de saltos | 2.Ejecución con forwarding pero sin predicción de saltos  | 3.Ejecución sin forwarding con predicción de saltos     | 4.Ejecución con forwarding y predicción de saltos|
| ------------------| --------------------------- | ------------------------------| -------------------------------| ---------------------------|
| Num de instruc    | 107                         | 107                           | 107                            | 107                        |
| Num de ciclos     | 150                         | 121                           | 150                            | 125                        |
| CPI               | 1.401                       | 1.13                          | 1.401                          | 1.16                       |
| % Aciertos        | No aplica                   | No aplica                     | 77%                            | 70%                        |
| Num de predicc    | No aplica                   | No aplica                     | 26                             | 26                         |


El  número de ciclos de reloj es mayor para los casos donde no hay forwarding, la implementación de predicción de saltos en este caso casi no incrementa el número de ciclos esto se observa comparando las columnas 1 y 3 (156 y 157 respectivamente). Comparando las columnas 2 y 4 hay un decremento en el número de ciclos (121 y 67 respectivamente).

Para el caso del CPI este es mayor en los escenarios donde no hay forwarding como consecuecia de que hay mayor número de ciclos. El efecto de activar o desactivar la predicción de saltos no produce grandes diferencias en el valor del CPI, comparando las columnas 2 y 4 (ambos tienen valores de 1.13).
En cuanto a la predicción de saltos, para este codigo no hay gran diferencia, asi que se puede decir que tanto forwardign con prediiccion de saltos y prediccion de saltos sin forwarding,tienen casi el mismo rendimiento y esto se debe a que en este codigo no se explota tanto las ventjas del forwarding.
