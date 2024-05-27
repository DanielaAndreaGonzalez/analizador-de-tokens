import tkinter as tk
from tkinter import scrolledtext

def es_letra(car):
    """Devuelve True si el caracter es una letra del alfabeto."""
    return car.isalpha()

def es_digito(car):
    """Devuelve True si el caracter es un dígito numérico."""
    return car.isdigit()

def es_espacio(car):
    """Devuelve True si el caracter es un espacio en blanco, tabulador o salto de línea."""
    return car in ' \t\n'

def leer_numero(codigo_fuente, inicio):
    """
    Extrae un número (natural o real) desde el código fuente comenzando en la posición 'inicio'.
    Devuelve una tupla con el tipo de número y el número extraído, junto con la nueva posición del cursor.
    """
    i = inicio
    num = ''
    es_real = False

    while i < len(codigo_fuente) and (es_digito(codigo_fuente[i]) or codigo_fuente[i] == '.'):
        if codigo_fuente[i] == '.':
            if es_real:  # Segundo punto en el número, terminar la lectura
                break
            es_real = True
        num += codigo_fuente[i]
        i += 1
    token_type = 'NUMERO_REAL' if es_real else 'NUMERO_NATURAL'
    return (token_type, num), i

def leer_identificador(codigo_fuente, inicio):
    """
    Extrae un identificador o palabra reservada desde el código fuente comenzando en la posición 'inicio'.
    Devuelve una tupla con el tipo del identificador y el identificador extraído, junto con la nueva posición del cursor.
    """
    palabras_reservadas = {'galaxia', 'estrella', 'espacio', 'viaje', 'planeta', 'nebulosa'}
    i = inicio
    ident = ''
    while i < len(codigo_fuente) and (es_letra(codigo_fuente[i]) or es_digito(codigo_fuente[i]) or codigo_fuente[i] == '_'):
        ident += codigo_fuente[i]
        i += 1
    token_type = 'PALABRA_RESERVADA' if ident in palabras_reservadas else 'IDENTIFICADOR'
    return (token_type, ident), i

def leer_cadena(codigo_fuente, inicio):
    """
    Extrae una cadena literal del código fuente comenzando en la posición 'inicio'.
    Gestiona las comillas escapadas para incluirlas en la cadena literal.
    Devuelve una tupla con el tipo 'CADENA' y la cadena literal extraída, junto con la nueva posición del cursor.
    """
    i = inicio + 1  # Saltar la comilla inicial
    cadena = ''
    while i < len(codigo_fuente) and not (codigo_fuente[i] == '"' and codigo_fuente[i-1] != '\\'):
        cadena += codigo_fuente[i]
        i += 1
    return ('CADENA', cadena), i + 1  # Saltar la comilla final

def leer_comentario(codigo_fuente, inicio):
    """
    Identifica y extrae comentarios, tanto de línea como de bloque, desde el código fuente.
    Devuelve una tupla con el tipo de comentario y el comentario extraído, junto con la nueva posición del cursor.
    """
    if codigo_fuente[inicio+1] == '/':  # Comentario de línea
        i = codigo_fuente.find('\n', inicio)
        return ('COMENTARIO_LINEA', codigo_fuente[inicio:i]), max(i, inicio+2)
    elif codigo_fuente[inicio+1] == '*':  # Comentario de bloque
        i = codigo_fuente.find('*/', inicio) + 2
        return ('COMENTARIO_BLOQUE', codigo_fuente[inicio:i]), i

def tokenizar(codigo_fuente):
    """
    Procesa el texto de código fuente y extrae los tokens según las reglas definidas.
    Devuelve una lista de tuplas, cada una representando un token con su tipo y valor.
    """
    tokens = []
    i = 0
    longitud = len(codigo_fuente)
    while i < longitud:
        if es_espacio(codigo_fuente[i]):
            i += 1
            continue

        if codigo_fuente[i] == '"':
            token, i = leer_cadena(codigo_fuente, i)
            tokens.append(token)
            continue

        if codigo_fuente[i:i+2] in {'//', '/*'}:
            token, i = leer_comentario(codigo_fuente, i)
            tokens.append(token)
            continue

        if es_digito(codigo_fuente[i]) or (codigo_fuente[i] == '.' and i + 1 < longitud and es_digito(codigo_fuente[i+1])):
            token, i = leer_numero(codigo_fuente, i)
            tokens.append(token)
            continue

        if es_letra(codigo_fuente[i]):
            token, i = leer_identificador(codigo_fuente, i)
            tokens.append(token)
            continue

        # Detectar y almacenar operadores y otros caracteres especiales
        if codigo_fuente[i] in '+-*/=;[],{}()':
            op = codigo_fuente[i]
            if i + 1 < longitud and codigo_fuente[i+1] == '=' and codigo_fuente[i] in '+-*/<>=!':
                op += '='
                i += 1
            tokens.append(('OPERADOR', op))
            i += 1
            continue

        i += 1  # Avanzar si no coincide con ninguna regla conocida

    return tokens

# Ejemplo de uso
#codigo_fuente = 'galaxia = 42; estrella = 3.14; auto = "vehiculo"; // Comentario'
#codigo_fuente = 'galaxia = 42; estrella = 3.14; auto = "vehi\\"culo"; // Comentario de línea\n/* Comentario de bloque */'
with open('codigo_fuente_andromeda.txt', 'r') as archivo:
    codigo_fuente = archivo.read()
tokens = tokenizar(codigo_fuente)
for token in tokens:
    print(token)


#INTERFAZ GRAFICA
def mostrar_tokens(tokens):
    # Limpiar el área de texto
    txt_tokens.delete('1.0', tk.END)
    
    # Mostrar los tokens en el área de texto
    for token in tokens:
        txt_tokens.insert(tk.END, f"{token[0]}: {token[1]}\n")

# Crear la ventana principal
root = tk.Tk()
root.title("Analizador Léxico")

# Crear un área de texto desplazable para mostrar los tokens
lbl_tokens = tk.Label(root, text="Tokens reconocidos:")
lbl_tokens.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

txt_tokens = scrolledtext.ScrolledText(root, width=100, height=30)
txt_tokens.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

# Botón para iniciar el análisis del código
btn_analizar = tk.Button(root, text="Analizar Código", command=lambda: mostrar_tokens(tokenizar(codigo_fuente)))
btn_analizar.grid(row=4, column=0, padx=10, pady=5, columnspan=2)

# Ejecutar el bucle de eventos
root.mainloop()

