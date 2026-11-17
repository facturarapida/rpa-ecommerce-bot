# Guia de selectores para adaptar el bot

Como encontrar los selectores CSS que hay que cambiar para cada sitio objetivo.

## Paso a paso

1. Abre la pagina en Chrome → F12 (DevTools) → pestana **Elements**.
2. Haz clic en el icono de "seleccionar elemento" (o pulsa `Ctrl+Shift+C`) y toca el dato que quieres extraer (p. ej. el precio).
3. DevTools resalta el nodo. Busca un **atributo estable**:
   - `id="..."` → mejor: `#precio`
   - `class="..."` → `div.precio`
   - si solo hay un `data-*` propio: `[data-testid="precio"]`
4. **Evita** selectores por posicion (`div > div > span`) y classes generadas (`css-1a2b3c`) — rompen con cualquier rediseño.
5. En el navegador, prueba desde la consola (pestaña **Console**):

   ```js
   document.querySelector('.precio').textContent.trim()
   ```

6. Tradúcelo a Selenium:

   ```python
   from selenium.webdriver.common.by import By
   precio = driver.find_element(By.CSS_SELECTOR, ".precio").text.strip()
   ```

## Selectores usados en este repo (books.toscrape.com)

| Dato | Selector |
|------|----------|
| Tarjeta de producto | `By.CLASS_NAME, "product_pod"` |
| Nombre | `card.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")` |
| Precio | `By.CLASS_NAME, "price_color"` |
| Disponibilidad | `By.CLASS_NAME, "availability"` (dentro de la tarjeta) |
| Enlace ficha | `card.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")` |
| Titulo ficha | `By.TAG_NAME, "h1"` |
| Descripcion | el `<p>` mas largo de la pagina |

## Buena practica anti-bloqueo

* Rota `User-Agent` (opcion Chrome `--user-agent=...`).
* `time.sleep(random.uniform(1, 3))` entre peticiones.
* Respeta `robots.txt` y los terminos del sitio.
* Para paginas grandes, limita el volumen y agenda en horario bajo.
