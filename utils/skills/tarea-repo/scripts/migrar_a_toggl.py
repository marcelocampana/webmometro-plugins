#!/usr/bin/env python3
"""
Migra un repo con el formato anterior (`tareas/tareas.md`, `revisar.md`, `secciones.md`) a Toggl
como única lista: arma la carga de tareas que hay que crear o actualizar, y el `tareas/toggl.md` que
queda en el repo.

**Solo lee y propone.** `armar` no escribe nada: devuelve un JSON con las tareas en orden, los pares
dudosos de `## Ahora` con su sección y el texto de `toggl.md`. El envío a Toggl (MCP `tasks
bulk-create` / `bulk-patch`) y el `git rm` los hace el skill, con el visto bueno del usuario. Así, lo
que se muestra es exactamente lo que se envía.

El orden de la cola se conserva: primero `## Ahora`, después las pendientes de cada sección en el
orden del archivo. Toggl da a cada tarea nueva una posición mayor que la anterior, así que crearlas en
ese orden basta. Cada tarea lleva su área (la sección) en la primera línea de la descripción.

Uso:
    migrar_a_toggl.py armar tareas/ --proyecto ID --usuario UID
                      [--estados '{"todo":ID,"in_progress":ID,"blocked":ID}'] [--bandeja ID_ETIQUETA] [--areas '{"Área":ID_ETIQUETA}']
                      [--hoy AAAA-MM-DD]
    migrar_a_toggl.py toggl-md tareas/ --proyecto ID --nombre NOMBRE --cliente ID --cliente-nombre NOMBRE
                      [--forzar]

Códigos de salida: 0 bien · 1 hay pares dudosos que confirmar · 2 error.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from emparejar_ahora import celdas, emparejar, sin_id  # noqa: E402

ESTADOS = {"🔵 En curso": "in_progress", "En curso": "in_progress", "Bloqueada": "blocked",
           "Pausada": "todo", "Pendiente": "todo"}
MARCADOR = re.compile(r"<!--\s*tarea:\s*toggl\s*·\s*proyecto\s+(\d+)\s*«([^»]*)»(?:\s*·\s*cliente\s+(\d+)\s*«([^»]*)»)?")


def id_toggl(texto):
    m = re.search(r"<!--\s*toggl:\s*(\d+)\s*-->", texto or "")
    return int(m.group(1)) if m else None


def limpio(texto):
    """Para Toggl: sin el id, sin comillas de código y sin enlaces al historial."""
    texto = sin_id(texto or "")
    texto = re.sub(r"\[detalle\]\([^)]*\)", "", texto)
    texto = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", texto)
    texto = texto.replace("`", "").replace("<br>", "\n")
    return re.sub(r"[ \t]+", " ", texto).strip(" .") if texto.strip() not in ("—", "-") else ""


def minutos(coste):
    """`~45m`, `2h 30m`, `1h` → minutos; `—` o vacío → None."""
    if not coste or coste.strip() in ("—", "-"):
        return None
    h = re.search(r"(\d+)\s*h", coste)
    m = re.search(r"(\d+)\s*m", coste)
    total = (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)
    return total or None


def fecha(vence):
    m = re.search(r"\d{4}-\d{2}-\d{2}", vence or "")
    return m.group(0) if m else None


def leer_tablas(ruta):
    """{sección: [fila como dict]}, en el orden del archivo, y el marcador si lo hay."""
    # `revisar.md` suele tener su tabla antes de cualquier `##`: esa va bajo la sección "".
    tablas, seccion, cabecera, marcador = {"": []}, "", None, None
    for linea in Path(ruta).read_text(encoding="utf-8").split("\n"):
        m = MARCADOR.search(linea)
        if m:
            marcador = m
        if linea.startswith("## "):
            seccion, cabecera = linea[3:].strip(), None
            tablas.setdefault(seccion, [])
            continue
        if not linea.startswith("|"):
            continue
        c = celdas(linea)
        if cabecera is None:
            cabecera = c
            continue
        if set("".join(c)) <= set("-: "):
            continue
        tablas[seccion].append(dict(zip(cabecera, c)))
    return tablas, marcador


def leer_secciones(ruta):
    """El catálogo: [(nombre, ámbito)], con el ámbito tomado del primer párrafo de cada entrada."""
    if not Path(ruta).exists():
        return []
    salida = []
    for bloque in Path(ruta).read_text(encoding="utf-8").split("\n## ")[1:]:
        nombre, _, cuerpo = bloque.partition("\n")
        parrafos = [p.strip() for p in cuerpo.split("\n\n") if p.strip()]
        ambito = next((p for p in parrafos if not p.startswith(("**", "---", "<!--"))), "")
        salida.append((nombre.strip(), " ".join(ambito.split())))
    return salida


def abierta(fila):
    return fila.get("Estado", "").replace("✅", "").strip() != "Completada"


def armar(carpeta, proyecto, usuario, estados=None, bandeja=None, hoy=None, areas_ids=None):
    carpeta = Path(carpeta)
    hoy = hoy or date.today().isoformat()
    tablas, marcador = leer_tablas(carpeta / "tareas.md")
    ahora = tablas.pop("Ahora", [])
    secciones = {s: [f for f in filas if abierta(f) and f.get("Tarea")] for s, filas in tablas.items() if s}
    secciones = {s: f for s, f in secciones.items() if f}

    punteros = [{"n": f.get("#"), "tarea": sin_id(f.get("Tarea", "")), "seccion": f.get("Sección", ""),
                 "fila": f} for f in ahora]
    pares = emparejar(punteros, {s: [sin_id(f["Tarea"]) for f in filas] for s, filas in secciones.items()})

    tareas, usadas = [], set()

    def agregar(fila, seccion, nombre=None, detalle=None, nota=None, puntero=None):
        comentario = limpio(fila.get("Comentarios", "") or fila.get("Nota", ""))
        partes = [x for x in (limpio(detalle or ""), comentario, limpio(nota or "")) if x]
        estado = ESTADOS.get(fila.get("Estado", "").strip(), "todo")
        vence = fecha(fila.get("Vence") or (puntero or {}).get("Vence"))
        tareas.append({
            "toggl_id": id_toggl(fila.get("Tarea")) or id_toggl((puntero or {}).get("Tarea")),
            "nombre": limpio(nombre or fila.get("Tarea", "")),
            "area": seccion,
            "descripcion": "\n".join(["Área: %s" % seccion] + partes),
            "estado": estado,
            "estimado_min": minutos(fila.get("Coste") or (puntero or {}).get("Coste")),
            "vence": vence,
            "bandeja": False,
        })

    for par, puntero in zip(pares, punteros):
        seccion = par["seccion"]
        fila = next((f for f in secciones.get(seccion, []) if sin_id(f["Tarea"]) == par["seccion_tarea"]), None)
        nota = puntero["fila"].get("Nota")
        if fila is None:   # un puntero sin fila en su sección: se migra tal cual
            agregar(puntero["fila"], seccion, puntero["tarea"], nota=nota)
            continue
        usadas.add((seccion, par["seccion_tarea"]))
        agregar(fila, seccion, par.get("nombre_unico") or par["seccion_tarea"],
                par.get("detalle_a_comentarios"), nota, puntero["fila"])
    for seccion, filas in secciones.items():
        for fila in filas:
            if (seccion, sin_id(fila["Tarea"])) not in usadas:
                agregar(fila, seccion)

    revisar = carpeta / "revisar.md"
    if revisar.exists():
        filas, _ = leer_tablas(revisar)
        for fila in (f for filas_s in filas.values() for f in filas_s if f.get("Tarea")):
            partes = ["%s: %s" % (k, limpio(fila.get(k))) for k in ("Origen", "Motivo", "Notas") if limpio(fila.get(k))]
            tareas.append({"toggl_id": None, "nombre": limpio(fila["Tarea"]), "area": "General",
                           "descripcion": "\n".join(["Área: General"] + partes), "estado": "todo",
                           "estimado_min": None, "vence": None, "bandeja": True})

    for t in tareas:
        t["payload"] = payload(t, proyecto, usuario, estados, bandeja, hoy, areas_ids)

    catalogo = leer_secciones(carpeta / "secciones.md")
    nombres = [n for n, _ in catalogo]
    areas = catalogo + [(s, "") for s in secciones if s not in nombres]
    proyecto_nombre = marcador.group(2) if marcador else None
    return {
        "proyecto": proyecto,
        "marcador_en_tareas_md": {"proyecto": int(marcador.group(1)), "nombre": proyecto_nombre} if marcador else None,
        "crear": [t for t in tareas if not t["toggl_id"]],
        "actualizar": [t for t in tareas if t["toggl_id"]],
        "dudosos": [p for p in pares if p["tipo"] != "exacto"],
        "areas": [{"nombre": n, "ambito": a} for n, a in areas],
        "resumen": {"crear": sum(1 for t in tareas if not t["toggl_id"] and not t["bandeja"]),
                    "actualizar": sum(1 for t in tareas if t["toggl_id"]),
                    "bandeja": sum(1 for t in tareas if t["bandeja"]),
                    "areas": len(areas)},
    }


def payload(t, proyecto, usuario, estados, bandeja, hoy, areas_ids=None):
    """Lo que va a Toggl, tal cual. `status_id` y las etiquetas solo si se dieron sus ids: la del
    área, si está en `areas_ids`, y la de la bandeja."""
    p = {"name": t["nombre"], "project_id": proyecto, "description": t["descripcion"]}
    if t["toggl_id"]:
        p = {"id": t["toggl_id"], "name": t["nombre"], "description": t["descripcion"]}
    etiquetas = [i for i in ((areas_ids or {}).get(t["area"]), bandeja if t["bandeja"] else None) if i]
    if etiquetas:
        p["tag_ids"] = etiquetas
    if t["bandeja"]:
        return p
    if usuario:
        p["assignee_user_ids"] = [usuario]
    if t["estimado_min"]:
        p["estimated_mins"] = t["estimado_min"]
    if t["vence"]:   # Toggl rechaza end_date sin start_date
        p["start_date"], p["end_date"] = min(hoy, t["vence"]), t["vence"]
    if estados and t["estado"] in estados:
        p["status_id"] = estados[t["estado"]]
    return p


def toggl_md(proyecto, nombre, cliente, cliente_nombre, areas):
    filas = "\n".join("| %s | %s |" % (a["nombre"], a["ambito"] or "—") for a in areas) or "| General | — |"
    return ("<!-- tarea: toggl · proyecto %s «%s» · cliente %s «%s» -->\n\n# Toggl · %s\n\n"
            "Configuración de este repo en Toggl. Los pendientes viven allí; aquí, cómo se ordenan. Lo común a\n"
            "todos los repos está en la configuración global de Toggl.\n\n## Áreas\n\n"
            "Cada tarea lleva la etiqueta de su área, con uno de estos nombres, y la repite en la primera línea\n"
            "de la descripción (`Área: <nombre>`).\n\n"
            "| Área | Qué abarca |\n| --- | --- |\n%s\n\n## Reglas\n\n<!-- Opcional: lo propio de este repo en Toggl. -->\n\n"
            "## Comentarios\n\n<!-- Opcional. -->\n") % (proyecto, nombre, cliente, cliente_nombre, nombre, filas)


def main(argv=None):
    p = argparse.ArgumentParser(description="Migra un repo del formato tareas.md a Toggl.")
    sub = p.add_subparsers(dest="orden", required=True)
    a = sub.add_parser("armar")
    a.add_argument("carpeta")
    a.add_argument("--proyecto", type=int, required=True)
    a.add_argument("--usuario", type=int)
    a.add_argument("--estados", type=json.loads, help='{"todo":ID,"in_progress":ID,"blocked":ID}')
    a.add_argument("--bandeja", type=int, help="id de la etiqueta por-revisar")
    a.add_argument("--areas", type=json.loads, help='{"Área": id de su etiqueta}')
    a.add_argument("--hoy")
    t = sub.add_parser("toggl-md")
    t.add_argument("carpeta")
    t.add_argument("--proyecto", type=int, required=True)
    t.add_argument("--nombre", required=True)
    t.add_argument("--cliente", type=int, required=True)
    t.add_argument("--cliente-nombre", required=True)
    t.add_argument("--forzar", action="store_true")
    args = p.parse_args(argv)
    carpeta = Path(args.carpeta)
    if not (carpeta / "tareas.md").exists():
        print("No hay %s: no hay nada que migrar." % (carpeta / "tareas.md"), file=sys.stderr)
        return 2
    if args.orden == "armar":
        r = armar(carpeta, args.proyecto, args.usuario, args.estados, args.bandeja, args.hoy, args.areas)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 1 if r["dudosos"] else 0
    destino = carpeta / "toggl.md"
    if destino.exists() and not args.forzar:
        print("%s ya existe; --forzar para reescribirlo." % destino, file=sys.stderr)
        return 2
    areas = armar(carpeta, args.proyecto, None)["areas"]
    destino.write_text(toggl_md(args.proyecto, args.nombre, args.cliente, args.cliente_nombre, areas), encoding="utf-8")
    print(json.dumps({"ok": True, "escrito": str(destino), "areas": len(areas)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
