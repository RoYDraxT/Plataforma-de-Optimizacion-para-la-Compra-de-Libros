from flask import Flask, render_template, request
from scraping import buscar_precios

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre_libro = request.form['nombre_libro']
    
    resultados = buscar_precios(nombre_libro)
    
    return render_template('resultados.html', resultados=resultados)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
