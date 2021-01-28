#clase restriction.
class restriction:
    def __init__(self, coeficientes, res='=<'):
        """Para crear una restriction se necesitan los coeficientes y el tipo de restricción. Esta última
        debe darse como =<,=>,=, en forma de string."""
        self.coeficientes = coeficientes
        #Estas son las únicas restricciones que podemos usar.
        restricciones = ['=<', '=>', '=']
        for i in restricciones:
            if i == res:
                #Vericamos que res sea alguna de las restricciones.
                self.res = res
                return
        #En caso de que el argumento res no este en la lista, lanzamos un error.
        raise self.RestrictionConstructError

    def setRestriction(self, nueva_res):
        """Este método ayuda a cambiar el símbolo de la restricción."""
        restricciones = ['=<', '=>', '=']
        is_good = False
        for i in restricciones:
            if i == nueva_res:
                self.res = nueva_res
                is_good = True
                break
        if not is_good:
            raise self.RestrictionConstructError

    class RestrictionConstructError(Exception):
        def __init__(self):
            pass
        def __str__(self):
            return "Esa restricción no es válida."