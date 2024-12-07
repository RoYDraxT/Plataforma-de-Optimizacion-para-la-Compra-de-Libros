from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre_libro = request.form['nombre_libro']
    resultados = buscar_precio_libro(nombre_libro)
    return render_template('resultados.html', resultados=resultados)

def buscar_precio_libro(nombre_libro):
    url_base = "https://www.crisol.com.pe/catalogsearch/result/?q="
    nombre_libro = nombre_libro.replace(" ", "+")
    url = f"{url_base}{nombre_libro}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return [{"titulo": "Error", "precio": "Error", "link": "Error"}]
    
    soup = BeautifulSoup(response.text, "html.parser")
    libros = soup.find_all("div", class_="product-item-info")
    
    if not libros:
        return [{"titulo": "No se encontraron resultados", "precio": "", "link": ""}]
    
    resultados = []
    for libro in libros[:5]:  # Tomar los primeros 5 resultados
        titulo = libro.find("a", class_="product-item-link").text.strip()
        precio = libro.find("span", class_="price").text.strip()
        link = libro.find("a", class_="product-item-link")["href"]
        resultados.append({"titulo": titulo, "precio": precio, "link": link})
    
    return resultados

if __name__ == '__main__':
    app.run(debug=True, port=5000)
