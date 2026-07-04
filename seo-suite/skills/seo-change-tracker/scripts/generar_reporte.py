#!/usr/bin/env python3
"""
Genera un reporte ejecutivo a partir de las notas de cambio SEO en contexto/seo-tracking/cambios/.

No depende de PyYAML: las notas de cambio que produce este skill usan un subconjunto acotado de
YAML (mapeos, listas, y mapeos "flow" tipo `{a: 1, b: 2}` para las métricas), así que se parsea con
un parser mínimo hecho a mano en vez de requerir una instalación adicional en la máquina del
usuario.

Uso:
    python3 generar_reporte.py <directorio_cambios> [--desde AAAA-MM-DD] [--hasta AAAA-MM-DD]
                                [--cliente "Nombre"] [--output ruta.md]
"""

import argparse
import datetime
import sys
from pathlib import Path

ICONOS_RESULTADO = {
    "positivo": "✅",
    "neutral": "➖",
    "negativo": "❌",
    "inconcluso": "❓",
}

METRICA_CLAVE_POR_AREA = {
    "on-page": ("gsc", "ctr"),
    "tecnico": ("tecnico", None),
    "contenido": ("gsc", "clicks"),
    "backlinks": ("backlinks", "referring_domains"),
    "local": ("local", "rating"),
    "otro": ("gsc", "clicks"),
}


# --- Parser mínimo de YAML (subconjunto usado por las notas de cambio) ----------------------

def _leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def _split_top_level(s, sep):
    parts, depth, cur, in_quote = [], 0, "", None
    for ch in s:
        if in_quote:
            cur += ch
            if ch == in_quote:
                in_quote = None
            continue
        if ch in ("'", '"'):
            in_quote = ch
            cur += ch
            continue
        if ch in "{[":
            depth += 1
            cur += ch
            continue
        if ch in "}]":
            depth -= 1
            cur += ch
            continue
        if ch == sep and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    if cur.strip() != "":
        parts.append(cur)
    return parts


def _parse_scalar(s):
    s = s.strip()
    if s == "" or s == "null" or s == "~":
        return None
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    if s.startswith("{") and s.endswith("}"):
        return _parse_flow_map(s)
    if s.startswith("[") and s.endswith("]"):
        return _parse_flow_list(s)
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        return s


def _parse_flow_list(s):
    inner = s[1:-1].strip()
    if inner == "":
        return []
    return [_parse_scalar(x.strip()) for x in _split_top_level(inner, ",")]


def _parse_flow_map(s):
    inner = s[1:-1].strip()
    if inner == "":
        return {}
    result = {}
    for item in _split_top_level(inner, ","):
        k, _, v = item.partition(":")
        result[k.strip()] = _parse_scalar(v.strip())
    return result


def _parse_map(lines, i, indent):
    result = {}
    while i < len(lines):
        if lines[i].strip() == "":
            i += 1
            continue
        cur_indent = _leading_spaces(lines[i])
        if cur_indent < indent:
            break
        stripped = lines[i].strip()
        if stripped.startswith("- "):
            break
        key, _, rest = stripped.partition(":")
        rest = rest.strip()
        i += 1
        if rest == "":
            if i < len(lines) and lines[i].strip() != "" and _leading_spaces(lines[i]) > indent:
                child_indent = _leading_spaces(lines[i])
                if lines[i].strip().startswith("- "):
                    value, i = _parse_list(lines, i, child_indent)
                else:
                    value, i = _parse_map(lines, i, child_indent)
            else:
                value = None
        else:
            value = _parse_scalar(rest)
        result[key.strip()] = value
    return result, i


def _parse_list(lines, i, indent):
    result = []
    while i < len(lines):
        if lines[i].strip() == "":
            i += 1
            continue
        cur_indent = _leading_spaces(lines[i])
        if cur_indent != indent:
            break
        stripped = lines[i].strip()
        if not stripped.startswith("-"):
            break
        item_content = stripped[1:].strip()
        i += 1
        sub_indent = indent + 2
        if item_content == "":
            if i < len(lines) and _leading_spaces(lines[i]) > indent:
                child_indent = _leading_spaces(lines[i])
                if lines[i].strip().startswith("-"):
                    value, i = _parse_list(lines, i, child_indent)
                else:
                    value, i = _parse_map(lines, i, child_indent)
            else:
                value = None
            result.append(value)
        elif ":" in item_content and not item_content.startswith(("{", "[", '"', "'")):
            key, _, rest = item_content.partition(":")
            submap = {key.strip(): _parse_scalar(rest.strip())}
            while i < len(lines):
                if lines[i].strip() == "":
                    i += 1
                    continue
                if _leading_spaces(lines[i]) == sub_indent and not lines[i].strip().startswith("-"):
                    k2, _, r2 = lines[i].strip().partition(":")
                    r2 = r2.strip()
                    i += 1
                    if r2 == "":
                        if i < len(lines) and _leading_spaces(lines[i]) > sub_indent:
                            child_indent = _leading_spaces(lines[i])
                            if lines[i].strip().startswith("-"):
                                v, i = _parse_list(lines, i, child_indent)
                            else:
                                v, i = _parse_map(lines, i, child_indent)
                        else:
                            v = None
                    else:
                        v = _parse_scalar(r2)
                    submap[k2.strip()] = v
                else:
                    break
            result.append(submap)
        else:
            result.append(_parse_scalar(item_content))
    return result, i


