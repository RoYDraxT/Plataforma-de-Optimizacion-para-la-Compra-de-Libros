from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from scraping import buscar_precio_libro_crisol, buscar_precio_libro_sbs, buscar_precio_libro_la_familia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre_libro = request.form['nombre_libro']
    
    # Llamadas a funciones de scraping
    resultados_crisol = buscar_precio_libro_crisol(nombre_libro)
    resultados_sbs = buscar_precio_libro_sbs(nombre_libro)
    resultados_familia = buscar_precio_libro_la_familia(nombre_libro)

    # Combina todos los resultados
    resultados = resultados_crisol + resultados_sbs + resultados_familia
    
    return render_template('resultados.html', resultados=resultados)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
