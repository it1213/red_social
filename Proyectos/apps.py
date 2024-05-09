import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from faker import Faker

# Crear una instancia de Faker
faker = Faker()

# Definir una función para generar usuarios aleatorios con nombres aleatorios
def generar_usuario():
    return {
        'id': random.randint(1, 1000),
        'nombre': faker.name(),
        'edad': random.randint(10, 35),
        'intereses': random.sample(['Deportes', 'Música', 'Tecnología', 'Arte', 'Cocina'], random.randint(1, 3))
    }

# Generar una lista de 150 usuarios aleatorios
num_usuarios = 10
usuarios = [generar_usuario() for _ in range(num_usuarios)]

# Crear un DataFrame de Pandas con la información de los usuarios
df_usuarios = pd.DataFrame(usuarios)

# Crear un grafo utilizando NetworkX
G = nx.Graph()

# Agregar nodos al grafo con los usuarios
for _, usuario in df_usuarios.iterrows():
    G.add_node(usuario['id'], nombre=usuario['nombre'], edad=usuario['edad'], intereses=usuario['intereses'])

# Establecer conexiones entre usuarios con intereses similares
for i, usuario1 in df_usuarios.iterrows():
    for j, usuario2 in df_usuarios.iterrows():
        if i != j:
            intereses_comunes = set(usuario1['intereses']).intersection(usuario2['intereses'])
            if intereses_comunes:
                G.add_edge(usuario1['id'], usuario2['id'], intereses_comunes=intereses_comunes)

# Función para agregar un nuevo usuario al grafo y mostrar sus relaciones con otros usuarios basadas en intereses comunes
def mostrar_coincidencias_intereses_nuevo_usuario(grafo, nuevo_usuario):
    # Agregar el nuevo usuario al grafo
    grafo.add_node(nuevo_usuario['id'], nombre=nuevo_usuario['nombre'], edad=nuevo_usuario['edad'], intereses=nuevo_usuario['intereses'])

    # Calcular las relaciones del nuevo usuario con otros usuarios basadas en el grafo original
    relaciones_nuevo_usuario = [(u, v) for u, v, d in grafo.edges(nuevo_usuario['id'], data=True) if d['intereses_comunes']]

    # Mostrar las relaciones del nuevo usuario
    print(f"Relaciones del nuevo usuario {nuevo_usuario['nombre']} con otros usuarios basadas en intereses comunes:")
    for u, v in relaciones_nuevo_usuario:
        nombre_u = grafo.nodes[u]['nombre']
        nombre_v = grafo.nodes[v]['nombre']
        intereses_comunes = grafo.edges[u, v]['intereses_comunes']
        print(f"{nombre_u} - {nombre_v}: {intereses_comunes}")

    # Visualizar el subgrafo con el nuevo usuario y sus relaciones
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(grafo)  # Layout para posicionar los nodos

    # Dibujar los nodos
    nx.draw_networkx_nodes(grafo, pos, node_color='skyblue', node_size=3000)

    # Dibujar las relaciones (edges)
    nx.draw_networkx_edges(grafo, pos, edge_color='magenta', width=0.5)

    # Añadir etiquetas de nombres, edades e intereses de usuario a los nodos
    for node, (x, y) in pos.items():
        etiqueta = f"{grafo.nodes[node]['nombre']}\nEdad: {grafo.nodes[node]['edad']}\nIntereses: {', '.join(grafo.nodes[node]['intereses'])}"
        plt.text(x, y, etiqueta, fontsize=8, ha='center')

    plt.title("Subgrafo con Nuevo Usuario y Relaciones")
    plt.axis('off')  # Ocultar los ejes

    # Mostrar el subgrafo
    plt.show()

# Generar un nuevo usuario
nuevo_usuario = generar_usuario()

# Mostrar las relaciones del nuevo usuario con otros usuarios basadas en intereses comunes
mostrar_coincidencias_intereses_nuevo_usuario(G, nuevo_usuario)
