from Abstract.Abstract import Expression

class Texto(Expression):

    def __init__(self, texto, tipo, fila, columna):
        self.texto = texto
        self.tipo = tipo
        super().__init__(fila, columna)

    def operar(self, arbol):
        pass

    def ejecutarT(self):
        pass

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
