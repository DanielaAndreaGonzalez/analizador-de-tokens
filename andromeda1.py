import re

# Definir expresiones regulares para cada tipo de token
patrones = {
    'NUMERO_NATURAL': r'\b\d+\b',
    'NUMERO_REAL': r'\b\d+\.\d+\b',
    'IDENTIFICADOR': r'\b[a-zA-Z][a-zA-Z0-9_]{0,9}\b',
    'PALABRA_RESERVADA': r'\b(?:galaxia|estrella|espacio|viaje|planeta|nebulosa)\b',
    'OPERADOR_ARITMETICO': r'[\+\-\*/]',
    'OPERADOR_COMPARACION': r'[<>]=?|==',
    'OPERADOR_LOGICO': r'\b(?:AND|OR|NOT)\b',
    'OPERADOR_ASIGNACION': r'=',
    'OPERADOR_INCREMENTO_DECREMENTO': r'\+\+|\-\-',
    'PARENTESIS_LLAVES': r'[()\[\]{}]',
    'TERMINAL': r';',
    'SEPARADOR': r',',
    'HEXADECIMAL': r'0[xX][0-9a-fA-F]+',
    'CADENA': r'\".*?\"',
    'COMENTARIO_LINEA': r'//.*',
    'COMENTARIO_BLOQUE': r'/\*.*?\*/'
}

# Leer el código fuente desde un archivo
with open('codigo_fuente_andromeda.txt', 'r') as archivo:
    codigo_fuente = archivo.read()

# Inicializar lista de tokens reconocidos
tokens = []

# Buscar y reconocer los tokens en el código fuente
for patron in patrones:
    regex = re.compile(patrones[patron])
    coincidencias = regex.findall(codigo_fuente)
    for coincidencia in coincidencias:
        # Verificar si el token es un comentario de línea o de bloque y omitirlo
        if patron.startswith('COMENTARIO'):
            continue
        # Verificar si el token es una cadena de caracteres y eliminar las comillas dobles
        elif patron == 'CADENA':
            tokens.append((patron, coincidencia[1:-1]))
        else:
            tokens.append((patron, coincidencia))

# Mostrar los tokens reconocidos
for token in tokens:
    print(token)