def parse_frontmatter(text):
    if not text.startswith("---"):
        raise ValueError("El archivo no empieza con frontmatter '---'")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Frontmatter incompleto (falta el '---' de cierre)")
    fm_text = parts[1]
    lines = fm_text.split("\n")
    data, _ = _parse_map(lines, 0, 0)
    return data


# --- Carga de notas de cambio ------------------------------------------------------------

def cargar_cambios(directorio, desde=None, hasta=None):
    cambios = []
    for path in sorted(Path(directorio).glob("*.md")):
        try:
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError as e:
            print(f"Aviso: se omite {path.name} ({e})", file=sys.stderr)
            continue
        fecha_str = data.get("fecha")
        if not fecha_str:
            print(f"Aviso: se omite {path.name} (sin campo 'fecha')", file=sys.stderr)
            continue
        try:
            fecha = datetime.date.fromisoformat(str(fecha_str))
        except ValueError:
            print(f"Aviso: se omite {path.name} (fecha inválida: {fecha_str})", file=sys.stderr)
            continue
        if desde and fecha < desde:
            continue
        if hasta and fecha > hasta:
            continue
        data["_archivo"] = path.name
        data["_fecha_obj"] = fecha
        cambios.append(data)
    return cambios


# --- Cálculo de deltas e impacto ----------------------------------------------------------

def _ultimo_checkpoint(cambio):
    checkpoints = cambio.get("checkpoints") or []
    if not checkpoints:
        return None
    return checkpoints[-1]


def calcular_delta(cambio):
    """Devuelve (texto_delta, valor_numerico_abs) usando la métrica clave del área."""
    area = cambio.get("area", "otro")
    grupo, campo = METRICA_CLAVE_POR_AREA.get(area, ("gsc", "clicks"))
    baseline = (cambio.get("baseline") or {}).get(grupo)
    checkpoint = _ultimo_checkpoint(cambio)
    checkpoint_grupo = checkpoint.get(grupo) if checkpoint else None

    if not baseline or not checkpoint_grupo:
        return ("sin checkpoint aún", 0.0)

    if campo is None:
        # área 'tecnico': no hay un único campo numérico fijo, mostrar lo que cambió
        claves_comunes = [k for k in baseline if k in checkpoint_grupo]
        if not claves_comunes:
            return ("sin datos comparables", 0.0)
        campo = claves_comunes[0]

    base_val = baseline.get(campo)
    chk_val = checkpoint_grupo.get(campo)
    es_numerico = (
        isinstance(base_val, (int, float)) and not isinstance(base_val, bool)
        and isinstance(chk_val, (int, float)) and not isinstance(chk_val, bool)
    )
    if not es_numerico:
        cambio_txt = "sin cambios" if base_val == chk_val else "con cambios"
        return (f"{grupo}.{campo}: {base_val} → {chk_val} ({cambio_txt})", 0.0)

    diff = chk_val - base_val
    pct = (diff / base_val * 100) if base_val else float("inf") if diff else 0.0
    flecha = "↑" if diff > 0 else ("↓" if diff < 0 else "→")
    pct_txt = f" ({pct:+.0f}%)" if base_val else ""
    texto = f"{grupo}.{campo}: {base_val} → {chk_val} {flecha}{pct_txt}"
    return (texto, abs(diff))


# --- Renderizado del reporte ---------------------------------------------------------------

