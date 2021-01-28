from sympy import *
from MétodosAuxiliares import *
from restriction import *
import copy
from ExcepcionesMPL import *

class ModeloPL:

    def __init__(self, MatrizRestricciones, VectorRecursos, VectorCostos, objetivo = "MAX"):
        """Creamos una el objeto de la clase Modelo PL.

        MatrizRestricciones:
            Matriz de mxn, donde m son las restricciones y n las variables.

            Puede agregarse como una matriz hecha con listas de python.

        VectorRecursos:
            Vector de mx1. Puede agregarse como una lista b=[b_1,...,b_m]. Se debe tener que b_i=>0.

        VectorCostos:
            Vector de 1xn. Puede agregarse como una lista dentro de otra lista c=[[c_1,...,c_n]].

        Objetivo:
            Se ingresa de forma de string. Las únicas opciones posibles son 'MAX' o 'MIN'. Ya sea en
            mayúsculas o minúsculas.
        """
        #Verificamos que todas las entradas del vector de recursos sean mayores o iguales a cero.
        for b in VectorRecursos:
            if b<0:
                #En caso contrario, lanzamos una excepción.
                raise ModelConstructError(op = 4)

        #Convertimos las listas en matrices de sympy.
        self.A =  Matrix(MatrizRestricciones)
        self.c = Matrix(VectorCostos)
        self.b = Matrix(VectorRecursos)

        #Verificamos que el objetivo sea 'MAX' o 'MIN'.
        if objetivo.upper() != "MAX" and objetivo.upper() != "MIN":
            #Lazamos una expeción en caso contrario
            raise ModelConstructError(op = 3)
        else:
            self.objetivo = objetivo.upper()

        #Obtenemos los tamaños de A,b y c.
        A_filas, A_col = self.A.shape
        b_filas, b_col = self.b.shape
        c_filas, c_col = self.c.shape

        #Verificamos que b sea vector columna y c sea vector fila.
        if b_col != 1 or c_filas != 1:
            #Lazamos una excepción si no son vectores como son pedidos.
            raise ModelConstructError(op = 1)
        #Verificamos que las filas de b coincidan con las de A y que las columnas de c coincidan con las de A.
        if A_filas != b_filas or A_col != c_col:
            raise ModelConstructError(op = 2)

        #Construimos una lista que albergará todas las restricciones como objetos de la clase restriction.
        #self.rest
        self.restricciones = []
        #recorremos las filas de A.
        for i in range(A_filas):
            #Esta lista contendrá los coeficientes de la fila actual.
            coeficientes = []
            #Recorresmos la fila actual.
            for j in range(A_col):
                #Agregamos el elemento A(i,j)
                coeficientes.append(self.A[i,j])
            #Creamos una nueva restricción con los coeficientes de la fila obtenida, la iniciamos como del tipo =.
            restricción = restriction(coeficientes)
            #Agregamos esta restricción a la lista.
            self.restricciones.append(restricción)

        self.soluciones = None
        self.solucionesDuales = None
        self.status = False
        self.TablaSimplex = None
        self.Aampliada = self.A
        self.TablaÓptima = None
        self.ValorÓptimo = None
        self.BaseÓptima = None
        self.CostosBase = None

    def __repr__(self):
        """Este método crea una representación en cadena de un objeto de la clase ModeloPL"""
        mensaje = "Objetivo: " + str(self.objetivo) + ";\nRestricciones: " + str(self.A.shape[0]) + \
                  ";\nVariables = "+ str(self.A.shape[1])+";\nSoluciones: " + str(self.soluciones) + \
                  ";\nSoluciones Duales: " + str(self.solucionesDuales)+";\nValor Óptimo: " + \
                  str(self.ValorÓptimo)
        return "-- Modelo de Programación Lineal --\n" + mensaje

    def cambiarRestricción(self, nueva_res, j):
        """Se usa para cambiar el signo de la j-ésima restricción por nueva_res."""
        self.restricciones[j].setRestriction(nueva_res)

    def construirTablaInicial(self):
        """Construimos una tabla óptima inicial. Usamos el método de la gran M."""
        #Establecemos un número grande para M.
        M = 9999
        #Iniciaremos desde la matriz de restricciones.
        TablaSimplex = self.A
        #Usaremos el vector c.
        c = self.c
        #Obtenemos el tamaño de la matriz A.
        m, n = TablaSimplex.shape


        for i in range(m):
            #Si la restricción actual es del tipo menor o igual:
            if self.restricciones[i].res == '=<':
                columna = zeros(m, 1)
                #Hacemos que la fila de la columna nueva correspondiente a la restricción actual sea 1.
                columna[i] = 1
                #Le pegamos a nuestra tabla simples la columna que creamos. Esto corresponde a agregar una
                #variable de holgura.
                TablaSimplex = TablaSimplex.row_join(columna)
                #Le agregramos su coeficiente correspondiente a esta variable de holgura.
                c = c.row_join(Matrix([0]))
            #Si la restricción actual es del tipo mayor o igual.
            elif self.restricciones[i].res == '=>':
                columna = zeros(m, 1)
                # Hacemos que la fila de la columna nueva correspondiente a la restricción actual sea -1.
                columna[i] = -1
                # Le pegamos a nuestra tabla simples la columna que creamos. Esto corresponde a agregar una
                # variable de holgura.
                TablaSimplex = TablaSimplex.row_join(columna)
                # Le agregramos su coeficiente correspondiente a esta variable de holgura.
                c = c.row_join(Matrix([0]))
                # Volvemos a modificar la columna para agregar una variable ficticia.
                columna[i] = 1
                # Le agregramos su columna correspondiente a esta variable de ficticia.
                TablaSimplex = TablaSimplex.row_join(columna)
                #Verificamos cómo será el valor de M en el vector de recursos y unimos el valor al vector c.
                if self.objetivo == 'MAX':
                    c = c.row_join(Matrix([-M]))
                else:
                    c = c.row_join(Matrix([M]))
            else:
                columna = zeros(m, 1)
                # Hacemos que la fila de la columna nueva correspondiente a la restricción actual sea 1.
                columna[i] = 1
                # Le agregramos su columna correspondiente a esta variable de ficticia.
                TablaSimplex = TablaSimplex.row_join(columna)
                # Verificamos cómo será el valor de M en el vector de recursos y unimos el valor al vector c.
                if self.objetivo == 'MAX':
                    c = c.row_join(Matrix([-M]))
                else:
                    c = c.row_join(Matrix([M]))
        #Unimoa la matriz de restricciones ya actualizada con el vector de costos actualizado.
        TablaSimplex = c.col_join(TablaSimplex)
        #Creamos una nueva casilla donde estará el valor de -z. La unimos arriba del vector de recursos.
        recursos = zeros(1, 1).col_join(self.b)
        #Pegamos las dos partes juntas.
        TablaSimplex = TablaSimplex.row_join(recursos)
        self.TablaSimplex = TablaSimplex
        #Creamos una copia estática de la tabla inicial
        self.Aampliada = copy.deepcopy(TablaSimplex)

    def esTablaÓptima(self):
        """Este método verifica si la tabla simplex actual ya es óptima."""
        if self.objetivo == 'MAX':
            #Recordemos que para un problema de maximización, la tabla es óptima si c =< 0.
            #Verificamos el signo del vector de costos reducido. True si c_j > 0, False en otro caso.
            signos = [self.TablaSimplex[0, j] > 0 for j in range(self.TablaSimplex.shape[1]-1)]
        else:
            # Recordemos que para un problema de minimización, la tabla es óptima si c => 0.
            # Verificamos el signo del vector de costos reducido. True si c_j < 0, False en otro caso.
            signos = [self.TablaSimplex[0, j] < 0 for j in range(self.TablaSimplex.shape[1]-1)]
        try:
            #Regresamos la j tal que c_j es la que viola el criterio de optimalidad.
            return signos.index(True)
            #En caso de que todas las c_j cumplan el criterio, regresamos un None.
        except ValueError:
            return None

    def reglaCociente(self, j):
        """Este método regresa la fila de la variable básica que debe salir, siguiendo la regla del cociente.
        El argumento j es la columna que violó el criterio de optimalidad."""
        #Aquí agremamos el resultado de dividir b_i/TablaSimplex[i,j]
        cocientes = []
        #Recorremos todos los elementos de la columna por excepción de c_rayita
        for i in range(1, self.TablaSimplex.shape[0]):
            #solo nos interesan los elementos de la columna mayores a cero
            if self.TablaSimplex[i,j]>0:
                #hacemos la dibisión b_i/T_ij
                cociente = self.TablaSimplex[i,-1]/self.TablaSimplex[i,j]
                cocientes.append(cociente)
            else:
                #Si el elemento de la columna no es positivo, lo caracterizamos como None
                cocientes.append(None)
        try:
            #Regresa la columna que arroja el mínimo
            return cocientes.index(mínimo(cocientes)) + 1
        except:
            #Llegar hasta esta instancia significa que ningun elemento de la columna fue mayor a cero y por lo
            #tanto el problema es ni acotado
            raise ProblemaNoAcotado


    def pivotear(self, i, j):
        """Este método permite pivotear sobre el elemento en la posición (i,j) de la Tabla Simplex."""
        #Obtenemos el pivote.
        pivote = self.TablaSimplex[i, j]
        #En caso de que el pivote sea cero, sumamos la primer columna cuyo elemento arriba o abajo del pivote no sea
        #cero
        if pivote==0:
            for x in range(self.TablaSimplex.shape[0]):
                if self.TablaSimplex[x,j]!=0:
                    pivote = self.TablaSimplex[x,j]
                    break
        for y in range(self.TablaSimplex.shape[1]):
            #Dividimos la fila del pivote entre sí mismo para hacer el uno en la posición (i,j).
            self.TablaSimplex[i, y] = self.TablaSimplex[i, y] / pivote
        #Hacemos las correspondientes eliminaciones en la columna
        for x in range(self.TablaSimplex.shape[0]):
            #omitimos la misma columna
            if x == i:
                pass
            else:
                #este es - el pivote, para hacer el cero en la columna
                diferencia = -self.TablaSimplex[x, j]
                for y in range(self.TablaSimplex.shape[1]):
                    self.TablaSimplex[x, y] = self.TablaSimplex[x, y] + self.TablaSimplex[i, y] * diferencia

    def simplex(self):
        """Usamos el método Simplex de manera recursiva para resolver el problema."""
        #El algoritmo se ejecuta mientras la tabla no sea óptima.
        while self.esTablaÓptima() is not None:
            #j es la columna que viola la optimalidad
            j = self.esTablaÓptima()
            #i es la columna de la variable básica que saldrá.
            i = self.reglaCociente(j)
            #Pivoteamos sobre i,j
            self.pivotear(i, j)
            self.simplex()

    def solve(self):
        """Se resuelve el problema y se extraen las soluciones"""
        #Construimos la tabla simplex inicial
        self.construirTablaInicial()
        self.simplex()
        #salir de aquí significa que la tabla ya es óptima
        self.status = True
        #La tabla óptima es la última tabla simplex construida
        self.TablaÓptima = self.TablaSimplex
        #Extraemos las soluciones del problema
        self.obtenerSoluciones()
        #Verificamos si hay otro óptimo
        if self.hayOtroÓptimo():
            self.obtenerÓptimoAlternativo()
        #Obtenemos las soluciones duales
        self.obtenerSolucionesDualdes()
        self.ValorÓptimo = - self.TablaÓptima[0, self.TablaÓptima.shape[1] - 1]

    def obtenerCostosReducidoBase(self):
        """Obtiene el sub vector del vector de costos reducidos asociado a la base óptima."""
        cB = []
        for j in range(0, self.TablaSimplex.shape[1] - 1):
            columna = self.TablaSimplex[1:, j]
            if esIdentidad(columna) and self.TablaSimplex[0, j] == 0:
                cB.append(self.Aampliada[0,j])
        self.CostosBase = Matrix([cB])

    def obtenerBase(self):
        """Obtiene la matriz B base de la solución y los índices de las variables correspondientes."""
        Bvacía = zeros(self.A.shape[0],1)
        B = Bvacía
        while B.shape[0]!=B.shape[1]:
            for j in range(0, self.TablaSimplex.shape[1]-1):
                columna = self.TablaSimplex[1:,j]
                if esIdentidad(columna) and self.TablaSimplex[0,j]==0:
                    if B == Bvacía:
                        B = self.Aampliada[1:,j]
                    else:
                        B = B.row_join(self.Aampliada[1:,j])
        self.BaseÓptima = B

    def obtenerSoluciones(self):
        """Extrae las soluciones del problema a partir de la tabla simplex óptima. Se usa el echo de que
        las variables básicas son a las que les corresponden columnas tipo identidad."""
        if not self.status:
            return None
        else:
            #Obtenemos una lista con todas las columnas
            columnas = [self.TablaÓptima[:, j] for j in range(self.TablaÓptima.shape[1])]
            #No nos sirve la columna del vector b
            columnas = columnas[:self.A.shape[1]]
            #Creamos unn vector de puros ceros.
            soluciones = [0]*self.A.shape[1]
            for col in columnas:
                #Si la columna es identidad,
                if esIdentidad(col):
                    soluciones[columnas.index(col)] = self.TablaÓptima[índice_del_uno(col), -1]
            self.soluciones = soluciones

    def obtenerSolucionesDualdes(self):
        """Obtenemos las soluciones duales a partir de la base de la solución óptima del primal."""
        self.obtenerBase()
        self.obtenerCostosReducidoBase()
        y = self.CostosBase*self.BaseÓptima.inv()
        self.solucionesDuales = vectorToList(y)

    def obtenerÓptimoAlternativo(self):
        """Obtenemos otro óptimo pivoteando sobre la columna con c=0 y que no es básica."""
        #Guardamos la primer solución
        solución_uno = self.soluciones
        j = self.columnaOtroÓptimo()
        i = self.reglaCociente(j)
        #pivotemos sobre la nueva columna
        self.pivotear(i, j)
        self.obtenerSoluciones()
        self.soluciones = 't' + str(self.soluciones) + '+(1-t)' + str(solución_uno) + '\n0 =< t =< 1'

    def columnaOtroÓptimo(self):
        """Regresa el index de la columna cuya variable no es básica pero su costo reducido es cero."""
        for j in range(self.TablaÓptima.shape[1]-1):
            columna = self.TablaÓptima[1:,j]
            if not esIdentidad(columna) and self.TablaÓptima[0,j]==0:
                return j

    def hayOtroÓptimo(self):
        """Verifica si hay un óptimo alternativo."""
        for j in range(self.TablaÓptima.shape[1]-1):
            columna = self.TablaÓptima[1:,j]
            if not esIdentidad(columna) and self.TablaÓptima[1,j]==0:
                return True
        return False



