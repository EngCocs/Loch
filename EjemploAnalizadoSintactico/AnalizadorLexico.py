from Abstract.Numero import *
from Abstract.Lexema import *
from Instrucciones.Texto import *
from Errores.Errores import *

reserverd = {
    'RCLAVES': 'Claves',
    'RIMPRIMIR': 'imprimir',
    'IGUAL': '=',
    'CORIZQ': '[',
    'CORDER': ']',
    'COMILLA': '"',
    'PARIZQ': '(',
    'PARDER': ')',
    'COMA': ',',
    'PUNTOYCOMA': ';',
}

lexema = list(reserverd.values())
global n_linea
global n_columna
global instrucciones
global lista_lexemas

n_linea = 1
n_columna = 1
lista_lexemas = []
instrucciones = []
lista_errores = []

def instruccion(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ''
    puntero = 0
    palabras_reservadas = ['Claves', 'imprimir']
    while cadena:
        char = cadena[puntero]
        puntero += 1

        if char == '"':       #! leemos nuestra cadena y al encontrar " que habre empieza a crear el token
            l = Lexema('"', n_linea, n_columna, 'COMILLA')
            lista_lexemas.append(l)
            lexema, cadena = armar_lexema(cadena[puntero:])
            if lexema and cadena:
                n_columna += 1
                #Armar lexema como clase
                l = Lexema(lexema, n_linea, n_columna, 'TEXTO')
                lista_lexemas.append(l)  #! Agregamos los lexemas a la lista_lexema
                n_columna += len(lexema) + 1
                puntero = 0
            l = Lexema('"', n_linea, n_columna, 'COMILLA')
            lista_lexemas.append(l)
            n_columna += 1
            puntero = 0

        elif cadena.startswith("Claves"):
            lexema, cadena = armar_lexema(cadena)
            if lexema and cadena:
                n_columna += 1
                l = Lexema(lexema, n_linea, n_columna, 'CLAVES')
                lista_lexemas.append(l)
                n_columna += len(lexema) + 1
                puntero = 0

        elif cadena.startswith("imprimir"):
            lexema, cadena = armar_lexema(cadena)
            if lexema and cadena:
                n_columna += 1
                l = Lexema(lexema, n_linea, n_columna, 'IMPRIMIR')
                lista_lexemas.append(l)
                n_columna += len(lexema) + 1
                puntero = 0
            l = Lexema('(', n_linea, n_columna, 'PARIZQ')
            lista_lexemas.append(l)
            n_columna += 1
            puntero = 0

        elif char.isdigit():
            token, cadena = armar_numero(cadena)
            if token and cadena:
                n_columna += 1
                #! Armamos lexema como clase
                n = Numero(token, n_linea, n_columna)

                lista_lexemas.append(n)
                n_columna += len(str(token)) + 1
                puntero = 0

        elif char == '[' or char == ']':
            # ! Armamos lexema como clase
            c = Lexema(char, n_linea, n_columna, 'CORCHETE')

            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1

        elif char == ';':

            c = Lexema(char, n_linea, n_columna, 'PUNTOYCOMA')

            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1

        elif char == '=':
            c = Lexema(char, n_linea, n_columna, 'IGUAL')
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1

        elif char == ',':
            c = Lexema(char, n_linea, n_columna, 'COMA')
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1

        elif char == ')':
            c = Lexema(char, n_linea, n_columna, 'PARDER')
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1

        elif char == "\t":
            n_columna += 4
            cadena = cadena[4:]
            puntero = 0
        elif char == "\n":
            cadena = cadena[1:]
            puntero = 0
            n_linea += 1
            n_columna = 1
        elif char == ' ' or char == '\r' or char == '.' or char == ':': #! Y Desde aquí se omiten los espacios
            n_columna += 1
            cadena = cadena[1:]
            puntero = 0
        else:
            lista_errores.append(Errores(char, "Léxico",n_linea, n_columna))
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1

    return lista_lexemas


def armar_lexema(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ''
    puntero = ''

    for char in cadena:
        puntero += char
        if char == '"' or char == '\n' or char == '\t' or char == '(' or char == ')':
            return lexema, cadena[len(puntero):]   # Se toman en cuenta los espacios
        else:
            lexema += char   #! creamos nuestros Token
    return None, None

def armar_numero(cadena):
    numero = ''
    puntero = ''
    is_decimal =  False

    for char in cadena:
        puntero += char
        if char == '.':
            is_decimal = True

        if char == ' ' or char == '\n' or char == '\t':
            if is_decimal:
                return float(numero), cadena[len(puntero)-1:]
            else:
                return int(numero), cadena[len(puntero)-1:]
        else:
            if char != ',': #! si no es una coma lo agregamos al numero
                numero += char
    return None, None



