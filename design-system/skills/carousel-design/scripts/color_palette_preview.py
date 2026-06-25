#!/usr/bin/env python3
"""
color_palette_preview.py
Genera un HTML standalone con previsualización de colores por lámina.

Esta vista es solo cromática: cada lámina se muestra como un bloque del color
de fondo, con chips de los colores de elementos de diseño (texto, acento,
secundario, etc.) en una franja inferior. No incluye textos de muestra ni
estructura de la lámina — el objetivo es que el usuario apruebe la combinación
de colores antes de producir.

Uso:
  python scripts/color_palette_preview.py \
    --slides '[{"n":1,"rol":"Portada","bg":"#1B4F72","elements":[{"hex":"#FFFFFF","name":"texto"},{"hex":"#F4D03F","name":"acento"}]}, ...]' \
    --output "ruta/al/carrusel/assets/color-preview.html"

Cada slide en el JSON debe tener:
  n        : número de lámina (int)
  rol      : nombre del rol (str), ej. "Portada", "Desarrollo", "Cierre"
  bg       : color de fondo en hex (str), ej. "#1B4F72"
  elements : lista de {hex, name} con los colores de elementos de diseño que
             aparecerán sobre el fondo (texto, acento, secundario, decoración,
             etc.). El primer elemento se usa además para calcular contraste
             WCAG contra el fondo (típicamente el color de texto principal).

Compatibilidad: si un slide trae el campo legacy "text" en vez de "elements",
se interpreta como un único elemento {hex: text, name: "texto"}.
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Calculo de contraste WCAG 2.1
# ---------------------------------------------------------------------------

def _linearize(c: int) -> float:
    s = c / 255.0
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * _linearize(r) + 0.7152 * _linearize(g) + 0.0722 * _linearize(b)


def contrast_ratio(hex_fg: str, hex_bg: str) -> float:
    l1 = relative_luminance(hex_fg)
    l2 = relative_luminance(hex_bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_label(ratio: float) -> dict:
    """Devuelve etiqueta WCAG y color de badge según el ratio."""
    if ratio >= 7.0:
        return {"label": f"AAA ({ratio:.1f}:1)", "color": "#1a7a4a"}
    elif ratio >= 4.5:
        return {"label": f"AA ({ratio:.1f}:1)", "color": "#2d7d46"}
    elif ratio >= 3.0:
        return {"label": f"AA Large ({ratio:.1f}:1)", "color": "#b45309"}
    else:
        return {"label": f"Falla ({ratio:.1f}:1)", "color": "#b91c1c"}


# ---------------------------------------------------------------------------
# Normalizacion de slides (compat con formato legacy)
# ---------------------------------------------------------------------------

def normalize_slide(slide: dict) -> dict:
    """Acepta formato nuevo (elements: [...]) o legacy (text: '#hex')."""
    elements = slide.get("elements")
    if not elements:
        text = slide.get("text")
        elements = [{"hex": text, "name": "texto"}] if text else []
    return {
        "n": slide.get("n", "?"),
        "rol": slide.get("rol", ""),
        "bg": slide.get("bg", "#FFFFFF"),
        "elements": elements,
        "image": slide.get("image", None),
    }


# ---------------------------------------------------------------------------
# Generacion HTML
# ---------------------------------------------------------------------------

def build_preview_html(slides: list) -> str:
    cards_html = ""
    for raw in slides:
        s = normalize_slide(raw)
        n, rol, bg, elements, image = s["n"], s["rol"], s["bg"], s["elements"], s.get("image")

        # Chips de elementos sobre el fondo de la lamina (sin texto de muestra).
        chips_on_bg = ""
        for el in elements:
            chips_on_bg += f"""
            <span class="el-chip" style="background:{el['hex']}; border:1px solid rgba(0,0,0,.12);" title="{el.get('name','')} {el['hex']}"></span>"""

        # Listado de hex + nombre debajo del swatch.
        elements_meta = ""
        for el in elements:
            elements_meta += f"""
            <div class="hex-row">
              <span class="chip" style="background:{el['hex']}; border:1px solid #ccc;"></span>
              <code>{el['hex']}</code>
              <span class="label-small">{el.get('name','')}</span>
            </div>"""

        # Contraste principal: primer elemento vs fondo (cuando exista).
        contrast_block = ""
        if elements:
            ratio = contrast_ratio(elements[0]["hex"], bg)
            wcag = wcag_label(ratio)
            contrast_block = f"""
            <div class="badge" style="background:{wcag['color']};" title="Contraste {elements[0].get('name','')} sobre fondo">{wcag['label']}</div>"""

        # Imagen asignada a esta lámina (si existe).
        image_block = ""
        if image:
            image_block = f"""
            <div class="img-row">
              <span class="img-label">img</span>
              <span class="img-filename">{image}</span>
            </div>"""

        cards_html += f"""
        <div class="card">
          <div class="swatch" style="background:{bg};">
            <div class="swatch-header">
              <span class="slide-num">Lámina {n}</span>
              <span class="slide-rol">{rol}</span>
            </div>
            <div class="chips-strip">{chips_on_bg}
            </div>
          </div>
          <div class="meta">
            <div class="hex-row">
              <span class="chip" style="background:{bg}; border:1px solid #ccc;"></span>
              <code>{bg}</code>
              <span class="label-small">fondo</span>
            </div>{elements_meta}{contrast_block}{image_block}
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Preview de colores – Carrusel</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f4f5f7;
      color: #1a1a1a;
      padding: 32px 24px;
    }}
    h1 {{
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 8px;
    }}
    .subtitle {{
      font-size: 0.875rem;
      color: #555;
      margin-bottom: 32px;
      max-width: 640px;
    }}
    .grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }}
    .card {{
      background: #fff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 1px 4px rgba(0,0,0,.10);
      width: 220px;
      flex-shrink: 0;
    }}
    .swatch {{
      height: 200px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 14px;
    }}
    .swatch-header {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      mix-blend-mode: difference;
      color: #fff;
    }}
    .slide-num {{
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      opacity: 0.9;
    }}
    .slide-rol {{
      font-size: 0.9rem;
      font-weight: 600;
    }}
    .chips-strip {{
      display: flex;
      gap: 8px;
      align-items: center;
    }}
    .el-chip {{
      width: 28px;
      height: 28px;
      border-radius: 6px;
      flex-shrink: 0;
      box-shadow: 0 1px 2px rgba(0,0,0,.15);
    }}
    .meta {{
      padding: 12px 14px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      border-top: 1px solid #eee;
    }}
    .hex-row {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
    }}
    .chip {{
      width: 14px;
      height: 14px;
      border-radius: 3px;
      flex-shrink: 0;
    }}
    code {{
      font-family: "SF Mono", "Fira Code", monospace;
      font-size: 0.78rem;
    }}
    .label-small {{
      color: #888;
      font-size: 0.72rem;
    }}
    .badge {{
      margin-top: 4px;
      display: inline-block;
      color: #fff;
      font-size: 0.7rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 99px;
      width: fit-content;
    }}
    .img-row {{
      display: flex;
      align-items: baseline;
      gap: 6px;
      margin-top: 6px;
      padding-top: 6px;
      border-top: 1px dashed #e0e0e0;
    }}
    .img-label {{
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #aaa;
      flex-shrink: 0;
    }}
    .img-filename {{
      font-family: "SF Mono", "Fira Code", monospace;
      font-size: 0.7rem;
      color: #555;
      word-break: break-all;
    }}
    footer {{
      margin-top: 40px;
      font-size: 0.75rem;
      color: #999;
      max-width: 640px;
    }}
  </style>
