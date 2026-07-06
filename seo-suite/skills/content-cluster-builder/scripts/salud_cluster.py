#!/usr/bin/env python3
"""
Calcula las métricas de salud de un clúster de contenido a partir de las notas del vault.

Lee los archivos .md del clúster (pilar + spokes), extrae el frontmatter y los wikilinks,
y calcula: cobertura, link health, content quality, y los 4 gates de tolerancia-cero.

No depende de PyYAML — usa un parser mínimo de frontmatter, igual que generar_reporte.py
del skill seo-change-tracker.

Uso:
    python3 salud_cluster.py <directorio_o_lista_de_notas> [--cluster nombre]
    python3 salud_cluster.py nota-pilar.md spoke-1.md spoke-2.md
    python3 salud_cluster.py --cluster "hifu-12d" --vault /ruta/al/vault
"""

import argparse
import re
import sys
from pathlib import Path


# --- Parser mínimo de frontmatter YAML -------------------------------------------------------

def _leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def _parse_scalar(s):
    s = s.strip()
    if s in ("", "null", "~"):
        return None
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
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
        if _leading_spaces(lines[i]) < indent:
            break
        stripped = lines[i].strip()
        if not stripped.startswith("-"):
            break
        item = stripped[2:].strip()
        i += 1
        result.append(_parse_scalar(item))
    return result, i


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    lines = parts[1].split("\n")
    data, _ = _parse_map(lines, 0, 0)
    return data


def extract_wikilinks(text):
    """Extrae todos los nombres de [[wikilinks]] del cuerpo del texto."""
    return re.findall(r"\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]", text)


# --- Carga de notas --------------------------------------------------------------------------

def cargar_nota(path):
    text = Path(path).read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    links = extract_wikilinks(body)
    fm["_path"] = str(path)
    fm["_nombre"] = Path(path).stem
    fm["_links"] = links
    return fm


def encontrar_notas_cluster(cluster_name, vault_path):
    """Busca notas en el vault cuyo frontmatter `cluster` coincida con cluster_name."""
    vault = Path(vault_path)
    notas = []
    for md in vault.rglob("*.md"):
        if ".claude" in md.parts:
            continue
        try:
            fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        except Exception:
            continue
        if fm.get("cluster") == cluster_name:
            notas.append(md)
    return notas


# --- Métricas de salud -----------------------------------------------------------------------

