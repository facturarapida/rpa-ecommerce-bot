# rpa-ecommerce-bot

**RPA: monitor de precios y catalogo automatizado** — automatiza el trabajo manual de "apuntar precios en Excel" usando un navegador autonomo (Selenium + Chrome).

## El problema que resuelve

Un empleado de una tienda online pasaba 30 min/dia abriendo la tienda, leyendo cada producto y apuntando el precio en una hoja de calculo. Con errores de tecleo, sin evidencia, y sin forma de auditar el trabajo.

## La solucion (este repo)

`rpa_demo.py` reproduce el recorrido manual de forma autonomo:

1. Abre el catalogo (tienda demo publica `books.toscrape.com`, estable y sin bloqueos).
2. Recopila **nombre / precio / disponibilidad** de los N primeros productos.
3. Abre la ficha del primero y lee el titulo + descripcion completa.
4. Guarda el resultado en **CSV** (UTF-8-BOM, listo para Excel) y una **captura de pantalla** como evidencia.
5. Salida con codigo de error si algo falla (idempotente, seguro para programar con cron/Task Scheduler).

## Ejecucion

```bash
pip install selenium   # Selenium >= 4 descarga solo el chromedriver
python rpa_demo.py --limit 25
```

Opciones:
- `--limit N` — cuantos productos del catalogo leer (defecto 10).
- `--headed` — ver el navegador en accion (por defecto es headless).

## Resultado real (ejecucion del 2026-11-17)

```
OK  10 productos recopilados del catalogo
CSV  output/precios_2026-11-17.csv
PNG  output/evidencia_2026-11-17.png
DETALLE  A Light in the Attic: It's hard to imagine a world without A Light...
```

`output/precios_2026-11-17.csv`:

| fecha        | producto               | precio | disponibilidad |
|--------------|------------------------|--------|---------------|
| 2026-11-17   | A Light in the Attic   | £51.77 | In stock      |
| 2026-11-17   | Tipping the Velvet     | £53.74 | In stock      |
| 2026-11-17   | Soumission             | £50.10 | In stock      |
| ...          | (7 mas)                |        |               |

## Que se automatiza (vs. manual)

| Tarea | Manual | Con este repo |
|-------|--------|---------------|
| Abrir tienda | empleado | Selenium |
| Leer N precios | a mano | DOM `product_pod` |
| Leer descripcion | copiar | `<p>` mas largo |
| Guardar en Excel | teclear | CSV UTF-8-BOM |
| Evidencia | ninguna | screenshot PNG |
| Error de tecleo | ~5% | 0% |
| Duracion | ~30 min | ~2 min |

## Adaptar a tu negocio

El codigo esta pensado para que se adapte en 3 pasos:

1. Cambiar `BASE` (linea 33) por la URL de tu tienda/portal.
2. Ajustar los selectores CSS de `collect_catalog()` y `first_product_details()` (ver [selector-guia.md](selector-guia.md)).
3. Sustituir `OUT / f"precios_{stamp}.csv"` por el destino que necesites (SharePoint, mail, API...).

## Dependencias

- Python >= 3.10
- `selenium>=4` (baja solo el `chromedriver` de la version de Chrome instalada)
- Chrome o Chromium en el sistema

## Licencia

MIT — uso libre para proyectos internos o como punto de partida para automatizaciones propias.
