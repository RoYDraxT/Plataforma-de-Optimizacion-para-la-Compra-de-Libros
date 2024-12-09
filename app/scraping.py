from bs4 import BeautifulSoup
import requests

def buscar_precio_libro_crisol(nombre_libro):
    url_base = "https://www.crisol.com.pe/catalogsearch/result/?q="
    nombre_libro = nombre_libro.replace(" ", "+")
    url = f"{url_base}{nombre_libro}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return [{"titulo": "Error al acceder a Crisol", "precio": "N/A", "link": "", "tienda": "Crisol"}]
    
    soup = BeautifulSoup(response.text, "html.parser")
    libros = soup.find_all("div", class_="product-item-info")
    
    if not libros:
        return [{"titulo": "No se encontraron resultados en Crisol", "precio": "N/A", "link": "", "tienda": "Crisol"}]
    
    resultados = []
    for libro in libros[:5]:
        try:
            titulo = libro.find("a", class_="product-item-link").text.strip()
            precio = libro.find("span", class_="price").text.strip()
            link = libro.find("a", class_="product-item-link")["href"]
            resultados.append({"titulo": titulo, "precio": precio, "link": link, "tienda": "Crisol"})
        except AttributeError:
            continue

    return resultados

def buscar_precio_libro_sbs(nombre_libro):
    url_base = "https://www.sbs.com.pe/catalogsearch/result/?q="
    nombre_libro = nombre_libro.replace(" ", "+")
    url = f"{url_base}{nombre_libro}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return [{"titulo": "Error al acceder a sbs", "precio": "N/A", "link": "Error", "tienda": "SBS"}]

    soup = BeautifulSoup(response.text, "html.parser")

    # Encuentra los resultados usando las clases inspeccionadas
    libros = soup.find_all("div", class_="product-item-info")

    if not libros:
        return [{"titulo": "No se encontraron resultados en SBS", "precio": "N/A", "link": "", "tienda": "SBS"}]

    resultados = []
    for libro in libros:
        try:
            titulo = libro.find("a", class_="product-item-link").text.strip()
            precio = libro.find("span", class_="price").text.strip()
            link = libro.find("a", class_="product-item-link")["href"]
            resultados.append({"titulo": titulo, "precio": precio, "link": link, "tienda": "SBS"})
        except AttributeError:
            continue  

    return resultados

def buscar_precio_libro_la_familia(nombre_libro):
    # Estandarizamos el input convirtiéndolo a minúsculas
    nombre_libro = nombre_libro.strip().lower()
    # Reemplazamos los espacios con '+' para formar una URL compatible con la página
    nombre_libro_url = nombre_libro.replace(" ", "+")
    
    # URL de búsqueda específica para La Familia
    url = f"https://lafamilia.com.pe/?s={nombre_libro_url}&post_type=product"
    
    # Realizamos la solicitud HTTP
    response = requests.get(url)
    
    # Verificamos que la respuesta sea exitosa
    if response.status_code != 200:
        print("Error al acceder a la página")
        return None
    
    # Analizamos el contenido HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscamos todos los productos en la página
    productos = soup.find_all('h3', class_='wd-entities-title')
    
    if not productos:
        print("No se encontraron resultados para el libro.")
        return None
    
    # Creamos una lista para almacenar los productos con nombre y precio
    lista_productos = []
    
    for producto in productos:  # Recorremos todos los productos encontrados
        # Intentamos extraer el nombre del libro
        nombre = producto.find('a')
        if nombre:
            nombre_libro = nombre.text.strip()
        
        # Intentamos extraer el precio del libro
        precio = producto.find_next('span', class_='woocommerce-Price-amount')
        if precio:
            precio_texto = precio.text.strip()
            # Extraemos solo el número del precio, eliminando la moneda
            precio_numero = float(precio_texto.replace('S/', '').strip())
        
            # Agregamos el producto con el precio como número
            lista_productos.append((nombre_libro, precio_texto, precio_numero))
    
    # Ordenamos los productos por el precio de menor a mayor
    lista_productos_ordenada = sorted(lista_productos, key=lambda x: x[2])
    
    # Retornamos los 3 productos con los precios más bajos
    return lista_productos_ordenada[:3]