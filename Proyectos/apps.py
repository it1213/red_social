import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import uuid
from flask import Flask, render_template

app = Flask(__name__)

# Definir una función para generar usuarios aleatorios
def generar_usuario():
    return {
        'id': uuid.uuid4().hex,  # Asignar un ID único a cada usuario
        'nombre': f'Usuario_{random.randint(1, 100)}',
        'intereses': random.sample(['Deportes', 'Música', 'Tecnología', 'Arte', 'Cocina'], random.randint(1, 3))
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

# Generar un nuevo usuario con un único interés
nuevo_usuario = generar_usuario()
print("Nuevo usuario:")
print(nuevo_usuario)

# Elegir un interés aleatorio del nuevo usuario
interes_nuevo_usuario = random.choice(nuevo_usuario['intereses'])

# Crear un subgrafo con los usuarios que comparten el mismo interés del nuevo usuario
subgrafo = G.subgraph([nodo for nodo, datos in G.nodes(data=True) if interes_nuevo_usuario in datos['intereses']])

# Aplicar el algoritmo de Kruskal para encontrar el árbol de expansión mínima del subgrafo
arbol_expansion_minima = nx.minimum_spanning_tree(subgrafo)

# Obtener lista de usuarios del subgrafo
lista_usuarios_subgrafo = [datos for nodo, datos in subgrafo.nodes(data=True)]

# Asignar IDs únicos a los usuarios que no tienen
for usuario in lista_usuarios_subgrafo:
    if 'id' not in usuario:
        usuario['id'] = uuid.uuid4().hex

@app.route('/usuarios')
def mostrar_usuarios():
    # Renderizar la página HTML con la lista de usuarios del subgrafo
    return render_template('usuarios2.html', usuarios=lista_usuarios_subgrafo)

if __name__ == "__main__":
    app.run(debug=True)
