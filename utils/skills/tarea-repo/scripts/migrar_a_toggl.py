#!/usr/bin/env python3
"""
Migra un repo de un formato anterior al de utils 6.

- **Formato antiguo** (`tareas/tareas.md`, `revisar.md`, `secciones.md`): arma la carga de tareas
  abiertas y los archivos que quedan en el repo: `tareas/config.md` y `tareas/por-revisar.md` (la
  bandeja **no va a Toggl**). Qué tarea es del usuario (va a Toggl) y cuál es de Claude (va a
  `tareas/pendientes.md`) lo propone el skill y lo confirma el usuario.
- **utils 5** (`tareas/toggl.md`, `tareas/para-claude.md`): `a-config` renombra `toggl.md` a
  `config.md` y convierte `para-claude.md` en `pendientes.md`. Sin `--aplicar`, solo dice qué haría.

**`armar` solo lee y propone**: devuelve un JSON con las tareas en orden, los pares dudosos de
`## Ahora` con su sección y las áreas. El envío a Toggl (MCP `tasks bulk-create` / `bulk-patch`) y
el `git rm` los hace el skill, con el visto bueno del usuario. Así, lo que se muestra es
exactamente lo que se envía.

El orden de la cola se conserva: primero `## Ahora`, después las pendientes de cada sección en el
orden del archivo. Toggl da a cada tarea nueva una posición mayor que la anterior, así que crearlas en
ese orden basta. Cada tarea lleva su área (la sección) en la primera línea de la descripción.

Uso:
    migrar_a_toggl.py armar tareas/ --proyecto ID --usuario UID
                      [--estados '{"todo":ID,"in_progress":ID,"blocked":ID}'] [--areas '{"Área":ID_ETIQUETA}']
                      [--hoy AAAA-MM-DD]
    migrar_a_toggl.py config-md tareas/ --proyecto ID --nombre NOMBRE --cliente ID --cliente-nombre NOMBRE [--rama preview]
                      [--forzar]          (alias antiguo: toggl-md)
    migrar_a_toggl.py por-revisar tareas/ [--hoy AAAA-MM-DD] [--forzar]
    migrar_a_toggl.py a-config tareas/ [--aplicar]

Códigos de salida: 0 bien · 1 hay pares dudosos que confirmar · 2 error.
"""

import argparse
import json
import re
import subprocess
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


def armar(carpeta, proyecto, usuario, estados=None, hoy=None, areas_ids=None):
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

    bandeja = leer_bandeja(carpeta)

    for t in tareas:
        t["payload"] = payload(t, proyecto, usuario, estados, hoy, areas_ids)

    catalogo = leer_secciones(carpeta / "secciones.md")
    nombres = [n for n, _ in catalogo]
    areas = catalogo + [(s, "") for s in secciones if s not in nombres]
    proyecto_nombre = marcador.group(2) if marcador else None
    return {
        "proyecto": proyecto,
        "marcador_en_tareas_md": {"proyecto": int(marcador.group(1)), "nombre": proyecto_nombre} if marcador else None,
        "crear": [t for t in tareas if not t["toggl_id"]],
        "actualizar": [t for t in tareas if t["toggl_id"]],
        "bandeja": bandeja,
        "dudosos": [p for p in pares if p["tipo"] != "exacto"],
        "areas": [{"nombre": n, "ambito": a} for n, a in areas],
        "resumen": {"crear": sum(1 for t in tareas if not t["toggl_id"]),
                    "actualizar": sum(1 for t in tareas if t["toggl_id"]),
                    "bandeja": len(bandeja),
                    "areas": len(areas)},
    }


def leer_bandeja(carpeta):
    """Las entradas de `revisar.md`. No van a Toggl: se quedan en el repo, en `por-revisar.md`."""
    revisar = Path(carpeta) / "revisar.md"
    if not revisar.exists():
        return []
    filas, _ = leer_tablas(revisar)
    return [{"nombre": limpio(f["Tarea"]), "area": limpio(f.get("Sección") or f.get("Área") or "") or "General",
             "origen": limpio(f.get("Origen") or "") or "revisar.md",
             "motivo": " ".join(x for x in (limpio(f.get("Motivo") or ""), limpio(f.get("Notas") or "")) if x),
             "fecha": fecha_de_alta(revisar, f)}
            for filas_s in filas.values() for f in filas_s if f.get("Tarea")]


