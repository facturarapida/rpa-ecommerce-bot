# -*- coding: utf-8 -*-
"""
RPA: monitor de precios automatizado.

Antes (a mano): un empleado abria la tienda, buscaba cada producto,
leia el precio de cada libro y lo apuntaba en una hoja de calculo.
30 min/dia, con errores de tecleo.

Despues (este script): el mismo recorrido lo hace un navegador
autonomo (Selenium + Chrome): abre el catalogo, recopila nombre /
precio / disponibilidad de los N primeros productos, abre el primero
para leer su descripcion completa, guarda el resultado en CSV y deja
una captura de pantalla como evidencia. 2 minutos, sin tocar el PC.

Uso:
    python rpa_demo.py                  # 10 productos por defecto
    python rpa_demo.py --limit 25       # 25 productos
    python rpa_demo.py --headed        # ver el navegador en accion
"""
import argparse
import csv
import datetime as dt
import pathlib
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://books.toscrape.com/"  # tienda demo publica y estable (hecha para ejercicios de scraping)
OUT = pathlib.Path(__file__).parent / "output"


def build_driver(headless: bool) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    # perfil propio: no choca con la sesion Chrome del usuario
    opts.add_argument("--user-data-dir=" + str(OUT / "chrome-profile"))
    return webdriver.Chrome(options=opts)


def collect_catalog(driver: webdriver.Chrome, limit: int) -> list[dict]:
    """Recorrido manual automatizado: leer el catalogo fila a fila."""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_pod")))
    rows = []
    for card in driver.find_elements(By.CLASS_NAME, "product_pod")[:limit]:
        name = card.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
        price = card.find_element(By.CLASS_NAME, "price_color").text.strip()
        avail = ""
        try:
            avail = card.find_element(By.CLASS_NAME, "availability").text.replace("\n", " ").strip()
        except Exception:
            pass
        rows.append({"producto": name, "precio": price, "disponibilidad": avail})
    return rows


def first_product_details(driver: webdriver.Chrome) -> dict:
    """Abre la ficha del primer producto (como lo haria el empleado) y la lee."""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_pod")))
    first = driver.find_elements(By.CLASS_NAME, "product_pod")[0]
    # navegamos por el href del enlace (los clics directos los intercepta el sitio)
    href = first.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
    driver.get(href)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    title = driver.find_element(By.TAG_NAME, "h1").text
    # la descripcion es el <p> mas largo de la ficha
    desc = ""
    for p in driver.find_elements(By.TAG_NAME, "p"):
        t = p.text.strip()
        if len(t) > len(desc):
            desc = t
    return {"producto": title, "descripcion": desc}


def main() -> int:
    ap = argparse.ArgumentParser(description="RPA monitor de precios")
    ap.add_argument("--limit", type=int, default=10, help="num. de productos del catalogo (defecto: 10)")
    ap.add_argument("--headed", action="store_true", help="mostrar el navegador")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    stamp = dt.date.today().isoformat()
    csv_path = OUT / f"precios_{stamp}.csv"
    shot_path = OUT / f"evidencia_{stamp}.png"

    driver = build_driver(headless=not args.headed)
    rows, detail = [], None
    try:
        rows = collect_catalog(driver, args.limit)
        detail = first_product_details(driver)
        driver.save_screenshot(str(shot_path))
    except Exception as exc:  # noqa: BLE001 - reportar y salir con codigo
        print(f"FALLO: {exc}", file=sys.stderr)
        return 1
    finally:
        driver.quit()

    if not rows:
        print("FALLO: no se recopero ningun producto", file=sys.stderr)
        return 1

    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["fecha", "producto", "precio", "disponibilidad"])
        w.writeheader()
        for r in rows:
            w.writerow({"fecha": stamp, **r})

    print(f"OK  {len(rows)} productos recopilados del catalogo")
    print(f"CSV  {csv_path}")
    print(f"PNG  {shot_path}")
    print(f"DETALLE  {detail['producto']}: {detail['descripcion'][:80]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
