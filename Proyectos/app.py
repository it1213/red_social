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
num_usuarios = 150
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

# Visualizamos el grafo
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)  # Layout para posicionar los nodos

# Dibujar los nodos
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=3000)

# Dibujar las relaciones (edges)
nx.draw_networkx_edges(G, pos, edge_color='magenta', width=0.5)

# Añadimos etiquetas de nombres, edades e intereses de usuario a los nodos
for node, (x, y) in pos.items():
    usuario_info = df_usuarios[df_usuarios['id'] == node]
    nombre_usuario = usuario_info['nombre'].iloc[0]
    edad_usuario = usuario_info['edad'].iloc[0]
    intereses_usuario = ', '.join(usuario_info['intereses'].iloc[0])
    etiqueta = f"{nombre_usuario}\nEdad: {edad_usuario}\nIntereses: {intereses_usuario}"
    plt.text(x, y, etiqueta, fontsize=8, ha='center')

plt.title("Red de Usuarios con Intereses Comunes")
plt.axis('off')  # Ocultar los ejes

# Guardar la imagen en el directorio static
plt.savefig('Proyectos/static/red_usuarios_intereses_comunes.png')

# Mostrar el grafo
plt.show()