def fecha_de_alta(revisar, fila):
    """El día en que la entrada se anotó: el del commit que añadió su texto a `revisar.md` o, sin git,
    la primera fecha escrita en la fila. `revisar.md` no tenía columna de fecha, y la del día de la
    migración haría parecer nueva una entrada de semanas."""
    try:
        r = subprocess.run(["git", "-C", str(revisar.parent), "log", "--reverse", "--format=%cs",
                            "-S", fila["Tarea"], "--", revisar.name], capture_output=True, text=True, timeout=20)
        primera = r.stdout.split()[0] if r.returncode == 0 and r.stdout.split() else None
    except (OSError, subprocess.SubprocessError):
        primera = None
    return primera or fecha(" ".join(fila.get(k) or "" for k in ("Origen", "Motivo", "Notas")))


def por_revisar_md(bandeja, hoy):
    """`tareas/por-revisar.md`: el esqueleto del skill y una línea por entrada, con su fecha de alta."""
    esqueleto = Path(__file__).resolve().parent.parent / "assets" / "por-revisar.esqueleto.md"
    texto = re.sub(r"\n<!-- - \*\*.*?-->\n", "\n", esqueleto.read_text(encoding="utf-8"), flags=re.S).rstrip() + "\n\n"
    for b in bandeja:
        texto += "- **%s** · %s · %s · %s%s\n" % (b["nombre"], b["area"], b["origen"], b.get("fecha") or hoy,
                                                (" — " + b["motivo"]) if b["motivo"] else "")
    return texto


def payload(t, proyecto, usuario, estados, hoy, areas_ids=None):
    """Lo que va a Toggl, tal cual. `status_id` y la etiqueta del área solo si se dieron sus ids."""
    p = {"name": t["nombre"], "project_id": proyecto, "description": t["descripcion"]}
    if t["toggl_id"]:
        p = {"id": t["toggl_id"], "name": t["nombre"], "description": t["descripcion"]}
    etiquetas = [i for i in ((areas_ids or {}).get(t["area"]),) if i]
    if etiquetas:
        p["tag_ids"] = etiquetas
    if usuario:
        p["assignee_user_ids"] = [usuario]
    if t["estimado_min"]:
        p["estimated_mins"] = t["estimado_min"]
    if t["vence"]:   # Toggl rechaza end_date sin start_date
        p["start_date"], p["end_date"] = min(hoy, t["vence"]), t["vence"]
    if estados and t["estado"] in estados:
        p["status_id"] = estados[t["estado"]]
    return p


INTRO = ("Configuración del sistema de tareas en este repo: la rama destino (la lee también la guardia de\n"
         "git), las áreas, el proyecto de Toggl donde van las tareas que el usuario elige y las reglas propias.")
RAMA = ("La rama desde la que sale cada tarea y a la que vuelve al cerrarse, siempre con la aprobación del\n"
        "usuario después de ver el resultado. Si no es `main`, pasar de ella a `main` es un acto aparte.")
AREAS = ("Cada plan, pendiente y fila del historial lleva una de estas áreas; las tareas que van a Toggl la\n"
         "llevan como etiqueta y en la primera línea de la descripción (`Área: <nombre>`).")
GENERAL = "Lo transversal y lo que no se gana un área propia."


def config_md(proyecto, nombre, cliente, cliente_nombre, areas, rama="main"):
    filas = "\n".join("| %s | %s |" % (a["nombre"], a["ambito"] or "—") for a in areas) or "| General | — |"
    return ("<!-- tarea: toggl · proyecto %s «%s» · cliente %s «%s» -->\n\n# Configuración · %s\n\n"
            "%s\n\n## Rama destino\n\n`%s`\n\n%s\n\n## Áreas\n\n%s\n\n"
            "| Área | Qué abarca |\n| --- | --- |\n%s\n\n## Reglas\n\n<!-- Opcional: lo propio de este repo. -->\n\n"
            "## Comentarios\n\n<!-- Opcional. -->\n") % (proyecto, nombre, cliente, cliente_nombre, nombre,
                                                       INTRO, rama, RAMA, AREAS, filas)


