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
        return [{"titulo": "Error al acceder a Crisol", "precio": "N/A", "link": "", "tienda": "Crisol", "imagen": ""}]
    
    soup = BeautifulSoup(response.text, "html.parser")
    libros = soup.find_all("div", class_="product-item-info")
    
    if not libros:
        return [{"titulo": "No se encontraron resultados en Crisol", "precio": "N/A", "link": "", "tienda": "Crisol", "imagen": ""}]
    
    resultados = []
    for libro in libros[:5]:
        try:
            titulo = libro.find("a", class_="product-item-link").text.strip()
            precio = libro.find("span", class_="price").text.strip()
            link = libro.find("a", class_="product-item-link")["href"]
            imagen_url = libro.find("img", class_="product-image-photo")["src"]
            resultados.append({
                "titulo": titulo,
                "precio": precio,
                "link": link,
                "tienda": "Crisol",
                "imagen": imagen_url
            })
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
        return [{"titulo": "Error al acceder a sbs", "precio": "N/A", "link": "Error", "tienda": "SBS", "imagen": ""}]

    soup = BeautifulSoup(response.text, "html.parser")

    # Encuentra los resultados usando las clases inspeccionadas
    libros = soup.find_all("div", class_="product-item-info")

    if not libros:
        return [{"titulo": "No se encontraron resultados en SBS", "precio": "N/A", "link": "", "tienda": "SBS", "imagen": ""}]

    resultados = []
    for libro in libros:
        try:
            titulo = libro.find("a", class_="product-item-link").text.strip()
            precio = libro.find("span", class_="price").text.strip()
            link = libro.find("a", class_="product-item-link")["href"]
            imagen_url = libro.find("img", class_="product-image-photo")["src"]
            resultados.append({
                "titulo": titulo,
                "precio": precio,
                "link": link,
                "tienda": "SBS",
                "imagen": imagen_url
            })
        except AttributeError:
            continue  
    
    return resultados

def buscar_precio_libro_la_familia(nombre_libro):
    url_base = "https://lafamilia.com.pe/?s="
    nombre_libro = nombre_libro.replace(" ", "+")
    url = f"{url_base}{nombre_libro}&post_type=product"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return [{"titulo": "Error al acceder a La Familia", "precio": "N/A", "link": "", "tienda": "La Familia", "imagen": ""}]

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.find_all("h3", class_="wd-entities-title")

    if not productos:
        return [{"titulo": "No se encontraron resultados en La Familia", "precio": "N/A", "link": "", "tienda": "La Familia", "imagen": ""}]

    resultados = []
    for producto in productos[:5]:
        try:
            titulo = producto.find("a").text.strip()
            precio = producto.find_next("span", class_="woocommerce-Price-amount").text.strip()
            link = producto.find("a")["href"]
            imagen_url = producto.find_previous("div", class_="product-wrapper").find("img")["src"]

            resultados.append({
                "titulo": titulo,
                "precio": precio,
                "link": link,
                "tienda": "La Familia",
                "imagen": imagen_url
            })
        except AttributeError:
            continue
    
    return resultados

def buscar_precios(nombre_libro):
    resultados_crisol = buscar_precio_libro_crisol(nombre_libro)
    resultados_sbs = buscar_precio_libro_sbs(nombre_libro)
    resultados_la_familia = buscar_precio_libro_la_familia(nombre_libro)

    resultados_combined = resultados_crisol + resultados_sbs + resultados_la_familia
    resultados_sorted = sorted(resultados_combined, key=lambda x: float(x["precio"].replace("S/", "").replace(",", "")))

    return resultados_sorted
