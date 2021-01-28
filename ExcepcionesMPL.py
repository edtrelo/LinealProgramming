class ModelConstructError(Exception):
    """Esta clase la creamos para manejar las expeciones que resulten de intruducir de manera incorrecta
    los argumentos del init de la clase ModeloPL: A,b,c y el objetivo."""

    def __init__(self, op=1):
        self.op = op

    def __str__(self):
        if self.op == 1:
            return "El tamaño del Vector de Recursos o del Vector de Costos no es adecuado."
        elif self.op == 2:
            mensaje = "El tamaño de la Matriz de Restricciones no coincide con el tamaño del Vector" \
                      " de Recursos o con el del Vector de Costos."
            return mensaje
        elif self.op == 3:
            return "La opción de Objetivo no es válida: \"MAX\" o \"MIN\" son las únicas opciones válidas."
        else:
            return "El vector de recursos no es mayor o igual a cero."


class ProblemaNoAcotado(Exception):
    """Esta clase sirve para menejar el caso en el que el problema es no acotado."""
    def __init__(self):
        pass

    def __str__(self):
        return "El problema es no acotado."