def config_desde_toggl(texto):
    """El `toggl.md` de utils 5 con la forma de `config.md`: título, presentación, «Rama destino»
    (`main` si no la declaraba) y la entrada de «Áreas». Áreas, reglas y comentarios se conservan."""
    texto = re.sub(r"^# Toggl · ", "# Configuración · ", texto, count=1, flags=re.M)
    m = re.search(r"^# .*\n", texto, re.M)
    if m and "\n## " in texto[m.end():]:  # la presentación: lo que va entre el título y la primera sección
        resto = texto[m.end():]
        texto = texto[:m.end()] + "\n" + INTRO + "\n" + resto[resto.index("\n## "):]
    if "## Rama destino" not in texto:
        seccion = "## Rama destino\n\n`main`\n\n" + RAMA + "\n\n"
        texto = texto.replace("## Áreas", seccion + "## Áreas", 1) if "## Áreas" in texto else \
            texto.rstrip() + "\n\n" + seccion
    texto = re.sub(r"(## Áreas\n\n)La primera línea de la descripción[^\n]*\n", lambda x: x.group(1) + AREAS + "\n",
                   texto, count=1)
    return texto.replace("<!-- Opcional: lo propio de este repo en Toggl. -->", "<!-- Opcional: lo propio de este repo. -->")


toggl_md = config_md  # nombre anterior

ENTRADA_PC = re.compile(r"^- \*\*(?P<titulo>.+?)\*\* · (?P<area>[^·]+?) · (?P<origen>.+?) · delegada (?P<fecha>\d{4}-\d{2}-\d{2}) — (?P<que>.+)$")


def pendientes_desde_para_claude(texto):
    """Convierte las entradas de `para-claude.md` en líneas de `Por hacer` de `pendientes.md`.
    Una línea que no tenga el formato se conserva tal cual, para no perder nada."""
    lineas, pendientes = [], False
    for linea in texto.splitlines():
        if linea.startswith("## "):
            pendientes = linea.strip() == "## Pendientes"
            continue
        if not pendientes or not linea.startswith("- "):
            continue
        m = ENTRADA_PC.match(linea.strip())
        if m:
            lineas.append("- **%s** · %s · rama — · plan — · %s — %s · delegada en revisión (%s)" % (
                m["titulo"], m["area"].strip(), m["fecha"], m["que"].strip(), m["origen"].strip()))
        else:
            lineas.append(linea.rstrip())
    return lineas


def pendientes_md(lineas):
    esqueleto = Path(__file__).resolve().parent.parent / "assets" / "pendientes.esqueleto.md"
    texto = esqueleto.read_text(encoding="utf-8")
    if lineas:
        texto = texto.replace("## Por hacer\n", "## Por hacer\n\n" + "\n".join(lineas) + "\n", 1)
    return texto


def a_config(carpeta, aplicar=False):
    """utils 5 → 6: `toggl.md` → `config.md` y `para-claude.md` → `pendientes.md`."""
    hechos = []
    toggl, config = carpeta / "toggl.md", carpeta / "config.md"
    if toggl.exists() and not config.exists():
        hechos.append("toggl.md → config.md")
        if aplicar:
            config.write_text(config_desde_toggl(toggl.read_text(encoding="utf-8")), encoding="utf-8")
            toggl.unlink()
    pc, pend = carpeta / "para-claude.md", carpeta / "pendientes.md"
    if pc.exists():
        lineas = pendientes_desde_para_claude(pc.read_text(encoding="utf-8"))
        hechos.append("para-claude.md → pendientes.md (%d entradas)" % len(lineas))
        if aplicar:
            if pend.exists():
                actual = pend.read_text(encoding="utf-8")
                pend.write_text(actual.replace("## Por hacer\n", "## Por hacer\n\n" + "\n".join(lineas) + "\n", 1)
                                if lineas else actual, encoding="utf-8")
            else:
                pend.write_text(pendientes_md(lineas), encoding="utf-8")
            pc.unlink()
    elif not pend.exists():
        hechos.append("pendientes.md nuevo")
        if aplicar:
            pend.write_text(pendientes_md([]), encoding="utf-8")
    return {"ok": True, "aplicado": aplicar, "cambios": hechos}


