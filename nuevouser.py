import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Definir una función para generar un usuario aleatorio con un único interés
def generar_usuario():
    return {
        'id': random.randint(1001, 2000),
        'nombre': f'Nuevo_Usuario_{random.randint(1, 100)}',
        'intereses': [random.choice(['Deportes', 'Música', 'Tecnología', 'Arte', 'Cocina'])]
    }

# Generar un nuevo usuario aleatorio
nuevo_usuario = generar_usuario()
print("Nuevo usuario:")
print(nuevo_usuario)

# Crear un grafo utilizando NetworkX
G = nx.Graph()

# Agregar nodos al grafo con los usuarios
for _, usuario in df_usuarios.iterrows():
    G.add_node(usuario['id'], nombre=usuario['nombre'], intereses=usuario['intereses'])

# Agregar el nuevo usuario al grafo
G.add_node(nuevo_usuario['id'], nombre=nuevo_usuario['nombre'], intereses=nuevo_usuario['intereses'])

# Establecer conexiones entre usuarios con intereses similares
for i, usuario1 in df_usuarios.iterrows():
    for j, usuario2 in df_usuarios.iterrows():
        if i != j:
            intereses_comunes = set(usuario1['intereses']).intersection(usuario2['intereses'])
            if intereses_comunes:
                G.add_edge(usuario1['id'], usuario2['id'], intereses_comunes=intereses_comunes)

# Visualizamos el grafo
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)  # Layout para posicionar los nodos
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, edge_color='gray', linewidths=1, font_size=10)

# Añadimos etiquetas de intereses a los nodos
for node, (x, y) in pos.items():
    intereses_usuario = ', '.join(df_usuarios[df_usuarios['id'] == node]['intereses'].iloc[0])
    plt.text(x, y + 0.05, intereses_usuario, fontsize=8, ha='center')

# Añadimos etiquetas de intereses al nuevo usuario
plt.text(pos[nuevo_usuario['id']][0], pos[nuevo_usuario['id']][1] + 0.05,
         ', '.join(nuevo_usuario['intereses']), fontsize=8, ha='center')

plt.title("Red de Usuarios con Intereses Comunes y Nuevo Usuario")
plt.show()
