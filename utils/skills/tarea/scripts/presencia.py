#!/usr/bin/env python3
"""
Registro de presencia: cuándo está el usuario trabajando, en qué proyecto y con qué aplicación.

Toggl solo sabe lo que alguien le dice. Si el cronómetro corre mientras el usuario se fue y Claude
sigue trabajando, cuenta ese tramo como suyo; si hay dos sesiones en paralelo, se lo quitan una a
otra (Toggl permite un solo cronómetro por persona). Este script resuelve las dos cosas sin hablar
con Toggl: guarda en local las señales de presencia y calcula, al cerrar una tarea, los tramos
exactos de cada uno. **Toggl es solo del usuario**: el tiempo de Claude no va allí, se asienta en un
registro local por proyecto y mes (`asentar`), que `balance` lee aparte.

Dos señales, unidas minuto a minuto (un minuto con las dos cuenta una vez):
  - actividad en el Mac: segundos sin teclado ni mouse (HIDIdleTime) y la aplicación en primer
    plano (lsappinfo). Nunca títulos de ventana ni lo que se escribe.
  - mensajes a Claude: el gancho UserPromptSubmit anota la hora y el proyecto de cada mensaje,
    venga del teclado del Mac o del celular por control remoto.

Todo el cálculo es determinista: las mismas marcas dan siempre los mismos tramos.

Uso:
    presencia.py registrar                         # cada minuto, desde launchd
    presencia.py mensaje < entrada-del-gancho.json  # desde el gancho UserPromptSubmit
    presencia.py marca --repo R --tarea ID --evento crear|abrir|pausar|retomar|cerrar
                       [--coste 45m] [--vence AAAA-MM-DD] [--hora ISO]
    presencia.py tramos --repo R --tarea ID [--hasta ISO] [--completo]
    presencia.py sesion [--hasta ISO]
    presencia.py resumen --desde AAAA-MM-DD --hasta AAAA-MM-DD
    presencia.py claude --desde AAAA-MM-DD --hasta AAAA-MM-DD
    presencia.py asentar [--hasta ISO]              # tiempo de Claude → registro local, por proyecto
    presencia.py mi-tiempo [--hasta ISO] [--desde ISO] [--enviado]   # tu tiempo, por aplicación
    presencia.py plan guardar|leer|comparar [--semana AAAA-Www] [--vigente]
    presencia.py abiertas [--repo R]               # tareas abiertas o en pausa (sin cerrar)

Todas las salidas son JSON salvo `mensaje`, que imprime el aviso de pausa (o nada) para que el
gancho lo pase a Claude como contexto. `registrar` y `mensaje` nunca fallan hacia fuera: un error
suyo no puede romper ni el Mac ni la conversación.

Códigos de salida: 0 bien · 2 error de uso.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from bisect import bisect_right
from datetime import date, datetime, timedelta
from pathlib import Path

DIR_DEFECTO = Path.home() / ".local" / "share" / "tarea" / "presencia"
CONFIG_DEFECTO = Path.home() / "Github" / "AI-kit" / "config" / "context" / "toggl.md"
# El tiempo de Claude, fuera de Toggl y fuera de todo repo: un archivo por proyecto y mes.
TIEMPO_DEFECTO = Path.home() / "Obsidian" / "global" / "claude" / "registro-tiempo"

# Valores por defecto; la configuración global los puede cambiar (tabla `| clave | valor |`).
AJUSTES = {
    "ausencia_min": 10,      # sin ninguna señal durante esto → ausente desde la última actividad
    "sesion_min": 90,        # sesión continua a partir de la cual se avisa
    "pausa_min": 10,         # hueco que cuenta como pausa y corta la sesión
    "repetir_aviso_min": 30,  # no se repite el aviso antes de esto
    "claude_hueco_min": 5,   # hueco entre mensajes de Claude que corta su tramo de trabajo
    "claude_herramienta_max_min": 30,  # un comando de Claude cuenta entero hasta esto
    "notificar_mac": 1,      # 1: el aviso de pausa también sale como notificación de macOS
    "proyecto_mi_tiempo": 0,  # id del proyecto de Toggl donde va tu tiempo frente al computador
}


def carpeta():
    return Path(os.environ.get("TAREA_PRESENCIA_DIR", DIR_DEFECTO)).expanduser()


def leer_ajustes():
    ajustes = dict(AJUSTES)
    ruta = Path(os.environ.get("TOGGL_CONFIG", CONFIG_DEFECTO)).expanduser()
    try:
        texto = ruta.read_text(encoding="utf-8")
    except OSError:
        return ajustes
    for clave in ajustes:
        m = re.search(r"^\|\s*`?%s`?\s*\|\s*(\d+)" % re.escape(clave), texto, re.M)
        if m:
            ajustes[clave] = int(m.group(1))
    return ajustes


def ahora():
    return datetime.now().astimezone().replace(microsecond=0)


def anotar(momento, *campos):
    """Una línea TSV en el archivo del día local. Añadir es atómico para líneas cortas."""
    d = carpeta()
    d.mkdir(parents=True, exist_ok=True)
    linea = "\t".join([momento.isoformat()] + [str(c).replace("\t", " ").replace("\n", " ") for c in campos])
    with open(d / ("%s.log" % momento.date().isoformat()), "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def leer_lineas(desde, hasta):
    """Todas las marcas entre dos fechas locales (inclusive), en orden."""
    d = carpeta()
    salida = []
    dia = desde
    while dia <= hasta:
        ruta = d / ("%s.log" % dia.isoformat())
        if ruta.exists():
            for linea in ruta.read_text(encoding="utf-8").splitlines():
                partes = linea.split("\t")
                if len(partes) < 2:
                    continue
                try:
                    momento = datetime.fromisoformat(partes[0])
                except ValueError:
                    continue
                salida.append((momento, partes[1], partes[2:]))
        dia += timedelta(days=1)
    salida.sort(key=lambda x: x[0])
    return salida


def minuto(m):
    return m.replace(second=0, microsecond=0)


# ── Señales ───────────────────────────────────────────────────────────────────────────────────


def segundos_inactivo():
    salida = subprocess.run(["ioreg", "-c", "IOHIDSystem"], capture_output=True, text=True, timeout=10).stdout
    m = re.search(r'"HIDIdleTime"\s*=\s*(\d+)', salida)
    return int(m.group(1)) // 1_000_000_000 if m else None


def app_al_frente():
    asn = subprocess.run(["lsappinfo", "front"], capture_output=True, text=True, timeout=10).stdout.strip()
    if not asn:
        return "-"
    info = subprocess.run(["lsappinfo", "info", "-only", "name", asn], capture_output=True, text=True, timeout=10).stdout
    m = re.search(r'"([^"]+)"', info)
    return m.group(1) if m else "-"


def proyecto_de(cwd):
    """El nombre del repo (raíz de git) o, si no hay git, el de la carpeta."""
    if not cwd:
        return "-"
    try:
        raiz = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        raiz = ""
    return Path(raiz or cwd).name


def minutos_activos(lineas):
    """Minutos con alguna señal. El Mac muestrea cada minuto: si hubo teclado o mouse en el último
    minuto (inactivo < 60 s), ese minuto y los anteriores cubiertos por el muestreo cuentan."""
    activos = {}
    for momento, tipo, campos in lineas:
        if tipo == "mac" and campos:
            try:
                inactivo = int(campos[0])
            except ValueError:
                continue
            if inactivo < 60:
                activos.setdefault(minuto(momento), {})["app"] = campos[1] if len(campos) > 1 else "-"
        elif tipo == "mensaje":
            activos.setdefault(minuto(momento), {})["proyecto"] = campos[0] if campos else "-"
    return activos


def tramos_presentes(activos, ausencia_min):
    """Une los minutos activos en tramos: un hueco menor que `ausencia_min` sigue siendo presencia
    (leer, pensar); uno mayor es ausencia desde la última actividad."""
    tramos = []
    for m in sorted(activos):
        fin = m + timedelta(minutes=1)
        if tramos and m - tramos[-1][1] < timedelta(minutes=ausencia_min):
            tramos[-1][1] = max(tramos[-1][1], fin)
        else:
            tramos.append([m, fin])
    return [(a, b) for a, b in tramos]


def cortar(intervalos, presentes):
    """Intersección de dos listas de intervalos ordenados."""
    salida = []
    for a1, b1 in intervalos:
        for a2, b2 in presentes:
            a, b = max(a1, a2), min(b1, b2)
            if a < b:
                salida.append((a, b))
    return salida


# ── Tareas ────────────────────────────────────────────────────────────────────────────────────


def eventos_tarea(lineas, repo, tarea):
    return [(m, c[2], c[3:]) for m, t, c in lineas
            if t == "tarea" and len(c) >= 3 and c[0] == repo and c[1] == tarea]


def abierta_en(eventos, hasta):
    """Intervalos en que la tarea estuvo abierta (abrir/retomar → pausar/cerrar)."""
    intervalos, inicio = [], None
    for m, evento, _ in eventos:
        if evento in ("abrir", "retomar") and inicio is None:
            inicio = m
        elif evento in ("pausar", "cerrar") and inicio is not None:
            intervalos.append((inicio, m))
            inicio = None
    if inicio is not None:
        intervalos.append((inicio, hasta))
    return intervalos


def datos_creacion(eventos):
    datos = {}
    for _, evento, extra in eventos:
        if evento == "crear":
            for par in extra:
                if "=" in par:
                    k, v = par.split("=", 1)
                    datos[k] = v
    return datos


def fmt_duracion(segundos):
    h, m = divmod(int(round(segundos / 60)), 60)
    return ("%dh %dm" % (h, m)) if h else ("%dm" % m)


def calcular_tramos(repo, tarea, hasta, ajustes, completo=False):
    # Una tarea abierta hace más de 120 días no se mide aquí: su tiempo sale de git, con `~`.
    desde = hasta.date() - timedelta(days=120)
    lineas = leer_lineas(desde, hasta.date())
    eventos = eventos_tarea(lineas, repo, tarea)
    if not eventos:
        return {"repo": repo, "tarea": tarea, "error": "sin marcas de esta tarea"}
    abiertos = abierta_en(eventos, hasta)
    presentes = tramos_presentes(minutos_activos(lineas), ajustes["ausencia_min"])
    # `completo`: el usuario confirmó que trabajó fuera del computador (una reunión, una llamada):
    # el tramo abierto cuenta entero, sin recortar por presencia.
    trabajados = abiertos if completo else cortar(abiertos, presentes)
    abierto_s = sum((b - a).total_seconds() for a, b in abiertos)
    trabajado_s = sum((b - a).total_seconds() for a, b in trabajados)
    creacion = datos_creacion(eventos)
    # Nada de esto va a Toggl. Tu tiempo lo cronometras tú con la app de Toggl; aquí queda en
    # `duracion`, para el historial. El de Claude en su repo mientras la tarea estuvo abierta queda en
    # `claude`, también para el historial; su registro lo lleva `asentar`.
    claude = []
    if abiertos and repo != "sin-repo":
        claude = cortar(tramos_claude(abiertos[0][0], hasta, ajustes, repo).get(repo, []), abiertos)
    return {
        "repo": repo,
        "tarea": tarea,
        "inicio": trabajados[0][0].isoformat() if trabajados else None,
        "fin": trabajados[-1][1].isoformat() if trabajados else None,
        "duracion_s": int(trabajado_s),
        "duracion": fmt_duracion(trabajado_s),
        "descontado": fmt_duracion(max(0, abierto_s - trabajado_s)),
        "descontado_s": int(max(0, abierto_s - trabajado_s)),
        "coste": creacion.get("coste"),
        "vence": creacion.get("vence"),
        "claude": reparto_claude(claude, presentes),
    }


# ── Sesión continua y aviso ───────────────────────────────────────────────────────────────────


def sesion_actual(hasta, ajustes):
    lineas = leer_lineas(hasta.date() - timedelta(days=1), hasta.date())
    presentes = tramos_presentes(minutos_activos(lineas), ajustes["pausa_min"])
    if not presentes:
        return None
    inicio, fin = presentes[-1]
    if hasta - fin >= timedelta(minutes=ajustes["pausa_min"]):
        return None
    return {"inicio": inicio.isoformat(), "minutos": int((min(fin, hasta + timedelta(minutes=1)) - inicio).total_seconds() // 60)}


def aviso_pausa(hasta, ajustes):
    sesion = sesion_actual(hasta, ajustes)
    if not sesion or sesion["minutos"] < ajustes["sesion_min"]:
        return None
    estado = carpeta() / "aviso.json"
    try:
        previo = json.loads(estado.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        previo = {}
    ultimo = previo.get("ultimo")
    misma_sesion = previo.get("sesion") == sesion["inicio"]
    if ultimo and misma_sesion and hasta - datetime.fromisoformat(ultimo) < timedelta(minutes=ajustes["repetir_aviso_min"]):
        return None
    estado.write_text(json.dumps({"ultimo": hasta.isoformat(), "sesion": sesion["inicio"]}), encoding="utf-8")
    return sesion


def notificar(titulo, texto):
    """Notificación de macOS. El texto va como argumento, nunca dentro del código AppleScript."""
    subprocess.run(["osascript", "-e", "on run argv",
                    "-e", 'display notification (item 2 of argv) with title (item 1 of argv) sound name "Glass"',
                    "-e", "end run", titulo, texto], capture_output=True, timeout=10)


def avisar_desde_el_mac(hasta, inactivo, ajustes):
    """El aviso de pausa sin depender de que el usuario le escriba a Claude. Comparte `aviso.json`
    con el gancho: sale por uno o por otro, nunca por los dos. Solo con alguien frente al Mac."""
    if not ajustes["notificar_mac"] or inactivo >= 60:
        return None
    aviso = aviso_pausa(hasta, ajustes)
    if aviso:
        notificar("Toca una pausa", "Llevas %s seguidas sin una pausa de %d min."
                  % (fmt_duracion(aviso["minutos"] * 60), ajustes["pausa_min"]))
    return aviso


# ── Resúmenes ─────────────────────────────────────────────────────────────────────────────────


def resumen(desde, hasta, ajustes):
    lineas = leer_lineas(desde, hasta)
    activos = minutos_activos(lineas)
    presentes = tramos_presentes(activos, ajustes["ausencia_min"])
    sesiones = tramos_presentes(activos, ajustes["pausa_min"])
    dias = {}
    # Atención: cada minuto presente va al repo en que trabajaba la sesión a la que se escribió por
    # última vez (no a la carpeta donde se abrió esa sesión).
    brutos = sorted((m, c[0], c[1] if len(c) > 1 else None) for m, t, c in lineas if t == "mensaje" and c)
    inicio = datetime.combine(desde, datetime.min.time()).astimezone()
    fin = datetime.combine(hasta + timedelta(days=1), datetime.min.time()).astimezone()
    de_claude = leer_sesiones(inicio, fin, ajustes)
    # Desempeño: cuánto de tu tiempo fue con Claude trabajando en algún proyecto, y cuántas horas de
    # Claude salieron por cada hora tuya.
    claude = tramos_claude(inicio, fin, ajustes, sesiones=de_claude)
    union = unir(sorted(x for v in claude.values() for x in v))
    inicios_union = [a for a, _ in union]
    mensajes = [(minuto(m), anotado, sesion_del_mensaje(de_claude, m, sid)) for m, anotado, sid in brutos]
    horas_msg = [t for t, _, _ in mensajes]
    for a, b in presentes:
        m = a
        while m < b:
            dia = dias.setdefault(m.date().isoformat(), {"minutos": 0, "atencion": {}, "apps": {}})
            dia["minutos"] += 1
            i = bisect_right(horas_msg, m)
            proyecto = "-"
            if i:
                _, anotado, sid = mensajes[i - 1]
                proyecto = (repo_de_sesion(de_claude[sid], m) if sid else None) or anotado
            dia["atencion"][proyecto] = dia["atencion"].get(proyecto, 0) + 1
            app = activos.get(m, {}).get("app")
            if app:
                dia["apps"][app] = dia["apps"].get(app, 0) + 1
            j = bisect_right(inicios_union, m)
            if j and m < union[j - 1][1]:
                dia["con_claude_min"] = dia.get("con_claude_min", 0) + 1
            m += timedelta(minutes=1)
    for a, b in sesiones:
        dia = dias.setdefault(a.date().isoformat(), {"minutos": 0, "atencion": {}, "apps": {}})
        largo = int((b - a).total_seconds() // 60)
        dia["sesion_max_min"] = max(dia.get("sesion_max_min", 0), largo)
        dia["sesiones"] = dia.get("sesiones", 0) + 1
    for tramos in claude.values():
        for a, b in tramos:
            while a < b:   # partido por día
                corte = min(b, datetime.combine(a.date() + timedelta(days=1), datetime.min.time()).astimezone())
                dia = dias.setdefault(a.date().isoformat(), {"minutos": 0, "atencion": {}, "apps": {}})
                dia["claude_min"] = dia.get("claude_min", 0) + (corte - a).total_seconds() / 60
                a = corte
    for dia in dias.values():
        dia["pausas"] = max(0, dia.get("sesiones", 1) - 1)
        dia["horas"] = fmt_duracion(dia["minutos"] * 60)
        dia.update(desempeno(dia["minutos"], dia.get("con_claude_min", 0), dia.get("claude_min", 0)))
    total = sum(d["minutos"] for d in dias.values())
    salida = {"desde": desde.isoformat(), "hasta": hasta.isoformat(), "total": fmt_duracion(total * 60),
              "total_min": total, "dias": dias}
    salida.update(desempeno(total, sum(d.get("con_claude_min", 0) for d in dias.values()),
                            sum(d.get("claude_min", 0) for d in dias.values())))
    return salida


def desempeno(tuyos, con_claude, de_claude):
    """Tu tiempo con y sin Claude trabajando, qué parte fue con Claude en algún proyecto, y cuántas
    horas de Claude (sumadas por proyecto) salieron por cada hora tuya."""
    return {"con_claude_min": int(con_claude), "sin_claude_min": int(tuyos - con_claude),
            "sin_claude": fmt_duracion((tuyos - con_claude) * 60),
            "en_proyectos_pct": round(100 * con_claude / tuyos) if tuyos else None,
            "claude_min": int(round(de_claude)),
            "rendimiento": round(de_claude / tuyos, 1) if tuyos else None}


def unir(intervalos):
    """Une intervalos ordenados que se tocan o se pisan."""
    salida = []
    for a, b in intervalos:
        if salida and a <= salida[-1][1]:
            salida[-1] = (salida[-1][0], max(salida[-1][1], b))
        else:
            salida.append((a, b))
    return salida


def raiz_claude():
    return Path(os.environ.get("CLAUDE_PROYECTOS_DIR", Path.home() / ".claude" / "projects")).expanduser()


RUTA = re.compile(r"(~|\$HOME)?(/[^\s\"'`\\,;()\[\]]+)")


class Raices:
    """La raíz de git de cada carpeta, con caché (una consulta a git por carpeta)."""

    def __init__(self):
        self.cache = {}

    def de(self, ruta):
        d = Path(ruta)
        while not d.is_dir() and d != d.parent:
            d = d.parent
        clave = str(d)
        if d == d.parent:   # la raíz del disco: una URL o una ruta que no existe
            return None
        if clave not in self.cache:
            try:
                r = subprocess.run(["git", "-C", clave, "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True, timeout=5).stdout.strip()
            except (OSError, subprocess.SubprocessError):
                r = ""
            self.cache[clave] = r or None
        return self.cache[clave]


def repos_tocados(d, raices):
    """Raíces de git de las rutas que usan las herramientas de una respuesta, en orden."""
    salida = []
    for x in (d.get("message") or {}).get("content") or []:
        if isinstance(x, dict) and x.get("type") == "tool_use":
            for m in RUTA.finditer(json.dumps(x.get("input") or {}, ensure_ascii=False)):
                r = raices.de((str(Path.home()) if m.group(1) else "") + m.group(2))
                if r and r not in salida:
                    salida.append(r)
    return salida


def leer_sesiones(desde, hasta, ajustes):
    """Una pasada por las sesiones locales de Claude Code (subagentes incluidos). Por sesión: sus
    marcas de trabajo `(inicio, fin, raíz)`, sus cambios de repo `(hora, raíz)` y la hora de cada
    mensaje del usuario.

    **El repo de una respuesta es el de los archivos que toca**, no el de la carpeta donde se abrió
    la sesión: una sesión abierta en un repo puede pasarse el día trabajando en otro. Si una
    respuesta no toca archivos, sigue en el repo de la última que sí; al principio, en el de la
    carpeta. Cada respuesta marca un minuto; un comando largo cuenta entero, de la respuesta que lo
    lanzó a su resultado (hasta `claude_herramienta_max_min`). `desde` y `hasta`, con zona."""
    herramienta = timedelta(minutes=ajustes["claude_herramienta_max_min"])
    raices, sesiones, raiz = Raices(), {}, raiz_claude()
    for archivo in raiz.rglob("*.jsonl") if raiz.exists() else []:
        try:
            if datetime.fromtimestamp(archivo.stat().st_mtime).astimezone() < desde:
                continue
            s = {"marcas": [], "cambios": [], "mensajes": []}
            actual = ultima = None
            with open(archivo, encoding="utf-8") as f:
                for linea in f:
                    if '"timestamp"' not in linea:
                        continue
                    try:
                        d = json.loads(linea)
                        t = datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")).astimezone()
                    except (ValueError, KeyError, TypeError, AttributeError):
                        continue
                    if actual is None and d.get("cwd"):
                        actual = raices.de(d["cwd"]) or d["cwd"]
                        s["cambios"].append((t, actual))
                    tipo = d.get("type")
                    if tipo == "assistant":
                        tocados = repos_tocados(d, raices)
                        if tocados and tocados[0] != actual:
                            actual = tocados[0]
                            s["cambios"].append((t, actual))
                        tramo, ultima = (t, t), t
                    elif tipo == "user" and es_resultado(d):
                        if not ultima or t - ultima > herramienta:
                            continue
                        tramo = (ultima, t)
                    elif tipo == "user":
                        if desde <= t < hasta:
                            s["mensajes"].append(t)
                        continue
                    else:
                        continue
                    if actual and tramo[1] >= desde and tramo[0] < hasta:
                        s["marcas"].append((tramo[0], tramo[1] + timedelta(minutes=1), actual))
        except OSError:
            continue
        sesiones[archivo.stem] = s
    return sesiones


def nombre_repo(raiz):
    return Path(raiz).name if raiz else "-"


def tramos_claude(desde, hasta, ajustes, proyecto=None, sesiones=None):
    """Tramos en que Claude trabajó, por proyecto (nombre del repo). Las marcas se unen con
    `claude_hueco_min` y **entre sesiones**: un minuto con dos sesiones o un subagente en el mismo
    repo cuenta una vez; en dos repos distintos cuenta en los dos, porque se trabajó en los dos."""
    hueco = timedelta(minutes=ajustes["claude_hueco_min"])
    if sesiones is None:
        sesiones = leer_sesiones(desde, hasta, ajustes)
    marcas = {}
    for s in sesiones.values():
        for a, b, raiz in s["marcas"]:
            nombre = nombre_repo(raiz)
            if not proyecto or nombre == proyecto:
                marcas.setdefault(nombre, []).append((a, b))
    salida = {}
    for nombre, lista in marcas.items():
        unidos = []
        for a, b in sorted(lista):
            if unidos and a - unidos[-1][1] < hueco:
                unidos[-1][1] = max(unidos[-1][1], b)
            else:
                unidos.append([a, b])
        salida[nombre] = [(max(a, desde), min(b, hasta)) for a, b in unidos]
    return salida


def repo_de_sesion(s, momento):
    """En qué repo estaba trabajando una sesión en un momento dado."""
    actual = s["cambios"][0][1] if s["cambios"] else None
    for t, raiz in s["cambios"]:
        if t > momento:
            break
        actual = raiz
    return nombre_repo(actual) if actual else None


def sesion_del_mensaje(sesiones, momento, anotada=None):
    """La sesión a la que fue un mensaje: la anotada por el gancho o, en las marcas antiguas que no
    la traen, la que recibió un mensaje del usuario a menos de 2 minutos."""
    if anotada and anotada in sesiones:
        return anotada
    mejor, distancia = None, timedelta(minutes=2)
    for sid, s in sesiones.items():
        for t in s["mensajes"]:
            if abs(t - momento) <= distancia:
                mejor, distancia = sid, abs(t - momento)
    return mejor


def es_resultado(d):
    contenido = (d.get("message") or {}).get("content")
    return isinstance(contenido, list) and any(isinstance(x, dict) and x.get("type") == "tool_result" for x in contenido)


def reparto_claude(claude, presentes):
    """Claude total, con el usuario presente y solo, en segundos y legible."""
    total = sum((b - a).total_seconds() for a, b in claude)
    con = sum((b - a).total_seconds() for a, b in cortar(claude, presentes))
    return {"claude_s": int(total), "con_usuario_s": int(con), "solo_s": int(total - con),
            "claude": fmt_duracion(total), "con_usuario": fmt_duracion(con), "solo": fmt_duracion(total - con)}


def restar(intervalos, quitar):
    """Lo de `intervalos` que no cae en ningún intervalo de `quitar`."""
    salida = []
    for a, b in intervalos:
        trozos = [(a, b)]
        for qa, qb in quitar:
            nuevos = []
            for x, y in trozos:
                if qb <= x or qa >= y:
                    nuevos.append((x, y))
                    continue
                if x < qa:
                    nuevos.append((x, qa))
                if qb < y:
                    nuevos.append((qb, y))
            trozos = nuevos
        salida.extend(trozos)
    return salida


def enlace_toggl(raiz):
    """El proyecto y el cliente de Toggl de un repo, del marcador de su `tareas/toggl.md`, o None."""
    try:
        texto = (Path(raiz) / "tareas" / "toggl.md").read_text(encoding="utf-8")
    except (OSError, TypeError):
        return None
    m = re.search(r"<!--\s*tarea:\s*toggl\s*·\s*proyecto\s+(\d+)\s*«([^»]*)»"
                  r"(?:\s*·\s*cliente\s+(\d+)\s*«([^»]*)»)?", texto)
    if not m:
        return None
    return {"proyecto_id": int(m.group(1)), "proyecto": m.group(2).strip(),
            "cliente_id": int(m.group(3)) if m.group(3) else None, "cliente": (m.group(4) or "").strip() or None}


def slug(texto):
    plano = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", plano.lower()).strip("-") or "sin-proyecto"


def carpeta_tiempo():
    return Path(os.environ.get("CLAUDE_TIEMPO_DIR", TIEMPO_DEFECTO)).expanduser()


def partir_por_dia(a, b):
    while a < b:
        corte = min(b, datetime.combine(a.date() + timedelta(days=1), datetime.min.time()).astimezone())
        yield a, corte
        a = corte


def ultimo_asiento(lineas):
    marcas = [datetime.fromisoformat(c[0]) for m, t, c in lineas if t == "claude-asentado" and c]
    return max(marcas) if marcas else None


def calcular_asiento(desde, hasta, lineas, ajustes, sesiones=None):
    """Los tramos de Claude entre `desde` y `hasta`, uno por fila: repo, tarea abierta en ese repo
    (o `—`), minutos y cuánto fue solo, sin el usuario presente. Si dos tareas del mismo repo
    estuvieron abiertas a la vez, el tramo va a la que se abrió después: nunca cuenta dos veces."""
    abiertas = {}
    for repo, tarea in {(c[0], c[1]) for m, t, c in lineas if t == "tarea" and len(c) >= 3}:
        for a, b in abierta_en(eventos_tarea(lineas, repo, tarea), hasta):
            abiertas.setdefault(repo, []).append((a, b, tarea))
    if sesiones is None:
        sesiones = leer_sesiones(desde, hasta, ajustes)
    raices = {nombre_repo(r): r for s in sesiones.values() for _, _, r in s["marcas"]}
    presentes = tramos_presentes(minutos_activos(lineas), ajustes["ausencia_min"])
    # Un día sin ninguna señal de presencia (antes de instalar el registro, o con el Mac apagado y
    # sin mensajes) no permite afirmar que Claude trabajó solo: su «Solo» queda en blanco (`—`).
    con_presencia = {m.date() for m, t, _ in lineas if t in ("mac", "mensaje")}
    filas = []
    for nombre, tramos in sorted(tramos_claude(desde, hasta, ajustes, sesiones=sesiones).items()):
        piezas, resto = [], tramos
        for a, b, tarea in sorted(abiertas.get(nombre, []), key=lambda x: x[0], reverse=True):
            piezas += [(x, y, tarea) for x, y in cortar(resto, [(a, b)])]
            resto = restar(resto, [(a, b)])
        piezas += [(x, y, "—") for x, y in resto]
        enlace = enlace_toggl(raices.get(nombre))
        for x, y, tarea in sorted(piezas):
            for a, b in partir_por_dia(x, y):
                if (b - a).total_seconds() < 1:   # restos de un corte: nada que contar
                    continue
                con = sum((q - p).total_seconds() for p, q in cortar([(a, b)], presentes))
                filas.append({"inicio": a, "fin": b, "repo": nombre, "tarea": tarea, "enlace": enlace,
                              "segundos": int((b - a).total_seconds()),
                              "solo_s": int((b - a).total_seconds() - con) if a.date() in con_presencia else None})
    return filas


def archivo_de(fila):
    """`<proyecto>-AAAA-MM.md`: el nombre del proyecto de Toggl; sin enlace, el del repo."""
    nombre = fila["enlace"]["proyecto"] if fila["enlace"] else ("sin-proyecto" if fila["repo"] == "-" else fila["repo"])
    return carpeta_tiempo() / ("%s-%s.md" % (slug(nombre), fila["inicio"].strftime("%Y-%m")))


def encabezado_tiempo(fila):
    e = fila["enlace"] or {}
    proyecto = e.get("proyecto") or ("sin proyecto" if fila["repo"] == "-" else fila["repo"])
    marcador = "<!-- tiempo-claude · proyecto %s «%s» · cliente %s «%s» · lo escribe presencia.py asentar -->" % (
        e.get("proyecto_id") or "-", proyecto, e.get("cliente_id") or "-", e.get("cliente") or "-")
    return (marcador + "\n\n# Tiempo de Claude · %s · %s\n\n"
            "Lo que trabajó Claude en este proyecto, tramo a tramo. No va a Toggl ni se suma con tu tiempo.\n"
            "«Solo»: minutos sin ti delante (`—` si ese día no hay registro de presencia). «Tarea»: la que\n"
            "estaba abierta en el repo, o `—`.\n\n"
            "| Fecha | Inicio | Fin | Min | Solo | Repo | Tarea |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n") % (proyecto, fila["inicio"].strftime("%Y-%m"))


def asentar(hasta, ajustes, dias=31):
    """Escribe en el registro local el tiempo de Claude desde el último asiento (o 31 días atrás:
    Claude Code borra sus sesiones a los 30) y anota hasta dónde llegó. Idempotente: una segunda
    pasada no repite nada."""
    lineas = leer_lineas(hasta.date() - timedelta(days=dias), hasta.date())
    desde = ultimo_asiento(lineas) or datetime.combine(hasta.date() - timedelta(days=dias), datetime.min.time()).astimezone()
    filas = calcular_asiento(desde, hasta, lineas, ajustes) if desde < hasta else []
    por_archivo = {}
    for f in filas:
        por_archivo.setdefault(archivo_de(f), []).append(f)
    for ruta, lista in por_archivo.items():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        nuevo = not ruta.exists()
        with open(ruta, "a", encoding="utf-8") as out:
            if nuevo:
                out.write(encabezado_tiempo(lista[0]))
            for f in lista:
                out.write("| %s | %s | %s | %d | %s | %s | %s |\n" % (
                    f["inicio"].date().isoformat(), f["inicio"].strftime("%H:%M:%S"), f["fin"].strftime("%H:%M:%S"),
                    round(f["segundos"] / 60), "—" if f["solo_s"] is None else round(f["solo_s"] / 60),
                    f["repo"], f["tarea"]))
    if desde < hasta:
        anotar(hasta, "claude-asentado", hasta.isoformat())
    return {"desde": desde.isoformat(), "hasta": hasta.isoformat(), "filas": len(filas),
            "archivos": {str(r): fmt_duracion(sum(f["segundos"] for f in l)) for r, l in por_archivo.items()}}


FILA_TIEMPO = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d{2}:\d{2}(?::\d{2})?)\s*\|\s*(\d{2}:\d{2}(?::\d{2})?)\s*\|"
                         r"\s*\d+\s*\|\s*(\d+|—)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
PROYECTO_TIEMPO = re.compile(r"<!--\s*tiempo-claude\s*·\s*proyecto\s+\S+\s*«([^»]*)»")


def leer_registro(desde, hasta):
    """Las filas asentadas entre dos fechas locales, con el proyecto de su archivo."""
    filas, d = [], carpeta_tiempo()
    for ruta in sorted(d.glob("*-[0-9][0-9][0-9][0-9]-[0-9][0-9].md")) if d.exists() else []:
        texto = ruta.read_text(encoding="utf-8")
        m = PROYECTO_TIEMPO.search(texto)
        proyecto = m.group(1) if m else ruta.stem[:-8]
        for linea in texto.splitlines():
            f = FILA_TIEMPO.match(linea)
            if not f or not (desde.isoformat() <= f.group(1) <= hasta.isoformat()):
                continue
            dia = date.fromisoformat(f.group(1))
            a, b = (datetime.combine(dia, datetime.strptime(h if len(h) == 8 else h + ":00", "%H:%M:%S").time()).astimezone()
                    for h in (f.group(2), f.group(3)))
            if b <= a:   # un tramo que termina a medianoche
                b += timedelta(days=1)
            filas.append({"proyecto": proyecto, "repo": f.group(5), "tarea": f.group(6),
                          "segundos": int((b - a).total_seconds()),
                          "solo_s": None if f.group(4) == "—" else int(f.group(4)) * 60})
    return filas


def claude_solo(desde, hasta, ajustes):
    """Cuánto trabajó Claude en el período, por repo y por proyecto de Toggl: lo asentado en el
    registro local más lo que aún no se asentó, calculado al vuelo **sin escribir nada**."""
    limite_a = datetime.combine(desde, datetime.min.time()).astimezone()
    limite_b = datetime.combine(hasta + timedelta(days=1), datetime.min.time()).astimezone()
    lineas = leer_lineas(desde - timedelta(days=31), max(hasta, ahora().date()))
    asentado = ultimo_asiento(lineas)
    filas = leer_registro(desde, hasta) if asentado else []
    cola_desde = max(limite_a, asentado) if asentado else limite_a
    if cola_desde < limite_b:
        for f in calcular_asiento(cola_desde, min(limite_b, ahora()), lineas, ajustes):
            e = f["enlace"]
            filas.append({"proyecto": e["proyecto"] if e else ("sin proyecto" if f["repo"] == "-" else f["repo"]),
                          "repo": f["repo"], "tarea": f["tarea"], "segundos": f["segundos"], "solo_s": f["solo_s"]})

    def reparto(lista):
        """Contigo y solo, sobre lo que tiene presencia; lo que no, aparte (`sin_presencia`)."""
        total = sum(f["segundos"] for f in lista)
        sin = sum(f["segundos"] for f in lista if f["solo_s"] is None)
        solo = min(total - sin, sum(f["solo_s"] for f in lista if f["solo_s"] is not None))
        return {"claude_s": total, "con_usuario_s": total - sin - solo, "solo_s": solo, "sin_presencia_s": sin,
                "claude": fmt_duracion(total), "con_usuario": fmt_duracion(total - sin - solo),
                "solo": fmt_duracion(solo), "sin_presencia": fmt_duracion(sin)}

    repos, proyectos = {}, {}
    for f in filas:
        repos.setdefault(f["repo"], []).append(f)
        proyectos.setdefault(f["proyecto"], []).append(f)
    return {"desde": desde.isoformat(), "hasta": hasta.isoformat(),
            "asentado_hasta": asentado.isoformat() if asentado else None,
            "repos": {k: reparto(v) for k, v in repos.items()},
            "proyectos": {k: reparto(v) for k, v in proyectos.items()}}


def mi_tiempo(hasta, ajustes, dias=31, desde=None):
    """Tu tiempo frente al computador desde el último envío (o desde el inicio del día): un registro
    por tramo continuo de presencia, con sus aplicaciones principales en la descripción. Los minutos
    sin muestra propia (leyendo, pensando, un mensaje desde el celular) cuentan en el tramo. Va a
    Toggl a un proyecto propio, sin cliente: no es tiempo de proyecto."""
    lineas = leer_lineas(hasta.date() - timedelta(days=dias), hasta.date())
    envios = [datetime.fromisoformat(c[1]) for m, t, c in lineas if t == "mi-tiempo" and len(c) > 1 and c[0] == "enviado"]
    if desde is None:
        desde = max(envios) if envios else datetime.combine(hasta.date(), datetime.min.time()).astimezone()
    activos = minutos_activos(lineas)
    registros, total = [], 0
    for a, b in cortar(tramos_presentes(activos, ajustes["ausencia_min"]), [(desde, hasta)]):
        apps, m = {}, minuto(a)
        while m < b:
            app = (activos.get(m, {}).get("app") or "").replace("\u200e", "").strip()
            if app and app not in ("-", "loginwindow"):
                apps[app] = apps.get(app, 0) + 1
            m += timedelta(minutes=1)
        if not apps or (b - a).total_seconds() < 60:
            continue   # solo la pantalla de inicio de sesión, o un instante: no es trabajo frente al Mac
        total += (b - a).total_seconds()
        principales = sorted(apps.items(), key=lambda x: -x[1])[:3]
        registros.append({"start": a.replace(microsecond=0).isoformat(), "duration": int((b - a).total_seconds()),
                          "type": "activity",
                          "description": " · ".join("%s %s" % (n, fmt_duracion(v * 60)) for n, v in principales)})
    return {"desde": desde.isoformat(), "hasta": hasta.isoformat(),
            "proyecto_toggl": ajustes["proyecto_mi_tiempo"] or None,
            "total": fmt_duracion(total), "total_s": int(total), "registros": registros}


def instante(s):
    """Una fecha de Toggl (RFC3339, con `Z` o con desfase) en hora local."""
    return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone()


def verificar(entradas, ajustes, tolerancia_min=5):
    """Compara los registros que cronometraste en Toggl con tu actividad en el Mac. Solo lee: dice
    cuánto de cada registro tuvo actividad, si el cronómetro partió tarde o siguió tras tu última
    actividad, las pausas de dentro y las aplicaciones principales. No sabe qué hacías fuera del
    computador ni separa dos trabajos hechos en las mismas aplicaciones."""
    rangos = []
    for e in entradas:
        a = instante(e["start"])
        if e.get("duration") not in (None, "") and int(e["duration"]) >= 0:
            b = a + timedelta(seconds=int(e["duration"]))
        elif e.get("stop"):
            b = instante(e["stop"])
        else:
            continue   # un cronómetro en marcha: se verifica cuando pare
        rangos.append((e, a, b))
    if not rangos:
        return {"registros": []}
    desde = min(a for _, a, _ in rangos).date() - timedelta(days=1)
    hasta = max(b for _, _, b in rangos).date()
    activos = minutos_activos(leer_lineas(desde, hasta))
    presentes = tramos_presentes(activos, ajustes["ausencia_min"])
    hueco = timedelta(minutes=ajustes["ausencia_min"])
    salida = []
    for e, a, b in rangos:
        dentro = cortar([(a, b)], presentes)
        activo_s = sum((y - x).total_seconds() for x, y in dentro)
        # Partió tarde: venías trabajando sin corte hasta el inicio del registro.
        antes = [x for x, y in presentes if x < a < y]
        antes_min = int((a - antes[0]).total_seconds() // 60) if antes else 0
        # Siguió corriendo: desde tu última actividad dentro del registro hasta que lo paraste.
        ultimo = dentro[-1][1] if dentro else a
        despues_min = int((b - ultimo).total_seconds() // 60)
        primero = dentro[0][0] if dentro else b
        sin_actividad_al_inicio_min = int((primero - a).total_seconds() // 60)
        pausas = [{"desde": x.isoformat(), "min": int((y - x).total_seconds() // 60)}
                  for (_, x), (y, _) in zip(dentro, dentro[1:]) if y - x >= hueco]
        apps, m = {}, minuto(a)
        while m < b:
            app = (activos.get(m, {}).get("app") or "").replace("\u200e", "").strip()
            if app and app not in ("-", "loginwindow"):
                apps[app] = apps.get(app, 0) + 1
            m += timedelta(minutes=1)
        avisos = []
        if antes_min >= tolerancia_min:
            avisos.append("venías activo %s antes de iniciarlo" % fmt_duracion(antes_min * 60))
        if sin_actividad_al_inicio_min >= tolerancia_min:
            avisos.append("%s sin actividad al empezar" % fmt_duracion(sin_actividad_al_inicio_min * 60))
        if despues_min >= tolerancia_min:
            avisos.append("siguió %s tras tu última actividad" % fmt_duracion(despues_min * 60))
        for pz in pausas:
            avisos.append("pausa de %s a las %s" % (fmt_duracion(pz["min"] * 60), pz["desde"][11:16]))
        salida.append({
            "id": e.get("id"), "descripcion": e.get("description") or e.get("descripcion") or "",
            "inicio": a.isoformat(), "fin": b.isoformat(),
            "registrado": fmt_duracion((b - a).total_seconds()), "registrado_s": int((b - a).total_seconds()),
            "activo": fmt_duracion(activo_s), "activo_s": int(activo_s),
            "antes_min": antes_min, "sin_actividad_al_inicio_min": sin_actividad_al_inicio_min,
            "despues_min": despues_min, "pausas": pausas,
            "apps": " · ".join("%s %s" % (n, fmt_duracion(v * 60))
                               for n, v in sorted(apps.items(), key=lambda x: -x[1])[:3]),
            "avisos": avisos,
        })
    return {"registros": salida}


def tareas_abiertas(hasta, repo=None, dias=30):
    """Estado de cada tarea con marcas recientes: la última marca manda. Es la forma local de saber
    cuáles quedaron abiertas o en pausa, sin preguntarle a Toggl."""
    lineas = leer_lineas(hasta.date() - timedelta(days=dias), hasta.date())
    ultimo = {}
    for m, t, c in lineas:
        if t == "tarea" and len(c) >= 3 and (repo is None or c[0] == repo) and c[2] != "enviado":
            ultimo[(c[0], c[1])] = (m, c[2])
    estado = {"crear": "creada", "abrir": "abierta", "retomar": "abierta", "pausar": "pausada", "cerrar": "cerrada"}
    return [{"repo": r, "tarea": t, "estado": estado.get(e, e), "desde": m.isoformat()}
            for (r, t), (m, e) in sorted(ultimo.items(), key=lambda x: x[1][0]) if e != "cerrar"]


# ── Plan semanal ──────────────────────────────────────────────────────────────────────────────
# El plan de la semana vive en Toggl (fechas de cada tarea), pero se puede replanificar a media
# semana y Toggl solo guarda lo último. Para medir plan contra realidad hace falta el plan tal como
# se hizo el lunes: se guarda aquí cada versión, y se compara contra la primera.


def carpeta_planes():
    return carpeta() / "planes"


def semana_de(d):
    anio, num, _ = d.isocalendar()
    return "%d-W%02d" % (anio, num)


def limites_semana(semana):
    anio, num = semana.split("-W")
    lunes = date.fromisocalendar(int(anio), int(num), 1)
    return lunes, lunes + timedelta(days=6)


def plan_guardar(semana, tareas, hora):
    d = carpeta_planes()
    d.mkdir(parents=True, exist_ok=True)
    ruta = d / ("%s.json" % semana)
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        datos = {"semana": semana, "versiones": []}
    datos["versiones"].append({"guardado": hora.isoformat(), "tareas": tareas})
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(ruta)  # atómico: nunca queda un plan a medias
    return {"semana": semana, "version": len(datos["versiones"]), "tareas": len(tareas)}


def plan_leer(semana, vigente=False):
    try:
        datos = json.loads((carpeta_planes() / ("%s.json" % semana)).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return datos["versiones"][-1 if vigente else 0]


def plan_comparar(semana, hasta, ajustes):
    """Plan original de la semana frente a lo medido. Solo cuenta el tiempo medido en local
    (tareas abiertas con `tarea` y presencia); lo que se registró a mano en Toggl no está aquí."""
    plan = plan_leer(semana)
    lunes, domingo = limites_semana(semana)
    fin = min(hasta, datetime.combine(domingo + timedelta(days=1), datetime.min.time()).astimezone())
    inicio = datetime.combine(lunes, datetime.min.time()).astimezone()
    lineas = leer_lineas(lunes - timedelta(days=120), min(domingo, hasta.date()))
    presentes = cortar(tramos_presentes(minutos_activos(lineas), ajustes["ausencia_min"]), [(inicio, fin)])
    claves = sorted({(c[0], c[1]) for _, t, c in lineas if t == "tarea" and len(c) >= 3})
    medido = {}
    for repo, tarea in claves:
        eventos = eventos_tarea(lineas, repo, tarea)
        trabajados = cortar(abierta_en(eventos, fin), presentes)
        por_dia = {}
        for a, b in trabajados:
            por_dia[a.date().isoformat()] = por_dia.get(a.date().isoformat(), 0) + int((b - a).total_seconds() // 60)
        cierres = [m for m, e, _ in eventos if e == "cerrar" and inicio <= m < fin]
        if por_dia or cierres:
            medido[(repo, tarea)] = {"por_dia": por_dia, "cerrada": max(cierres).date().isoformat() if cierres else None}
    filas, en_plan = [], set()
    for t in (plan or {}).get("tareas", []):
        clave = (t.get("repo"), str(t.get("tarea")))
        en_plan.add(clave)
        m = medido.get(clave, {"por_dia": {}, "cerrada": None})
        filas.append({**t, "real_min": sum(m["por_dia"].values()),
                      "real_en_su_dia_min": m["por_dia"].get(t.get("dia"), 0), "cerrada": m["cerrada"],
                      "cumplida": bool(m["cerrada"] and t.get("dia") and m["cerrada"] <= t["dia"])})
    fuera = [{"repo": r, "tarea": t, "real_min": sum(m["por_dia"].values()), "cerrada": m["cerrada"]}
             for (r, t), m in medido.items() if (r, t) not in en_plan and m["por_dia"]]
    real_plan = sum(f["real_min"] for f in filas)
    real_fuera = sum(f["real_min"] for f in fuera)
    return {
        "semana": semana, "hay_plan": plan is not None,
        "planificado_min": sum(int(f.get("estimado_min") or 0) for f in filas),
        "real_en_plan_min": real_plan, "real_fuera_min": real_fuera,
        "porcentaje_planificado": round(100 * real_plan / (real_plan + real_fuera)) if real_plan + real_fuera else None,
        "cumplidas": sum(1 for f in filas if f["cumplida"]), "planificadas": len(filas),
        "tareas": filas, "fuera_de_plan": fuera,
    }


# ── Entrada ───────────────────────────────────────────────────────────────────────────────────


def fecha(s):
    return date.fromisoformat(s)


def momento(s):
    return datetime.fromisoformat(s).astimezone() if s else ahora()


def main(argv=None):
    p = argparse.ArgumentParser(description="Registro de presencia para el skill tarea.")
    sub = p.add_subparsers(dest="orden", required=True)
    sub.add_parser("registrar")
    sub.add_parser("mensaje")
    m = sub.add_parser("marca")
    m.add_argument("--repo", required=True)
    m.add_argument("--tarea", required=True)
    m.add_argument("--evento", required=True, choices=["crear", "abrir", "pausar", "retomar", "cerrar", "enviado"])
    m.add_argument("--coste")
    m.add_argument("--vence")
    m.add_argument("--hora")
    t = sub.add_parser("tramos")
    t.add_argument("--repo", required=True)
    t.add_argument("--tarea", required=True)
    t.add_argument("--hasta")
    t.add_argument("--completo", action="store_true", help="sin recortar por presencia (trabajo fuera del Mac)")
    s = sub.add_parser("sesion")
    s.add_argument("--hasta")
    st = sub.add_parser("asentar", help="el tiempo de Claude, al registro local por proyecto y mes")
    st.add_argument("--hasta")
    mt = sub.add_parser("mi-tiempo", help="tu tiempo frente al computador, por aplicación, desde el último envío")
    mt.add_argument("--hasta")
    mt.add_argument("--desde", help="ISO; por defecto, el último envío o el inicio del día")
    mt.add_argument("--enviado", action="store_true", help="marca como enviado hasta --hasta")
    vf = sub.add_parser("verificar", help="compara tus registros de Toggl con tu actividad en el Mac")
    vf.add_argument("--entradas", required=True, help="JSON con los registros (lista, o {data: [...]}); `-` lee de stdin")
    ab = sub.add_parser("abiertas")
    ab.add_argument("--repo", help="solo este repo; `sin-repo` para las de un proyecto sin repositorio")
    ab.add_argument("--hasta")
    pl = sub.add_parser("plan")
    pl.add_argument("accion", choices=["guardar", "leer", "comparar"])
    pl.add_argument("--semana", help="AAAA-Www; por defecto, la de hoy")
    pl.add_argument("--vigente", action="store_true", help="leer: la última versión, no la original")
    pl.add_argument("--hasta")
    for nombre in ("resumen", "claude"):
        r = sub.add_parser(nombre)
        r.add_argument("--desde", required=True, type=fecha)
        r.add_argument("--hasta", required=True, type=fecha)
    a = p.parse_args(argv)
    ajustes = leer_ajustes()

    if a.orden == "registrar":
        try:
            inactivo = segundos_inactivo()
            if inactivo is not None:
                t = ahora()
                anotar(t, "mac", inactivo, app_al_frente() if inactivo < 60 else "-")
                avisar_desde_el_mac(t, inactivo, ajustes)
        except Exception:  # noqa: BLE001 — desde launchd no hay a quién avisar
            pass
        try:
            # Una vez al día, el tiempo de Claude al registro local: aunque no se cierre ninguna
            # tarea en 30 días, nada se pierde cuando Claude Code borra sus sesiones.
            sello = carpeta() / "ultimo-asiento"
            if not sello.exists() or datetime.now().timestamp() - sello.stat().st_mtime > 86400:
                asentar(ahora(), ajustes)
                sello.touch()
        except Exception:  # noqa: BLE001
            pass
        return 0

    if a.orden == "mensaje":
        try:
            entrada = json.loads(sys.stdin.read() or "{}")
            t = ahora()
            anotar(t, "mensaje", proyecto_de(entrada.get("cwd")), entrada.get("session_id") or "")
            aviso = aviso_pausa(t, ajustes)
            if aviso:
                h = fmt_duracion(aviso["minutos"] * 60)
                print("Aviso de pausa (registro de presencia): el usuario lleva %s de trabajo continuo, "
                      "sin una pausa de %d min. Díselo en una línea al inicio de tu respuesta, "
                      "por ejemplo: «Llevas %s seguidas; toca una pausa». No insistas más."
                      % (h, ajustes["pausa_min"], h))
        except Exception:  # noqa: BLE001 — el gancho nunca puede romper la conversación
            pass
        return 0

    if a.orden == "marca":
        extra = []
        if a.coste:
            extra.append("coste=%s" % a.coste)
        if a.vence:
            extra.append("vence=%s" % a.vence)
        t = momento(a.hora)
        anotar(t, "tarea", a.repo, a.tarea, a.evento, *extra)
        print(json.dumps({"ok": True, "hora": t.isoformat()}))
        return 0

    if a.orden == "tramos":
        print(json.dumps(calcular_tramos(a.repo, a.tarea, momento(a.hasta), ajustes, a.completo), ensure_ascii=False))
        return 0

    if a.orden == "sesion":
        print(json.dumps(sesion_actual(momento(a.hasta), ajustes), ensure_ascii=False))
        return 0

    if a.orden == "resumen":
        print(json.dumps(resumen(a.desde, a.hasta, ajustes), ensure_ascii=False))
        return 0

    if a.orden == "asentar":
        resultado = asentar(momento(a.hasta), ajustes)
        (carpeta() / "ultimo-asiento").touch()
        print(json.dumps(resultado, ensure_ascii=False))
        return 0

    if a.orden == "mi-tiempo":
        t = momento(a.hasta)
        if a.enviado:
            anotar(t, "mi-tiempo", "enviado", t.isoformat())
            print(json.dumps({"ok": True, "hasta": t.isoformat()}))
        else:
            print(json.dumps(mi_tiempo(t, ajustes, desde=momento(a.desde) if a.desde else None), ensure_ascii=False))
        return 0

    if a.orden == "verificar":
        texto = sys.stdin.read() if a.entradas == "-" else Path(a.entradas).read_text(encoding="utf-8")
        datos = json.loads(texto)
        if isinstance(datos, dict):
            datos = datos.get("data") or datos.get("time_entries") or []
        print(json.dumps(verificar(datos, ajustes), ensure_ascii=False))
        return 0

    if a.orden == "abiertas":
        print(json.dumps(tareas_abiertas(momento(a.hasta), a.repo), ensure_ascii=False))
        return 0

    if a.orden == "plan":
        t = momento(a.hasta)
        semana = a.semana or semana_de(t.date())
        if a.accion == "guardar":
            print(json.dumps(plan_guardar(semana, json.loads(sys.stdin.read() or "[]"), t), ensure_ascii=False))
        elif a.accion == "leer":
            print(json.dumps(plan_leer(semana, a.vigente), ensure_ascii=False))
        else:
            print(json.dumps(plan_comparar(semana, t, ajustes), ensure_ascii=False))
        return 0

    if a.orden == "claude":
        print(json.dumps(claude_solo(a.desde, a.hasta, ajustes), ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
