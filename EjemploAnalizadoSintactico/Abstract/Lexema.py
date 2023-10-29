from Abstract.Abstract import Expression

class Lexema(Expression):

    def __init__(self, lexema,  fila, columna, tipo):
        self.lexema = lexema
        self.tipo = tipo
        super().__init__(fila, columna)

    def operar(self, arbol):   #! Retorna mi Lexema
        return self.lexema

    def getFila(self):              #! Retorna la fila
        return super().getFila()

    def getColumna(self):           #! Retorna la columna
        return super().getColumna()