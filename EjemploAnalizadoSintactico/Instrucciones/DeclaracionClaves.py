from Abstract.Abstract import Expression

class DeclaracionClaves(Expression):

    def __init__(self, nombre, elementos, fila, columna):
        self.nombre = nombre
        self.elementos = elementos
        super().__init__(fila, columna)

    def operar(self, arbol):
        pass

    def ejecutarT(self):
        return self.elementos

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()