def render_reporte(cambios, cliente, desde, hasta):
    concluidos = [c for c in cambios if c.get("resultado") in ("positivo", "neutral", "negativo", "inconcluso")]
    en_medicion = [c for c in cambios if c.get("resultado") in (None, "pendiente")]

    n_positivos = sum(1 for c in concluidos if c.get("resultado") == "positivo")
    hoy = datetime.date.today().isoformat()

    lineas = []
    rango = f"{desde or '(sin límite)'} a {hasta or '(sin límite)'}"
    lineas.append(f"# Reporte SEO — {cliente} — {rango}")
    lineas.append("")
    lineas.append(f"**Generado:** {hoy}")
    lineas.append(f"**Cambios en el período:** {len(cambios)} ({len(concluidos)} concluidos, {len(en_medicion)} en medición)")
    lineas.append("")
    lineas.append("## Resumen ejecutivo")
    lineas.append("")
    if concluidos:
        lineas.append(f"- {n_positivos} de {len(concluidos)} cambios concluidos dieron resultado positivo.")
    else:
        lineas.append("- Todavía no hay cambios con veredicto concluido en este período.")
    lineas.append(f"- {len(en_medicion)} cambio(s) siguen en medición, en espera de su próximo checkpoint.")
    lineas.append("")

    lineas.append("## Qué funcionó")
    lineas.append("")
    if concluidos:
        con_delta = [(c, calcular_delta(c)) for c in concluidos]
        con_delta.sort(key=lambda par: par[1][1], reverse=True)
        lineas.append("| Estado | Cambio | Área | Implementado | Resultado | Delta clave |")
        lineas.append("|---|---|---|---|---|---|")
        for c, (delta_txt, _) in con_delta:
            icono = ICONOS_RESULTADO.get(c.get("resultado"), "❓")
            lineas.append(
                f"| {icono} | {c.get('descripcion', '(sin descripción)')} | {c.get('area', '?')} | "
                f"{c.get('fecha', '?')} | {c.get('resultado', '?').capitalize()} | {delta_txt} |"
            )
    else:
        lineas.append("_Sin cambios concluidos todavía en este período._")
    lineas.append("")

    lineas.append("## En medición")
    lineas.append("")
    if en_medicion:
        lineas.append("| Cambio | Área | Implementado | Hipótesis |")
        lineas.append("|---|---|---|---|")
        for c in en_medicion:
            lineas.append(
                f"| {c.get('descripcion', '(sin descripción)')} | {c.get('area', '?')} | "
                f"{c.get('fecha', '?')} | {c.get('hipotesis', '(sin hipótesis)')} |"
            )
    else:
        lineas.append("_Sin cambios pendientes de medición._")
    lineas.append("")

    lineas.append("## Por área")
    lineas.append("")
    areas = sorted(set(c.get("area", "otro") for c in cambios))
    if areas:
        lineas.append("| Área | Cambios | Positivos | Negativos | En medición |")
        lineas.append("|---|---|---|---|---|")
        for area in areas:
            del_area = [c for c in cambios if c.get("area", "otro") == area]
            pos = sum(1 for c in del_area if c.get("resultado") == "positivo")
            neg = sum(1 for c in del_area if c.get("resultado") == "negativo")
            med = sum(1 for c in del_area if c.get("resultado") in (None, "pendiente"))
            lineas.append(f"| {area} | {len(del_area)} | {pos} | {neg} | {med} |")
    else:
        lineas.append("_Sin cambios registrados en este período._")
    lineas.append("")

    lineas.append("## Notas metodológicas")
    lineas.append("")
    lineas.append(
        "- Los deltas comparan el baseline (al momento del cambio) contra el checkpoint más "
        "reciente disponible, no contra el período anterior al cambio — esto aísla el efecto del "
        "cambio específico."
    )
    lineas.append(
        "- \"Inconcluso\" significa que los datos disponibles no permiten un veredicto claro "
        "(señales mixtas, volumen insuficiente, o un factor externo conocido)."
    )
    lineas.append("")

    return "\n".join(lineas)


def main():
    ap = argparse.ArgumentParser(description="Genera un reporte ejecutivo de cambios SEO.")
    ap.add_argument("directorio", help="Directorio con las notas de cambio (contexto/seo-tracking/cambios)")
    ap.add_argument("--desde", help="Fecha mínima AAAA-MM-DD (inclusive)")
    ap.add_argument("--hasta", help="Fecha máxima AAAA-MM-DD (inclusive)")
    ap.add_argument("--cliente", default="Cliente", help="Nombre del cliente para el encabezado")
    ap.add_argument("--output", help="Ruta de salida; si se omite, imprime a stdout")
    args = ap.parse_args()

    desde = datetime.date.fromisoformat(args.desde) if args.desde else None
    hasta = datetime.date.fromisoformat(args.hasta) if args.hasta else None

    cambios = cargar_cambios(args.directorio, desde, hasta)
    cambios.sort(key=lambda c: c["_fecha_obj"])

    reporte = render_reporte(cambios, args.cliente, args.desde, args.hasta)

    if args.output:
        Path(args.output).write_text(reporte, encoding="utf-8")
        print(f"Reporte escrito en {args.output}", file=sys.stderr)
    else:
        print(reporte)


if __name__ == "__main__":
    main()
