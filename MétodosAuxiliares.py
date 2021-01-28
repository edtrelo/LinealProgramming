from sympy import zeros

def esIdentidad(columna):
    """verifica si una columna es la forma (0,0,...1,...,0,0)"""
    Id = False
    filas = columna.shape[0]
    for i in range(filas):
        sub_id = zeros(filas, 1)
        sub_id[i, 0] = 1
        if columna == sub_id:
            Id = True
            break
    return Id

def índice_del_uno(columna):
    """Regresa el índice donde hay un uno en una columna."""
    índice = None
    for i in range(columna.shape[0]):
        if columna[i, 0] == 1:
            índice = i
            break
    return índice

def mínimo(lista):
    """Este método regresa el mínimo de una lista que incluye elementos None."""
    lista_sin_none = []
    for item in lista:
        if item is None:
            pass
        else:
            lista_sin_none.append(item)
    return min(lista_sin_none)

def vectorToList(vector):
    """Regresa el equivalente de lista de un vector de sympy."""
    lista = []
    for j in range(vector.shape[1]):
        lista.append(vector[0,j])
    return lista