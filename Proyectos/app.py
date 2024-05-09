import pandas as pd
import networkx as nx
import random
from faker import Faker
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt

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
            posibles_amigos.append(G.nodes[node])

# Crear un entorno de Jinja2 con la ruta específica al directorio que contiene la plantilla
file_loader = FileSystemLoader('C:/Users/itzco/OneDrive/Documentos/GitHub/red_social/templates')
env = Environment(loader=file_loader)

# Cargar la plantilla HTML
template = env.get_template('friends.html')

# Renderizar la plantilla con los datos de los posibles amigos
output = template.render(posibles_amigos=posibles_amigos)

# Guardar el HTML renderizado en un archivo friends.html
with open('friends.html', 'w') as f:
    f.write(output)

# Ahora, agregamos el redireccionamiento al archivo friends.html
redirect_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting to Friends</title>
</head>
<body>
    <script>
        // Redireccionar automáticamente a friends.html después de 3 segundos
        setTimeout(function() {
            window.location.href = "http://127.0.0.1:5500/templates/friends.html";
        }, 3000); // Cambiar el valor a 3000 para redirigir después de 3 segundos
    </script>
    <p>Redirecting to Friends...</p>
</body>
</html>
"""

# Guardar el código de redireccionamiento en un archivo redirect.html
with open('redirect.html', 'w') as f:
    f.write(redirect_code)

print("Se ha generado el archivo 'friends.html' con la lista de posibles amigos.")
print("Se ha generado el archivo 'redirect.html' para redireccionar a friends.html.")

# Dibujar el grafo
plt.figure(figsize=(10, 8))
nx.draw(subgrafo, with_labels=True, font_weight='bold')
plt.title("Subgrafo de Posibles Amigos")
plt.show()
