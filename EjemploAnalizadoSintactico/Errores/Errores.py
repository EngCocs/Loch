from Abstract.Abstract import Expression

class Errores(Expression):

    def __init__(self,lexema,tipo, fila, columna):
        self.lexema = lexema
        self.tipo = tipo
        super().__init__(fila, columna)

    def operar(self, no):
        lex = "Error: " + self.lexema + " Tipo: " + self.tipo
        return lex

    def getColumna(self):
        return super().getColumna()

    def getFila(self):
        return super().getFila()
