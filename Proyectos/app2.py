import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Definir una función para generar usuarios aleatorios
def generar_usuario():
    return {
        'id': random.randint(1, 1000),
        'nombre': f'Usuario_{random.randint(1, 100)}',
        'intereses': random.sample(['Deportes', 'Música', 'Tecnología', 'Arte', 'Cocina',' '], random.randint(1, 3))
    }

# Generar una lista de 100 usuarios aleatorios
num_usuarios = 100
usuarios = [generar_usuario() for _ in range(num_usuarios)]

# Crear un DataFrame de Pandas con la información de los usuarios
df_usuarios = pd.DataFrame(usuarios)

# Crear un grafo utilizando NetworkX
G = nx.Graph()

# Agregar nodos al grafo con los usuarios
for _, usuario in df_usuarios.iterrows():
    G.add_node(usuario['id'], nombre=usuario['nombre'], intereses=usuario['intereses'])

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

plt.title("Red de Usuarios con Intereses Comunes")
plt.show()

