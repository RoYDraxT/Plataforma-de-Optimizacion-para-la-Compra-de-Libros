from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from scraping import buscar_precio_libro_crisol

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre_libro = request.form['nombre_libro']
    
    # Llamadas a funciones de scraping
    resultados_crisol = buscar_precio_libro_crisol(nombre_libro)
    
    # Combina todos los resultados
    resultados = resultados_crisol
    
    return render_template('resultados.html', resultados=resultados)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