def calcular_salud(notas):
    """
    Recibe lista de dicts de notas (con _nombre, _links, tipo, estado, etc.)
    Devuelve un dict con las métricas y resultados de los gates.
    """
    pilar = next((n for n in notas if n.get("tipo") == "pilar"), None)
    spokes = [n for n in notas if n.get("tipo") == "spoke"]

    if not pilar:
        return {"error": "No se encontró nota de tipo 'pilar' en el conjunto."}

    n_spokes = len(spokes)
    if n_spokes == 0:
        return {"error": "No se encontraron notas de tipo 'spoke'."}

    pilar_nombre = pilar["_nombre"]
    pilar_links = set(pilar.get("_links", []))

    # Cobertura: spokes con estado != "gap" (cubierto o parcial cuentan)
    estados_validos = {"cubierto", "parcial", "borrador", "publicado"}
    spokes_cubiertos = sum(1 for s in spokes if s.get("estado", "borrador") in estados_validos)
    cobertura_pct = round(spokes_cubiertos / n_spokes * 100) if n_spokes else 0

    # Link health: spokes con enlace bidireccional al pilar
    spokes_con_link_al_pilar = 0
    pilar_enlaza_spoke = 0
    huerfanos = []

    for spoke in spokes:
        spoke_nombre = spoke["_nombre"]
        spoke_links = set(spoke.get("_links", []))

        spoke_enlaza_pilar = pilar_nombre in spoke_links
        pilar_enlaza_este_spoke = spoke_nombre in pilar_links

        if spoke_enlaza_pilar and pilar_enlaza_este_spoke:
            spokes_con_link_al_pilar += 1
        if not pilar_enlaza_este_spoke:
            huerfanos.append(spoke_nombre)
        if pilar_enlaza_este_spoke:
            pilar_enlaza_spoke += 1

    link_health_pct = round(spokes_con_link_al_pilar / n_spokes * 100) if n_spokes else 0

    # Content quality: spokes con calidad >= 3 (si el campo existe)
    spokes_con_calidad = [s for s in spokes if isinstance(s.get("calidad"), int)]
    if spokes_con_calidad:
        spokes_calidad_ok = sum(1 for s in spokes_con_calidad if s.get("calidad", 0) >= 3)
        content_quality_pct = round(spokes_calidad_ok / n_spokes * 100)
    else:
        content_quality_pct = None  # sin datos suficientes

    # Anchor diversity: contar anchors repetidos en todos los links del pilar
    all_anchors = pilar.get("_links", [])
    anchor_counts = {}
    for a in all_anchors:
        anchor_counts[a] = anchor_counts.get(a, 0) + 1
    total_anchors = len(all_anchors)
    anchor_violaciones = []
    if total_anchors > 0:
        for anchor, count in anchor_counts.items():
            pct = count / total_anchors * 100
            if pct > 40:
                anchor_violaciones.append((anchor, round(pct)))

    # Coherencia de intención: el tipo_pagina de cada nota debe calzar con su intencion_serp_dominante.
    # Solo se evalúa cuando ambos campos están presentes. Los tipos "mixta"/"hub-mixto" sirven varias
    # intenciones a propósito, así que no se marcan. Una página transaccional que rankea intención
    # local es coherente (servicio local).
    def _coherente(tipo, intent):
        if tipo in (None, "mixta", "hub-mixto") or intent is None:
            return True
        if tipo == "transaccional" and intent == "local":
            return True
        return tipo == intent

    intencion_violaciones = []
    for n in notas:
        tipo = n.get("tipo_pagina")
        intent = n.get("intencion_serp_dominante")
        if tipo is not None and intent is not None and not _coherente(tipo, intent):
            intencion_violaciones.append((n["_nombre"], tipo, intent))

    # Gates
    gate_huerfanos = len(huerfanos) == 0
    gate_cobertura = cobertura_pct >= 70
    gate_anchor = len(anchor_violaciones) == 0
    gate_coherencia = len(intencion_violaciones) == 0
    # Canibalización: no calculable con un solo clúster — requiere SERP externo
    gate_canibalizacion = None

    todos_ok = gate_huerfanos and gate_cobertura and gate_anchor and gate_coherencia

    return {
        "pilar": pilar_nombre,
        "n_spokes": n_spokes,
        "cobertura_pct": cobertura_pct,
        "link_health_pct": link_health_pct,
        "content_quality_pct": content_quality_pct,
        "huerfanos": huerfanos,
        "anchor_violaciones": anchor_violaciones,
        "intencion_violaciones": intencion_violaciones,
        "gates": {
            "canibalizacion": gate_canibalizacion,
            "huerfanos_ok": gate_huerfanos,
            "cobertura_ok": gate_cobertura,
            "anchor_ok": gate_anchor,
            "coherencia_ok": gate_coherencia,
        },
        "todos_gates_ok": todos_ok,
    }


# --- Renderizado del reporte -----------------------------------------------------------------

ESTADO_ICONO = {True: "✅", False: "❌", None: "⚠️ (requiere SERP externo)"}
ESTADO_TEXTO = {True: "OK", False: "REVISAR", None: "No calculable localmente"}


