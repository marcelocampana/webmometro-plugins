#!/usr/bin/env python3
"""
Copia local de la cola de Toggl: las tareas pendientes, con solo lo que sirve para decidir qué toca.

Toggl devuelve unos 2.000 caracteres por tarea, casi todo técnico (permisos, colores, contadores).
Leído por el MCP, eso entra entero en el contexto de Claude; con 50 tareas pendientes, cada consulta
lo llena. Este script le pregunta a Toggl directamente, se queda con los campos útiles —más la
descripción y las notas completas, que llevan el porqué y las dependencias— y guarda la copia en
local. Claude lee la copia, no la respuesta cruda.

La sesión es la del conector de Toggl (`~/.toggl/focus-tools.json`, perfil activo `mcp`): no hay
token aparte que configurar. **Nunca se renueva desde aquí**: renovar rota el token de refresco y
dejaría al conector sin sesión. Si el acceso caducó, sale con el código 3; una consulta cualquiera
por el MCP lo renueva, y el script vuelve a funcionar. El token nunca se imprime.

Uso:
    cola.py leer [--vista hoy|semana|pendientes] [--dia AAAA-MM-DD] [--proyecto ID] [--json]
                 [--max-edad MIN] [--refrescar]
    cola.py tarea ID [--json]        # una tarea entera, desde la copia
    cola.py invalidar                # tras una escritura en Toggl: la próxima lectura va a la red

Vistas:
    hoy         en curso, vencidas y las del día; con descripción y notas completas.
    semana      en curso, lo vencido y lo que cae de lunes a domingo; primera línea de la descripción.
    pendientes  todo lo que no está hecho; primera línea de la descripción.

Códigos de salida: 0 bien · 2 error de uso · 3 sin sesión o caducada · 4 Toggl no respondió y no
hay copia.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SESION_DEFECTO = Path.home() / ".toggl" / "focus-tools.json"
COPIA_DEFECTO = Path.home() / ".local" / "share" / "tarea" / "cola.json"
MAX_EDAD_MIN = 10     # una copia más joven se reutiliza sin ir a la red
POR_PAGINA = 100
MARGEN_CADUCIDAD_S = 60


class SinSesion(Exception):
    """No hay sesión del conector, o su acceso caducó."""


def ruta_sesion():
    return Path(os.environ.get("TOGGL_SESION", SESION_DEFECTO)).expanduser()


def ruta_copia():
    return Path(os.environ.get("TAREA_COLA", COPIA_DEFECTO)).expanduser()


def ahora():
    return datetime.now(timezone.utc).replace(microsecond=0)


def leer_sesion(ruta=None, momento=None):
    """El perfil activo del conector. No renueva: si caducó, lo dice."""
    ruta = ruta or ruta_sesion()
    try:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise SinSesion("no encuentro la sesión del conector de Toggl en %s" % ruta)
    clave = (datos.get("active") or {}).get("mcp")
    perfil = (datos.get("profiles") or {}).get(clave or "")
    if not perfil or not perfil.get("access_token"):
        raise SinSesion("el conector de Toggl no tiene un perfil activo; hay que iniciar sesión (tool `auth`)")
    momento = momento or ahora()
    if float(perfil.get("expires_at") or 0) < momento.timestamp() + MARGEN_CADUCIDAD_S:
        raise SinSesion("el acceso a Toggl caducó; una consulta cualquiera por el conector lo renueva")
    return {
        "token": perfil["access_token"],
        "url": (perfil.get("focus_api_url") or "https://focus.toggl.com").rstrip("/"),
        "organizacion": perfil["organization_id"],
        "espacio": perfil["workspace_id"],
        "usuario": perfil.get("user_id"),
    }


def pedir_pagina(sesion, pagina):
    """Una página de tareas sin archivar. Es la única función que habla con la red."""
    consulta = urllib.parse.urlencode({"page": pagina, "per_page": POR_PAGINA, "archived": "false"})
    url = "%s/api/organizations/%s/workspaces/%s/tasks?%s" % (
        sesion["url"], sesion["organizacion"], sesion["espacio"], consulta)
    pedido = urllib.request.Request(url, headers={
        "Authorization": "Bearer %s" % sesion["token"],
        "Accept": "application/json",
        "User-Agent": "tarea-cola",
    })
    with urllib.request.urlopen(pedido, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def traer_todas(sesion, pedir=pedir_pagina):
    tareas, pagina = [], 1
    while True:
        respuesta = pedir(sesion, pagina)
        lote = respuesta.get("data") or []
        tareas.extend(lote)
        if not lote or len(tareas) >= int(respuesta.get("total") or 0):
            return tareas
        pagina += 1


def area_de(descripcion):
    """El área va en la primera línea de la descripción: `Área: Informes`."""
    primera = (descripcion or "").strip().splitlines()[:1]
    if primera and primera[0].lower().startswith(("área:", "area:")):
        return primera[0].split(":", 1)[1].strip() or None
    return None


def reducir(t):
    """De los ~2.000 caracteres de Toggl, lo que sirve para decidir qué toca."""
    proyecto = t.get("project") or {}
    estado = t.get("status") or {}
    return {
        "id": t.get("id"),
        "nombre": t.get("name"),
        "proyecto": proyecto.get("name"),
        "proyecto_id": t.get("project_id"),
        "cliente": (t.get("client") or {}).get("name"),
        "madre": t.get("parent_task_id"),
        "subtareas": t.get("sub_task_total_count") or 0,
        "estado": estado.get("name"),
        "tipo_estado": estado.get("type"),
        "inicio": t.get("start_date"),
        "fin": t.get("end_date"),
        "estimado_min": t.get("estimated_mins"),
        "prioridad": t.get("priority") or "none",
        "posicion": t.get("position"),
        "etiquetas": [e.get("name") for e in (t.get("tags") or [])],
        "asignada": bool(t.get("assignee_user_ids")),
        "area": area_de(t.get("description")),
        "descripcion": t.get("description") or "",
        "notas": t.get("notes") or "",
    }


def pendientes(tareas):
    return [t for t in tareas if t.get("tipo_estado") != "done"]


def lunes_de(d):
    return d - timedelta(days=d.weekday())


def en_rango(t, desde, hasta):
    """¿La tarea cae entre `desde` y `hasta`? Una madre con varias fechas cuenta si se solapa."""
    if not t.get("fin"):
        return False
    inicio = date.fromisoformat((t.get("inicio") or t["fin"])[:10])
    fin = date.fromisoformat(t["fin"][:10])
    return inicio <= hasta and fin >= desde


def vencida(t, dia):
    return bool(t.get("fin")) and date.fromisoformat(t["fin"][:10]) < dia


ORDEN_PRIORIDAD = {"urgent": 0, "high": 1, "medium": 2, "low": 3, "none": 4}


def clave_orden(t):
    # En curso primero; luego por día, prioridad y posición. `position` solo ordena dentro de un
    # grupo (se repite entre proyectos), por eso va al final.
    return (
        0 if t.get("tipo_estado") == "in_progress" else 1,
        (t.get("fin") or "9999-99-99")[:10],
        ORDEN_PRIORIDAD.get(t.get("prioridad"), 4),
        t.get("proyecto") or "",
        t.get("posicion") or 0,
    )


def filtrar(tareas, vista, dia, proyecto=None):
    abiertas = pendientes(tareas)
    if proyecto:
        abiertas = [t for t in abiertas if str(t.get("proyecto_id")) == str(proyecto)]
    if vista == "hoy":
        elegidas = [t for t in abiertas if t.get("tipo_estado") == "in_progress"
                    or vencida(t, dia) or en_rango(t, dia, dia)]
    elif vista == "semana":
        lunes = lunes_de(dia)
        elegidas = [t for t in abiertas if t.get("tipo_estado") == "in_progress"
                    or vencida(t, lunes) or en_rango(t, lunes, lunes + timedelta(days=6))]
    else:
        elegidas = abiertas
    return sorted(elegidas, key=clave_orden)


def fmt_min(m):
    if not m:
        return "—"
    h, r = divmod(int(m), 60)
    return ("%dh %dm" % (h, r) if r else "%dh" % h) if h else "%dm" % r


def fmt_dia(t):
    if not t.get("fin"):
        return "sin día"
    fin = date.fromisoformat(t["fin"][:10])
    inicio = date.fromisoformat((t.get("inicio") or t["fin"])[:10])
    return fin.strftime("%d-%m") if inicio == fin else "%s a %s" % (inicio.strftime("%d-%m"), fin.strftime("%d-%m"))


def linea(t):
    partes = [str(t["id"]), t["nombre"] or "", t["proyecto"] or "sin proyecto", t["estado"] or "",
              fmt_dia(t), fmt_min(t.get("estimado_min"))]
    if t.get("prioridad") not in (None, "none"):
        partes.append("prioridad %s" % t["prioridad"])
    if t.get("area"):
        partes.append("área %s" % t["area"])
    if t.get("madre"):
        partes.append("paso de %s" % t["madre"])
    if t.get("etiquetas"):
        partes.append("#" + " #".join(t["etiquetas"]))
    return " · ".join(partes)


def texto(tareas, completo):
    """Una línea por tarea; debajo, la descripción y las notas (enteras o su primera línea)."""
    salida = []
    for t in tareas:
        salida.append(linea(t))
        for etiqueta, campo in (("descripción", "descripcion"), ("notas", "notas")):
            valor = (t.get(campo) or "").strip()
            if campo == "descripcion" and t.get("area"):
                valor = "\n".join(valor.splitlines()[1:]).strip()   # el área ya va en la línea
            if not valor:
                continue
            if not completo:
                if campo == "notas":
                    continue
                valor = valor.splitlines()[0]
            salida.append("    %s: %s" % (etiqueta, valor.replace("\n", "\n    ")))
    return "\n".join(salida) if salida else "(sin tareas)"


def leer_copia(ruta=None):
    try:
        return json.loads(Path(ruta or ruta_copia()).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def guardar_copia(tareas, momento, ruta=None):
    ruta = Path(ruta or ruta_copia())
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix(".tmp")
    temporal.write_text(json.dumps({"leida": momento.isoformat(), "tareas": tareas}, ensure_ascii=False),
                        encoding="utf-8")
    temporal.replace(ruta)   # atómico: una lectura a medias nunca ve un JSON cortado


def edad_min(copia, momento):
    if not copia or not copia.get("leida"):
        return None
    return (momento - datetime.fromisoformat(copia["leida"])).total_seconds() / 60


def obtener(max_edad, refrescar, momento=None, pedir=pedir_pagina, sesion=None):
    """La cola: de la copia si es reciente; si no, de Toggl. Devuelve (tareas, origen, aviso)."""
    momento = momento or ahora()
    copia = leer_copia()
    edad = edad_min(copia, momento)
    if not refrescar and edad is not None and edad <= max_edad:
        return copia["tareas"], "copia de hace %d min" % edad, None
    try:
        tareas = [reducir(t) for t in traer_todas(sesion or leer_sesion(momento=momento), pedir)]
    except SinSesion:
        raise
    except urllib.error.HTTPError as e:
        if e.code == 401:   # caducó antes de lo que decía expires_at, o se cerró la sesión
            raise SinSesion("Toggl rechazó el acceso (401); una consulta por el conector lo renueva")
        if copia:
            return copia["tareas"], "copia de hace %d min" % edad, "Toggl respondió %d" % e.code
        raise
    except (urllib.error.URLError, OSError, ValueError) as e:
        if copia:
            return copia["tareas"], "copia de hace %d min" % edad, "Toggl no respondió (%s)" % e
        raise
    guardar_copia(tareas, momento)
    return tareas, "Toggl, recién leída", None


def main(argv=None):
    p = argparse.ArgumentParser(description="Copia local de la cola de Toggl para el skill tarea.")
    sub = p.add_subparsers(dest="orden", required=True)
    le = sub.add_parser("leer")
    le.add_argument("--vista", choices=["hoy", "semana", "pendientes"], default="hoy")
    le.add_argument("--dia", type=date.fromisoformat, help="por defecto, hoy")
    le.add_argument("--proyecto", help="solo las de este proyecto (id de Toggl)")
    le.add_argument("--json", action="store_true")
    le.add_argument("--max-edad", type=int, default=MAX_EDAD_MIN, help="minutos que una copia sigue valiendo")
    le.add_argument("--refrescar", action="store_true", help="ir a Toggl aunque la copia sea reciente")
    ta = sub.add_parser("tarea")
    ta.add_argument("id")
    ta.add_argument("--json", action="store_true")
    sub.add_parser("invalidar")
    a = p.parse_args(argv)

    if a.orden == "invalidar":
        copia = leer_copia()
        if copia:
            copia["leida"] = "1970-01-01T00:00:00+00:00"
            guardar_copia(copia["tareas"], datetime.fromisoformat(copia["leida"]))
        print(json.dumps({"ok": True}))
        return 0

    if a.orden == "tarea":
        copia = leer_copia() or {"tareas": []}
        t = next((t for t in copia["tareas"] if str(t["id"]) == str(a.id)), None)
        if not t:
            print("No está en la copia: puede estar hecha, archivada o ser más nueva que la copia.", file=sys.stderr)
            return 2
        print(json.dumps(t, ensure_ascii=False) if a.json else texto([t], completo=True))
        return 0

    try:
        tareas, origen, aviso = obtener(a.max_edad, a.refrescar)
    except SinSesion as e:
        print("Sin sesión: %s." % e, file=sys.stderr)
        return 3
    except (urllib.error.URLError, OSError, ValueError) as e:
        print("Toggl no respondió y no hay copia local: %s." % e, file=sys.stderr)
        return 4
    dia = a.dia or datetime.now().astimezone().date()
    elegidas = filtrar(tareas, a.vista, dia, a.proyecto)
    if a.json:
        print(json.dumps({"origen": origen, "aviso": aviso, "vista": a.vista, "dia": dia.isoformat(),
                          "tareas": elegidas}, ensure_ascii=False))
    else:
        cabecera = "Cola de Toggl · vista %s · %s · %s" % (a.vista, dia.strftime("%d-%m"), origen)
        print(cabecera + ("\n(%s)" % aviso if aviso else ""))
        print(texto(elegidas, completo=(a.vista == "hoy")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
