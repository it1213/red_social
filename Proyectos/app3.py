from flask import Flask, render_template
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import os

app = Flask(__name__)

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

# Guardar el grafo como imagen
grafo_imagen_path = "static/grafo.png"
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)  # Layout para posicionar los nodos
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, edge_color='gray', linewidths=1, font_size=10)
for node, (x, y) in pos.items():
    intereses_usuario = ', '.join(df_usuarios[df_usuarios['id'] == node]['intereses'].iloc[0])
    plt.text(x, y + 0.05, intereses_usuario, fontsize=8, ha='center')
plt.title("Red de Usuarios con Intereses Comunes")
plt.savefig(grafo_imagen_path)
plt.close()

# Ruta para renderizar la página HTML
@app.route('/')
def index():
    return render_template('index2.html', grafo_imagen_path=grafo_imagen_path)

if __name__ == "__main__":
    app.run(debug=True)
