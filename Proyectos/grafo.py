import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from faker import Faker

# Crear una instancia de Faker
faker = Faker()

# Número de usuarios
num_usuarios = 200

# Generar una lista de nombres ficticios
nombres = [faker.name() for _ in range(num_usuarios)]

# Definir una función para generar usuarios aleatorios
def generar_usuario():
    return {
        'nombre': random.choice(nombres),
        'intereses': random.sample(['Deportes', 'Música', 'Tecnología', 'Arte', 'Cocina', 'Animales'], random.randint(1, 3))
    }

# Generar usuarios aleatorios
usuarios = [generar_usuario() for _ in range(num_usuarios)]

# Crear un DataFrame de Pandas con la información de los usuarios
df_usuarios = pd.DataFrame(usuarios)

# Crear un grafo utilizando NetworkX
G = nx.Graph()

# Agregar nodos al grafo con los usuarios
for _, usuario in df_usuarios.iterrows():
    G.add_node(usuario['nombre'], intereses=usuario['intereses'])

# Establecer conexiones entre usuarios con intereses similares
for nombre1, datos1 in G.nodes(data=True):
    for nombre2, datos2 in G.nodes(data=True):
        if nombre1 != nombre2:
            intereses_comunes = set(datos1['intereses']).intersection(datos2['intereses'])
            if intereses_comunes:
                G.add_edge(nombre1, nombre2, intereses_comunes=intereses_comunes)

# Generar un nuevo usuario con un único interés
nuevo_usuario = generar_usuario()
print("Nuevo usuario:")
print(nuevo_usuario)

# Elegir un interés aleatorio del nuevo usuario
interes_nuevo_usuario = random.choice(nuevo_usuario['intereses'])

# Crear un subgrafo con los usuarios que comparten el mismo interés del nuevo usuario
subgrafo = G.subgraph([nombre for nombre, datos in G.nodes(data=True) if interes_nuevo_usuario in datos['intereses']])

# Aplicar el algoritmo de Kruskal para encontrar el árbol de expansión mínima del subgrafo
arbol_expansion_minima = nx.minimum_spanning_tree(subgrafo)

# Crear una lista enlazada con los nodos del árbol de expansión mínima
lista_enlazada = list(nx.dfs_edges(arbol_expansion_minima))

# Imprimir los nodos en la lista enlazada
print("Lista enlazada:")
for edge in lista_enlazada:
    print(edge[0], "->", edge[1])

# Visualizar el árbol de expansión mínima
plt.figure(figsize=(10, 6))
pos_arbol = nx.spring_layout(arbol_expansion_minima)  # Layout para posicionar los nodos del árbol
nx.draw(arbol_expansion_minima, pos_arbol, with_labels=True, node_color='skyblue', node_size=3000, edge_color='gray', linewidths=1, font_size=10)

# Añadir etiquetas de intereses a los nodos del árbol
for node, (x, y) in pos_arbol.items():
    intereses_usuario = ', '.join(arbol_expansion_minima.nodes[node]['intereses'])
    plt.text(x, y + 0.05, intereses_usuario, fontsize=8, ha='center')

plt.title(f"Árbol de Expansión Mínima para Usuarios con Interés en {interes_nuevo_usuario}")
plt.show()
