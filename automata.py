from graphviz import Digraph

def crear_automata():
    # Crear un nuevo gráfico dirigido
    dot = Digraph(comment='Autómata del Analizador Léxico de Andromeda')

    # Agregar estados
    dot.node('A', 'Inicio')
    dot.node('B', 'Identificador/Palabra Reservada')
    dot.node('C', 'Número')
    dot.node('D', 'Cadena')
    dot.node('E', 'Operador')
    dot.node('F', 'Comentario de Línea')
    dot.node('G', 'Comentario de Bloque')
    dot.node('H', 'Espacio')

    # Agregar transiciones
    dot.edge('A', 'B', 'letra')
    dot.edge('B', 'B', 'letra | dígito | _')
    dot.edge('A', 'C', 'dígito')
    dot.edge('C', 'C', 'dígito')
    dot.edge('C', 'C', '.')
    dot.edge('A', 'D', '"')
    dot.edge('D', 'D', 'cualquier cosa excepto " no escapada')
    dot.edge('D', 'A', '"')
    dot.edge('A', 'E', 'operador')
    dot.edge('A', 'F', '//')
    dot.edge('F', 'F', 'todo hasta \n')
    dot.edge('A', 'G', '/*')
    dot.edge('G', 'G', 'todo hasta */')
    dot.edge('A', 'H', 'espacio')
    dot.edge('H', 'A', 'no espacio')

    # Renderizar y visualizar el gráfico
    dot.render('automata.gv', view=True)

# Llamar a la función para crear y visualizar el autómata
crear_automata()