</head>
<body>
  <h1>Vista previa de colores por lámina</h1>
  <p class="subtitle">Solo combinaciones cromáticas — sin textos ni estructura. Cada tarjeta muestra el color de fondo y los chips de los elementos de diseño que irán sobre la lámina (texto, acento, secundario, etc.).</p>
  <div class="grid">
    {cards_html}
  </div>
  <footer>Ratio de contraste calculado según WCAG 2.1 entre el primer elemento (típicamente el color de texto principal) y el fondo. AA requiere ≥4.5:1 para texto normal y ≥3:1 para texto grande.</footer>
</body>
</html>"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Genera preview HTML solo cromático por lámina (sin textos)"
    )
    parser.add_argument(
        "--slides",
        required=True,
        help='JSON array de slides: [{"n":1,"rol":"Portada","bg":"#hex","elements":[{"hex":"#hex","name":"texto"}]}, ...]'
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Ruta de salida para el archivo HTML"
    )
    args = parser.parse_args()

    try:
        slides = json.loads(args.slides)
    except json.JSONDecodeError as e:
        print(f"Error: JSON inválido en --slides: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(slides, list) or len(slides) == 0:
        print("Error: --slides debe ser un array JSON no vacío", file=sys.stderr)
        sys.exit(1)

    html = build_preview_html(slides)

    output_path = args.output
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Preview generado: {output_path}")
    print(f"Láminas procesadas: {len(slides)}")


if __name__ == "__main__":
    main()
