import tkinter as tk
from tkinter import scrolledtext
import re

def analizar_codigo(codigo):
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

    # Inicializar lista de tokens reconocidos
    tokens = []

    # Buscar y reconocer los tokens en el código fuente
    for patron in patrones:
        regex = re.compile(patrones[patron])
        coincidencias = regex.findall(codigo)
        for coincidencia in coincidencias:
            # Verificar si el token es un comentario de línea o de bloque y omitirlo
            if patron.startswith('COMENTARIO'):
                continue
            # Verificar si el token es una cadena de caracteres y eliminar las comillas dobles
            elif patron == 'CADENA':
                tokens.append((patron, coincidencia[1:-1]))
            else:
                tokens.append((patron, coincidencia))

    return tokens

def mostrar_tokens(tokens):
    # Limpiar el área de texto
    txt_tokens.delete('1.0', tk.END)
    
    # Mostrar los tokens en el área de texto
    for token in tokens:
        txt_tokens.insert(tk.END, f"{token[0]}: {token[1]}\n")

# Crear la ventana principal
root = tk.Tk()
root.title("Analizador Léxico")

# Crear un área de texto para ingresar el código fuente
lbl_codigo = tk.Label(root, text="Código fuente:")
lbl_codigo.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

txt_codigo = scrolledtext.ScrolledText(root, width=40, height=10)
txt_codigo.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

# Crear un área de texto desplazable para mostrar los tokens
lbl_tokens = tk.Label(root, text="Tokens reconocidos:")
lbl_tokens.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

txt_tokens = scrolledtext.ScrolledText(root, width=40, height=10)
txt_tokens.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

# Botón para iniciar el análisis del código
btn_analizar = tk.Button(root, text="Analizar Código", command=lambda: mostrar_tokens(analizar_codigo(txt_codigo.get("1.0", tk.END))))
btn_analizar.grid(row=4, column=0, padx=10, pady=5, columnspan=2)

# Ejecutar el bucle de eventos
root.mainloop()