def main(argv=None):
    p = argparse.ArgumentParser(description="Migra un repo del formato tareas.md a Toggl.")
    sub = p.add_subparsers(dest="orden", required=True)
    a = sub.add_parser("armar")
    a.add_argument("carpeta")
    a.add_argument("--proyecto", type=int, required=True)
    a.add_argument("--usuario", type=int)
    a.add_argument("--estados", type=json.loads, help='{"todo":ID,"in_progress":ID,"blocked":ID}')
    a.add_argument("--areas", type=json.loads, help='{"Área": id de su etiqueta}')
    a.add_argument("--hoy")
    t = sub.add_parser("config-md", aliases=["toggl-md"])
    t.add_argument("carpeta")
    t.add_argument("--proyecto", type=int, required=True)
    t.add_argument("--nombre", required=True)
    t.add_argument("--cliente", type=int, required=True)
    t.add_argument("--cliente-nombre", required=True)
    t.add_argument("--rama", default="main", help="rama destino de las tareas (main por defecto)")
    t.add_argument("--forzar", action="store_true")
    pr = sub.add_parser("por-revisar", help="escribe tareas/por-revisar.md con la bandeja de revisar.md")
    pr.add_argument("carpeta")
    pr.add_argument("--hoy")
    pr.add_argument("--forzar", action="store_true")
    ac = sub.add_parser("a-config", help="utils 5 → 6: toggl.md → config.md y para-claude.md → pendientes.md")
    ac.add_argument("carpeta")
    ac.add_argument("--aplicar", action="store_true", help="sin esto, solo dice qué haría")
    args = p.parse_args(argv)
    carpeta = Path(args.carpeta)
    if args.orden == "a-config":
        r = a_config(carpeta, args.aplicar)
        print(json.dumps(r, ensure_ascii=False))
        return 0
    if not (carpeta / "tareas.md").exists():
        print("No hay %s: no hay nada que migrar." % (carpeta / "tareas.md"), file=sys.stderr)
        return 2
    if args.orden == "armar":
        r = armar(carpeta, args.proyecto, args.usuario, args.estados, args.hoy, args.areas)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 1 if r["dudosos"] else 0
    if args.orden == "por-revisar":
        destino = carpeta / "por-revisar.md"
        if destino.exists() and not args.forzar:
            print("%s ya existe; --forzar para reescribirlo." % destino, file=sys.stderr)
            return 2
        bandeja = leer_bandeja(carpeta)
        destino.write_text(por_revisar_md(bandeja, args.hoy or date.today().isoformat()), encoding="utf-8")
        print(json.dumps({"ok": True, "escrito": str(destino), "entradas": len(bandeja)}, ensure_ascii=False))
        return 0
    destino = carpeta / "config.md"
    if destino.exists() and not args.forzar:
        print("%s ya existe; --forzar para reescribirlo." % destino, file=sys.stderr)
        return 2
    r = armar(carpeta, args.proyecto, None)
    areas = r["areas"]
    for b in r["bandeja"]:  # la bandeja lleva «General» por defecto: el área tiene que existir
        if b["area"] not in [a["nombre"] for a in areas]:
            areas.append({"nombre": b["area"], "ambito": GENERAL if b["area"] == "General" else ""})
    destino.write_text(config_md(args.proyecto, args.nombre, args.cliente, args.cliente_nombre, areas, args.rama), encoding="utf-8")
    print(json.dumps({"ok": True, "escrito": str(destino), "areas": len(areas)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
