#!/usr/bin/env python3
"""
search_flaticon.py — Descarga un icono PNG de Flaticon dado su ID.

La BUSQUEDA se hace via Chrome DevTools MCP (no via este script):
el navegador ya cargado en la sesion puede acceder a flaticon.com sin bloqueos.
Este script solo maneja la DESCARGA del PNG una vez que el ID es conocido.

Uso:
    python search_flaticon.py <icon_id> <icon_name> <dest_dir>

Argumentos:
    icon_id     ID numerico del icono (ej. 5017903)
    icon_name   Nombre descriptivo para el archivo (ej. "cancer-ribbon")
    dest_dir    Carpeta donde guardar el PNG (ej. assets/)

Salida:
    JSON con: path (ruta del archivo guardado), url, attribution, size_bytes

Ejemplo:
    python search_flaticon.py 5017903 "cancer-ribbon" assets/
    → assets/cancer-ribbon-5017903.png

Como buscar iconos (flujo con Chrome DevTools MCP):
    1. mcp__chrome-devtools__new_page con URL:
       https://www.flaticon.com/search?word={TERMINO}&type=icon&style={ESTILO}&shape=fill
       Estilos validos: outline, fill, lineal-color, hand-drawn
       El parametro &shape=fill pre-filtra resultados a iconos fill en la interfaz de Flaticon,
       reduciendo candidatos incorrectos antes de la verificacion individual.
    2. mcp__chrome-devtools__wait_for con text=["icons", "results"]
    3. mcp__chrome-devtools__evaluate_script con este bloque JS para extraer resultados:

       () => {
         const icons = [];
         const seen = new Set();
         document.querySelectorAll('a[href*="/free-icon/"]').forEach(link => {
           const img = link.querySelector('img');
           if (!img) return;
           const m = link.href.match(/\\/free-icon\\/([^_]+)_(\\d+)$/);
           if (!m) return;
           const id = m[2];
           if (seen.has(id)) return;
           seen.add(id);
           const folder = id.length > 3 ? id.slice(0, -3) : id;
           const container = link.closest('li, article, [class*="icon-item"]') || link.parentElement;
           const styleText = container
             ? (container.querySelector('[class*="style"], [class*="pack"], span:not(:first-child)')?.innerText || '').trim()
             : '';
           icons.push({
             id,
             name: img.alt.trim().replace(/\\s+icon\\s*$/i, ''),
             style_hint: styleText,
             png_128: `https://cdn-icons-png.flaticon.com/128/${folder}/${id}.png`,
             png_512: `https://cdn-icons-png.flaticon.com/512/${folder}/${id}.png`,
             page_url: link.href
           });
         });
         return icons.slice(0, 10);
       }

    3b. Para cada candidato, verificar el estilo visitando su page_url antes de sugerirlo al usuario:

       mcp__chrome-devtools__navigate_page a la page_url del icono, luego:

       () => {
         // Flaticon expone el estilo como link justo después del StaticText "Style:"
         // Buscar el nodo de texto "Style:" y tomar el siguiente link hermano
         const allText = [...document.querySelectorAll('*')];
         const styleLabel = allText.find(el =>
           el.childNodes.length === 1 &&
           el.childNodes[0].nodeType === 3 &&
           el.childNodes[0].textContent.trim() === 'Style:'
         );
         if (styleLabel) {
           const next = styleLabel.nextElementSibling || styleLabel.parentElement?.querySelector('a[href*="/authors/"]');
           if (next) return next.innerText.trim();
         }
         // Fallback: buscar cualquier link que apunte a /authors/ con "basic" o "rounded" en href
         const styleLink = document.querySelector('a[href*="/authors/basic"], a[href*="/authors/basic-rounded"]');
         return styleLink ? styleLink.innerText.trim() : null;
       }

       Solo incluir el icono en la tabla final si el estilo coincide con el requerido por el sistema de diseño.
       Para el Observatorio del Cáncer el estilo requerido es "Basic Rounded Filled" — descartar
       cualquier icono cuyo estilo sea "Basic Rounded Lineal", "Outline", "Hand Drawn", etc.

    4. Mostrar resultados al usuario (nombre + png_128 como preview visual).
    5. Usuario elige ID → ejecutar este script para descargar.
    6. mcp__chrome-devtools__close_page para cerrar el tab.

Limitaciones:
    - Solo PNG disponible sin cuenta (128px preview, 512px descarga).
    - SVG requiere cuenta Premium de Flaticon.
    - Los iconos requieren atribucion segun licencia gratuita de Flaticon.
      Registrar autor y URL en las notas de QA del paso 10 del carrusel.
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.request


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.flaticon.com/",
}


def get_folder(icon_id: str) -> str:
    """Deriva la carpeta CDN a partir del ID: quita los ultimos 3 digitos."""
    return icon_id[:-3] if len(icon_id) > 3 else icon_id


def download_png(icon_id: str, icon_name: str, dest_dir: str) -> dict:
    """Descarga PNG 512px y lo guarda en dest_dir."""
    folder = get_folder(icon_id)
    url = f"https://cdn-icons-png.flaticon.com/512/{folder}/{icon_id}.png"
    safe_name = re.sub(r"[^\w\-]", "-", icon_name.lower().strip())
    filename = f"{safe_name}-{icon_id}.png"
    dest_path = os.path.join(dest_dir, filename)

    os.makedirs(dest_dir, exist_ok=True)

    # El CDN de Flaticon acepta requests directas sin auth
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code} al descargar {url}"}
    except Exception as e:
        return {"error": str(e)}

    with open(dest_path, "wb") as f:
        f.write(data)

    return {
        "path": os.path.abspath(dest_path),
        "url": url,
        "size_bytes": len(data),
        "attribution": f"Icon from Flaticon (free license, attribution required) — https://www.flaticon.com/free-icon/icon_{icon_id}",
    }


def main():
    parser = argparse.ArgumentParser(description="Descarga un icono PNG de Flaticon por ID")
    parser.add_argument("icon_id", help="ID numerico del icono (ej. 5017903)")
    parser.add_argument("icon_name", help="Nombre descriptivo para el archivo (ej. cancer-ribbon)")
    parser.add_argument("dest_dir", help="Carpeta de destino (ej. assets/)")
    args = parser.parse_args()

    result = download_png(args.icon_id, args.icon_name, args.dest_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
