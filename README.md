## <div align="center">Universidad Nacional Agraria La Molina</div> 

<div align="center">
  <img src="https://www.lamolina.edu.pe/portada/html/acerca/escudos/download/color/1193x1355_ESCUDOCOLOR.png" alt="Logo de la Universidad Nacional Agraria La Molina" width="200">
</div>
<div align="center"><b>Facultad de Economía y Planificación</b></div>  
<div align="center"><b>Departamento Académico de Estadística Informática</b></div>  

# <div align="center">Plataforma de Obtimización para la Compra de Libros</div>
---

## Propuesta
Crear una página web que recopile información sobre el precio de algún libro específico en distintas páginas dedicadas al comercio de libros digitales y/o físicos. La página web a realizar será capaz de identificar cuál es la tienda que tiene un precio más bajo y, al mismo tiempo, mostrar el resto de opciones en donde el libro se encuentra disponible.

---

## Motivación
Los estudiantes comúnmente pueden pasar varias horas buscando el libro que deseen en diferentes tiendas digitales con el fin de comprar al precio más bajo, lo que provoca una pérdida de tiempo al tener que rebuscar entre las distintas opciones. Una página web como la que se desea desarrollar podría reducir el tiempo de búsqueda para los estudiantes y brindar el precio más bajo o la mejor oferta de una manera más rápida.

---

## Propósito
El fin del presente proyecto es brindar una herramienta de consulta digital que proporcione al usuario todas las opciones disponibles que tiene para comprar el libro de su interés, haciendo énfasis en aquella que muestre un precio más bajo.

---

## Objetivos

- **Objetivo general:**  
  Desarrollar una página web que permita a los usuarios buscar libros específicos y comparar sus precios en diferentes tiendas digitales, identificando la opción con el precio más bajo y mostrando todas las alternativas disponibles.

- **Objetivos específicos:**  
  - Diseñar un sistema de recopilación de datos automatizado, utilizando web scraping o APIs, que obtenga información actualizada sobre precios y disponibilidad de libros en diversas plataformas.  
  - Implementar una interfaz web intuitiva y accesible que facilite la búsqueda de libros y permita visualizar los precios y opciones disponibles de forma clara y ordenada.

---

## Fuente de datos

