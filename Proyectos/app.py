import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from faker import Faker

# Crear una instancia de Faker
faker = Faker()

# Definir una función para generar usuarios aleatorios con nombres aleatorios
def generar_usuario():
    edad = random.randint(1, 100)  # Generar una edad entre 1 y 100 años
    if 10 <= edad <= 20:
        edad = random.randint(10, 20)
    elif 21 <= edad <= 30:
        edad = random.randint(21, 30)
    else:
        edad = random.randint(31, 60)
        
    return {
        'id': random.randint(1, 1000),
        'nombre': faker.name(),
        'edad': edad,
        'activo': random.choice([True, False]),  # Determinar si el usuario es activo o no
        'intereses': random.sample(['Deportes', 'Música', 'Tecnología', 'Arte', 'Cocina'], random.randint(1, 4))
    }

# Definir la probabilidad de conexión aleatoria entre usuarios (de 0 a 1)
probabilidad_conexion = 0.5

# Generar una lista de 150 usuarios aleatorios
num_usuarios = 100
usuarios = [generar_usuario() for _ in range(num_usuarios)]

# Crear un DataFrame de Pandas con la información de los usuarios
df_usuarios = pd.DataFrame(usuarios)

# Crear un grafo utilizando NetworkX
G = nx.Graph()

# Agregar nodos al grafo con los usuarios
for _, usuario in df_usuarios.iterrows():
    G.add_node(usuario['id'], nombre=usuario['nombre'], edad=usuario['edad'], activo=usuario['activo'], intereses=usuario['intereses'])

# Establecer conexiones aleatorias entre usuarios con una cierta probabilidad
for i, usuario1 in df_usuarios.iterrows():
    for j, usuario2 in df_usuarios.iterrows():
        if i != j:
            if random.random() <= probabilidad_conexion:
                G.add_edge(usuario1['id'], usuario2['id'])

# Crear el subgrafo con el nuevo usuario y sus conexiones
nuevo_usuario_id = max(G.nodes()) + 1
nuevo_usuario = generar_usuario()
G.add_node(nuevo_usuario_id, nombre=nuevo_usuario['nombre'], edad=nuevo_usuario['edad'], activo=nuevo_usuario['activo'], intereses=nuevo_usuario['intereses'])

# Conectar el nuevo usuario con algunos usuarios existentes
for node in G.nodes():
    if random.random() <= probabilidad_conexion:
        G.add_edge(nuevo_usuario_id, node)

subgrafo = nx.subgraph(G, [nuevo_usuario_id] + list(G.neighbors(nuevo_usuario_id)))

# Imprimir la información del nuevo usuario en la consola
print("Información del Nuevo Usuario:")
print(f"ID: {nuevo_usuario_id}")
print(f"Nombre: {nuevo_usuario['nombre']}")
print(f"Edad: {nuevo_usuario['edad']}")
print(f"Activo: {'Sí' if nuevo_usuario['activo'] else 'No'}")
print("Intereses:", ', '.join(nuevo_usuario['intereses']))
print()

# Filtrar y clasificar la lista de posibles amigos en función de diferentes criterios
posibles_amigos = []
for node in G.nodes():
    if node != nuevo_usuario_id and not G.has_edge(nuevo_usuario_id, node):  # Solo considerar nodos que no sean el nuevo usuario y que no estén ya conectados
        if G.nodes[node]['activo']:  # Solo considerar usuarios activos
            posibles_amigos.append(node)

# Imprimir la lista de posibles amigos
print("Lista de Posibles Nuevos Amigos:")
for amigo in posibles_amigos:
    usuario_info = G.nodes[amigo]
    nombre_amigo = usuario_info['nombre']
    edad_amigo = usuario_info['edad']
    activo_amigo = usuario_info['activo']
    intereses_amigo = ', '.join(usuario_info['intereses'])
    print(f"ID: {amigo}, Nombre: {nombre_amigo}, Edad: {edad_amigo}, Activo: {'Sí' if activo_amigo else 'No'}, Intereses: {intereses_amigo}")

# Visualizar el subgrafo
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(subgrafo)

# Dibujar los nodos y las aristas
node_colors = ['lightblue' if node == nuevo_usuario_id else 'red' if not G.nodes[node]['activo'] else 'lightgreen' for node in subgrafo.nodes()]
nx.draw(subgrafo, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=8)
nx.draw_networkx_edges(subgrafo, pos, edge_color='magenta', width=0.5)

# Añadir etiquetas de nombres, edades, estado de actividad e intereses de usuario a los nodos
for node, (x, y) in pos.items():
    usuario_info = G.nodes[node]
    nombre_usuario = usuario_info['nombre']
    edad_usuario = usuario_info['edad']
    activo_usuario = 'Activo' if usuario_info['activo'] else 'Inactivo'
    intereses_usuario = ', '.join(usuario_info['intereses'])
    etiqueta = f"{nombre_usuario}\nEdad: {edad_usuario}\nEstado: {activo_usuario}\nIntereses: {intereses_usuario}"
    plt.text(x, y, etiqueta, fontsize=8, ha='center')

plt.title("Subgrafo con Nuevo Usuario y Conexiones")
plt.axis('off')

# Mostrar el grafo
plt.show()
