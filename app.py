from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    preferences = request.form['preferences']
    
    # Aquí puedes hacer lo que quieras con los datos del formulario,
    # como guardarlos en una base de datos, realizar operaciones,
    # redirigir a otra página, etc.
    
    # Por ahora, simplemente mostraremos los datos en la consola
    print("Nombre:", name)
    print("Edad:", age)
    print("Preferencias:", preferences)
    
    return "Formulario enviado correctamente"

if __name__ == '__main__':
    app.run(debug=True)