- **Tienda Crisol:**  
  [https://www.crisol.com.pe](https://www.crisol.com.pe/?srsltid=AfmBOop6vGsTKzJtnKU7UUfSdjkBEOgY_fFwvViFn_FwiRxUGlo3bzqp)

- **Tienda Ibero Librerías:**  
  [https://www.iberolibrerias.com](https://www.iberolibrerias.com/)

- **Tienda Buscalibre:**  
  [https://www.buscalibre.pe](https://www.buscalibre.pe/)

- **Tienda Librería Internacional:**  
  [https://www.sbs.com.pe](https://www.sbs.com.pe/)

- **Otros...**

---

## Webscraping

Este script permite buscar y comparar precios de libros en tres plataformas de comercio electrónico en el Perú: **Crisol**, **SBS** y **La Familia**. A través de diferentes métodos de webscraping obtiene información como el título del libro, su precio, el enlace al producto, la tienda de origen y la URL de la imagen del producto.

### Tecnologías utilizadas
- **Librería BeautifulSoup**: Para analizar y extraer información del HTML de las páginas web.
- **Librería requests**: Para realizar solicitudes HTTP y obtener el contenido de las páginas web.

---

### Funciones principales

#### 1. `buscar_precio_libro_crisol(nombre_libro)`
Busca los precios del libro ingresado en la tienda **Crisol**:
- Construye la URL de búsqueda reemplazando los espacios en el nombre del libro con "+".
- Realiza una solicitud HTTP GET con un encabezado de usuario definido para evitar bloqueos por bots.
- Analiza la respuesta HTML para encontrar los libros en contenedores con la clase `product-item-info`.
- Extrae los detalles del libro (título, precio, enlace, URL de la imagen).
- Devuelve una lista de hasta 5 resultados.

**Fragmento de código:**
```python
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
```

#### 2. `buscar_precio_libro_sbs(nombre_libro)`
Realiza la búsqueda en la tienda **SBS**:
- Construye y utiliza una URL similar a Crisol pero con el formato propio de SBS.
- Realiza la solicitud y procesa la respuesta HTML para encontrar los contenedores de productos.
- Extrae los mismos datos que en Crisol (título, precio, enlace, URL de la imagen).
- Devuelve una lista de resultados o un mensaje en caso de error.

**Fragmento de código:**
```python
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
```

#### 3. `buscar_precio_libro_la_familia(nombre_libro)`
Realiza la búsqueda en la tienda **La Familia**:
- Construye la URL con el formato de búsqueda específico de esta tienda, incluyendo `post_type=product`.
- Procesa la respuesta para encontrar los contenedores de productos y extrae los datos necesarios.
- Devuelve una lista de resultados o un mensaje si no encuentra productos.

**Fragmento de código:**
```python
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
```

#### 4. `buscar_precios(nombre_libro)`
Función principal que consolida los resultados de las tres tiendas:
- Llama a las funciones específicas de Crisol, SBS y La Familia.
- Combina los resultados de todas las tiendas en una lista única.
- Ordena la lista de resultados por precio (extrayendo el valor numérico de la cadena de texto del precio).

**Fragmento de código:**
```python
def buscar_precios(nombre_libro):
    resultados_crisol = buscar_precio_libro_crisol(nombre_libro)
    resultados_sbs = buscar_precio_libro_sbs(nombre_libro)
    resultados_la_familia = buscar_precio_libro_la_familia(nombre_libro)

    resultados_combined = resultados_crisol + resultados_sbs + resultados_la_familia
    resultados_sorted = sorted(resultados_combined, key=lambda x: float(x["precio"].replace("S/", "").replace(",", "")))

    return resultados_sorted
```

---

### Ejemplo de uso

1. Importar las funciones y librerías necesarias.
2. Llamar a la función `buscar_precios(nombre_libro)` pasando el nombre del libro como argumento. Por ejemplo:

```python
resultados = buscar_precios("Cien años de soledad")
for libro in resultados:
    print(libro)
```

**Salida esperada:**
Una lista de diccionarios con información como:

{'titulo': 'CIEN AÑOS DE SOLEDAD', 'precio': 'S/ 59.00', 'link': 'https://www.crisol.com.pe/libro-cien-anos-soledad-9786124262784', 'tienda': 'Crisol', 'imagen': 'https://www.crisol.com.pe/media/catalog/product/cache/597531f9de47f5e5225ef01cbe4bbd93/9/7/9786124262784_ef8rc4mqeziackm5.jpg'}

{'titulo': 'CIEN AÑOS DE SOLEDAD', 'precio': 'S/\xa059.00', 'link': 'https://www.sbs.com.pe/cien-anos-de-soledad-9786124262784.html', 'tienda': 'SBS', 'imagen': 'https://www.sbs.com.pe/media/catalog/product/9/7/978-6124262784.jpg?quality=80&bg-color=255,255,255&fit=bounds&height=470&width=360&canvas=360:470'}

---

### Consideraciones

1. **Errores de conexión:** Si no es posible acceder a una tienda, la función devuelve un mensaje de error específico.
2. **Resultados limitados:** Cada tienda devuelve un máximo de 5 resultados.
3. **Formato de precios:** El código asume que los precios están en soles peruanos (S/).
4. **Estructura HTML variable:** Si las páginas web cambian su estructura, puede ser necesario actualizar las clases HTML usadas en el scraping.

---

### Requisitos previos

1. Instalar las dependencias necesarias ejecutando:
    ```bash
    pip install beautifulsoup4 requests
    ```
2. Verificar la conexión a internet para realizar las solicitudes HTTP.

---

