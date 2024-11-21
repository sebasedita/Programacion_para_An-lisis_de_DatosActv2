# Código para extraer datos de Amazon
# Instala las dependencias necesarias
!apt-get update
!apt-get install -y chromium-chromedriver

# Configuración de variables de entorno
import os
os.environ["PATH"] += ":/usr/lib/chromium-browser/"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configurar opciones de Chrome en modo headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Inicializar el WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL de una categoría específica en Amazon
url_categoria = "https://www.amazon.com/s?k=laptops"
driver.get(url_categoria)

# Esperar a que la página cargue completamente
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
    )

    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")
    productos = soup.find_all("div", class_="s-result-item")

    productos_datos = []
    for producto in productos:
        nombre = producto.find("span", class_="a-size-medium")
        nombre = nombre.get_text(strip=True) if nombre else "No disponible"

        precio = producto.find("span", class_="a-offscreen")
        precio = precio.get_text(strip=True) if precio else "No disponible"

        enlace = producto.find("a", class_="a-link-normal")
        enlace = f"https://www.amazon.com{enlace['href']}" if enlace else "No disponible"

        productos_datos.append({
            "nombre": nombre,
            "precio": precio,
            "enlace": enlace
        })

    for idx, producto in enumerate(productos_datos):
        print(f"Producto {idx + 1}:")
        print(f"Nombre: {producto['nombre']}")
        print(f"Precio: {producto['precio']}")
        print(f"Enlace: {producto['enlace']}")
        print("-" * 40)

except Exception as e:
    print("Error al extraer información:", e)

driver.quit()
