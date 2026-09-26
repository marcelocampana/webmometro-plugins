#!/usr/bin/env python3
"""
Empareja cada fila de `## Ahora` con su fila de sección, aunque los nombres no coincidan.

La regla es que `## Ahora` copia la misma Tarea de su sección, pero con el tiempo se desvían: el
puntero se acorta («Probar un pago real de punta a punta») y la sección conserva el enunciado largo
con detalle dentro («… con las credenciales de producción y comprobar que…»). Al migrar un repo a
Toggl, emparejar por nombre exacto dejaría esas filas sin id. Este script las empareja dentro de su
misma sección —primero por nombre exacto, después por parecido— y dice cuáles son dudosas, para que
el usuario las confirme antes de escribir nada.

Solo lee. Salida JSON: una entrada por fila de `## Ahora` con su pareja, el tipo de emparejamiento
(`exacto`, `parecido`, `dudoso`, `sin_pareja`) y, si difieren, la propuesta de nombre único (el más
corto) y el detalle que sobra del largo, para moverlo a Comentarios.

Uso:
    emparejar_ahora.py tareas/tareas.md

Códigos de salida: 0 sin nada que confirmar · 1 hay pares por confirmar · 2 error.
"""

import json
import re
import sys
from difflib import SequenceMatcher

UMBRAL_PARECIDO = 0.75  # por debajo, el par se muestra como dudoso
UMBRAL_MINIMO = 0.45    # por debajo, no hay pareja: se dice, no se fuerza


def celdas(linea):
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def sin_id(texto):
    return re.sub(r"\s*<!--\s*toggl:[^>]*-->", "", texto).strip()


def leer(ruta):
    ahora, secciones, seccion, cabecera = [], {}, None, None
    for linea in open(ruta, encoding="utf-8").read().split("\n"):
        if linea.startswith("## "):
            seccion, cabecera = linea[3:].strip(), None
            continue
        if not linea.startswith("|") or seccion is None:
            continue
        c = celdas(linea)
        if cabecera is None:
            cabecera = c
            continue
        if set("".join(c)) <= set("-: "):
            continue
        fila = dict(zip(cabecera, c))
        if seccion == "Ahora":
            ahora.append({"n": fila.get("#"), "tarea": sin_id(fila.get("Tarea", "")),
                          "seccion": fila.get("Sección", "")})
        elif fila.get("Estado", "").replace("✅", "").strip() != "Completada":
            secciones.setdefault(seccion, []).append(sin_id(fila.get("Tarea", "")))
    return ahora, secciones


def parecido(corto, largo):
    """El largo suele ser el corto más detalle: se compara el corto con el comienzo del largo."""
    return SequenceMatcher(None, corto.lower(), largo[: len(corto) + 15].lower()).ratio()


def detalle_sobrante(corto, largo):
    if largo.lower().startswith(corto.lower().rstrip(".")):
        return largo[len(corto.rstrip(".")):].lstrip(" ,:;—-").strip()
    return largo


def emparejar(ahora, secciones):
    # Dos pasadas: primero todos los exactos, para que un puntero sin pareja no se lleve por
    # parecido la fila que era exacta de otro; después, lo que quede, por parecido.
    usados, pares = set(), {}
    for i, a in enumerate(ahora):
        if a["tarea"] in secciones.get(a["seccion"], []) and (a["seccion"], a["tarea"]) not in usados:
            usados.add((a["seccion"], a["tarea"]))
            pares[i] = (a["tarea"], "exacto", 1.0)
    for i, a in enumerate(ahora):
        if i in pares:
            continue
        candidatas = [t for t in secciones.get(a["seccion"], []) if (a["seccion"], t) not in usados]
        puntaje, par = max(((parecido(a["tarea"], t), t) for t in candidatas), default=(0.0, None))
        # Si en la sección queda una sola candidata, es casi seguro su pareja aunque se reescribiera
        # entera: se propone como dudosa, y el usuario confirma.
        if par is None or (puntaje < UMBRAL_MINIMO and len(candidatas) > 1):
            pares[i] = (None, "sin_pareja", round(puntaje, 2))
            continue
        usados.add((a["seccion"], par))
        pares[i] = (par, "parecido" if puntaje >= UMBRAL_PARECIDO else "dudoso", puntaje)
    salida = []
    for i, a in enumerate(ahora):
        par, tipo, puntaje = pares[i]
        entrada = {"n": a["n"], "seccion": a["seccion"], "ahora": a["tarea"], "seccion_tarea": par,
                   "tipo": tipo, "puntaje": round(puntaje, 2)}
        if par and par != a["tarea"]:
            corto, largo = sorted([a["tarea"], par], key=len)
            entrada["nombre_unico"] = corto
            entrada["detalle_a_comentarios"] = detalle_sobrante(corto, largo)
        salida.append(entrada)
    return salida


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        pares = emparejar(*leer(argv[1]))
    except OSError as e:
        print("No pude leer %s: %s" % (argv[1], e), file=sys.stderr)
        return 2
    print(json.dumps(pares, ensure_ascii=False, indent=1))
    return 1 if any(p["tipo"] != "exacto" for p in pares) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