def render_reporte(salud, cluster_name):
    if "error" in salud:
        return f"Error: {salud['error']}"

    lineas = []
    lineas.append(f"# Scorecard de salud — clúster: {cluster_name or salud['pilar']}")
    lineas.append("")
    lineas.append(f"**Pilar:** {salud['pilar']}")
    lineas.append(f"**Spokes analizados:** {salud['n_spokes']}")
    lineas.append("")

    lineas.append("## Métricas")
    lineas.append("")
    lineas.append("| Métrica | Valor | Umbral | Estado |")
    lineas.append("|---|---|---|---|")

    cob = salud["cobertura_pct"]
    lineas.append(f"| Cobertura | {cob}% | ≥70% | {'✅' if cob >= 70 else '❌'} |")

    lh = salud["link_health_pct"]
    lineas.append(f"| Link Health | {lh}% | 100% | {'✅' if lh == 100 else '❌'} |")

    cq = salud["content_quality_pct"]
    cq_txt = f"{cq}%" if cq is not None else "sin datos (campo 'calidad' no encontrado)"
    cq_ok = cq is not None and cq >= 80
    lineas.append(f"| Content Quality | {cq_txt} | ≥80% | {'✅' if cq_ok else ('⚠️' if cq is None else '❌')} |")
    lineas.append("")

    lineas.append("## Gates de tolerancia-cero")
    lineas.append("")
    gates = salud["gates"]
    lineas.append("| Gate | Estado | Detalle |")
    lineas.append("|---|---|---|")

    # Canibalización
    icon = ESTADO_ICONO[gates["canibalizacion"]]
    lineas.append(f"| Canibalización | {icon} | No calculable desde archivos: poblar con el overlap del Paso 4c (SERP en vivo). Falla si algún par >40% |")

    # Huérfanos
    h_ok = gates["huerfanos_ok"]
    h_detalle = "0 spokes huérfanos" if h_ok else f"{len(salud['huerfanos'])} huérfano(s): {', '.join(salud['huerfanos'])}"
    lineas.append(f"| Huérfanos | {ESTADO_ICONO[h_ok]} | {h_detalle} |")

    # Cobertura
    c_ok = gates["cobertura_ok"]
    lineas.append(f"| Cobertura | {ESTADO_ICONO[c_ok]} | {salud['cobertura_pct']}% ({'ok' if c_ok else 'por debajo del 70%'}) |")

    # Anchor diversity
    a_ok = gates["anchor_ok"]
    if a_ok:
        a_detalle = "Sin anchors dominantes"
    else:
        a_detalle = "; ".join(f'"{a}" en {p}% de los enlaces' for a, p in salud["anchor_violaciones"])
    lineas.append(f"| Anchor Diversity | {ESTADO_ICONO[a_ok]} | {a_detalle} |")

    # Coherencia de intención
    coh_ok = gates["coherencia_ok"]
    if coh_ok:
        coh_detalle = "Tipo de página coincide con la intención de la SERP en todas las piezas"
    else:
        coh_detalle = "; ".join(
            f'"{n}": página {t} vs SERP {i}' for n, t, i in salud["intencion_violaciones"]
        )
    lineas.append(f"| Coherencia de intención | {ESTADO_ICONO[coh_ok]} | {coh_detalle} |")
    lineas.append("")

    if salud["todos_gates_ok"]:
        lineas.append("**Resultado: clúster listo para competir.** ✅")
    else:
        lineas.append("**Resultado: el clúster necesita revisión antes de publicar.** ❌")

    return "\n".join(lineas)


# --- Main ------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Calcula la salud de un clúster de contenido.")
    ap.add_argument("notas", nargs="*", help="Rutas a los archivos .md del clúster (pilar + spokes)")
    ap.add_argument("--cluster", help="Nombre del clúster (busca en el vault si se usa con --vault)")
    ap.add_argument("--vault", help="Ruta raíz del vault (para buscar notas por nombre de clúster)")
    ap.add_argument("--output", help="Ruta de salida; si se omite, imprime a stdout")
    args = ap.parse_args()

    if args.notas:
        notas = [cargar_nota(p) for p in args.notas]
    elif args.cluster and args.vault:
        paths = encontrar_notas_cluster(args.cluster, args.vault)
        if not paths:
            print(f"No se encontraron notas con cluster='{args.cluster}' en {args.vault}", file=sys.stderr)
            sys.exit(1)
        notas = [cargar_nota(p) for p in paths]
    else:
        ap.print_help()
        sys.exit(1)

    salud = calcular_salud(notas)
    reporte = render_reporte(salud, args.cluster or "")

    if args.output:
        Path(args.output).write_text(reporte, encoding="utf-8")
        print(f"Scorecard escrito en {args.output}", file=sys.stderr)
    else:
        print(reporte)


if __name__ == "__main__":
    main()
