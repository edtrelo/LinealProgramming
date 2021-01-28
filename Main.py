import ProgramaciónLineal

#ESTE ES EL ARCHIVO QUE HAY QUE CORRER
#Los problemas de prueba se sacaron del libro de "Intro. a la Programación Lineal" de Hernández Ayuso.

print('Problema de Maximización (3.1): ')
A = [[-1,2,1],[3,2,0],[1,-1,0]]
b = [4,14,3]
c = [[3,2,1]]
P = ProgramaciónLineal.ModeloPL(A, b, c)
P.cambiarRestricción('=',0)
P.solve()
print(P,'\n')

print('Problema de Minimización (3.2): ')
A = [[-1,1,1,1,0],[1,1,0,0,1],[2,1,1,0,0]]
b = [1,2,6]
c = [[-2,1,-1,1,-1]]
P = ProgramaciónLineal.ModeloPL(A, b, c,objetivo = 'Min')
P.cambiarRestricción('=',0)
P.cambiarRestricción('=',1)
P.solve()
print(P,'\n')

#Este va a resultar en una excepción
# print('Problema de Maximización no acotado (3.5): ')
# A = [[1,-1],[1,0],[0,1]]
# b = [0,3,1]
# c = [[-3,2]]
# P = ProgramaciónLineal.ModeloPL(A, b, c,objetivo = 'Max')
# P.cambiarRestricción('=>',2)
# P.solve()

#Este tiene el error de que me da un óptimo bueno y uno malo.
print('Problema con Múltiples Óptimos (3.3): ')
A = [[1,-1],[1,0],[0,1]]
b = [0,3,1]
c = [[-2,2]]
P = ProgramaciónLineal.ModeloPL(A, b, c,objetivo = 'Min')
P.cambiarRestricción('=>',2)
P.solve()
print(P,'\n')





