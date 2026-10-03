#!/usr/bin/env python3
"""
Lo abierto de un repo: captura las ramas sin mergear en `tareas/pendientes.md` y lo lista para
`balance`. Solo stdlib.

- `capturar`: por cada rama local sin mergear a la rama destino que aún no figure en
  `pendientes.md`, añade una entrada en `## A medias` con los pasos que faltan de su plan y si hay
  cambios sin commitear. **Idempotente; no commitea nada; no depende de Claude.** Lo lanzan el
  gancho `SessionEnd` del plugin (`--gancho`, lee el `cwd` de la entrada) y, una vez al día, el
  agente de launchd de `presencia.py` (todos los repos de la agenda).
- `listar`: JSON con las tres secciones de `pendientes.md` (con su antigüedad), la bandeja y las
  ramas sin mergear, por repo.

Uso:
    pendientes.py capturar [--repo RUTA | --gancho | --todos] [--hoy AAAA-MM-DD]
    pendientes.py listar [--repo RUTA ... | --todos] [--hoy AAAA-MM-DD]

Solo actúa en repos con `tareas/config.md` (o el `toggl.md` de utils 5): nunca crea `tareas/` por su
cuenta ni escribe en un repo con el formato antiguo, que primero se migra.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ESQUELETO = Path(__file__).resolve().parent.parent / "assets" / "pendientes.esqueleto.md"
AGENDA = Path(os.environ.get("AGENDA_CONFIG", "~/Github/AI-kit/config/context/agenda.md")).expanduser()
SECCIONES = ("Por hacer", "A medias", "Espera tu decisión")
FECHA = re.compile(r" · (\d{4}-\d{2}-\d{2})(?: — |$)")


def git(raiz, *args):
    try:
        r = subprocess.run(["git", "-C", str(raiz), *args], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def raiz_de(ruta):
    r = git(ruta, "rev-parse", "--show-toplevel")
    return Path(r) if r else None


def texto_config(raiz):
    for nombre in ("config.md", "toggl.md"):
        f = Path(raiz) / "tareas" / nombre
        if f.exists():
            return f.read_text(encoding="utf-8")
    return ""


def rama_destino(raiz):
    """La de `config.md` § Rama destino (o `toggl.md` en utils 5); `main` si no la declara."""
    m = re.search(r"^## Rama destino\s*\n+\s*`([^`]+)`", texto_config(raiz), re.M)
    return m.group(1).strip() if m else "main"


def protegidas(raiz):
    p = {"main", "master", rama_destino(raiz)}
    defecto = git(raiz, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    if defecto:
        p.add(defecto.split("/", 1)[-1])
    return p


def base_de(raiz):
    """La rama contra la que se mide «sin mergear»: la destino si existe, si no main o master."""
    for b in (rama_destino(raiz), "main", "master"):
        if git(raiz, "rev-parse", "--verify", "--quiet", "refs/heads/" + b):
            return b
    return None


def ramas_sin_mergear(raiz):
    base = base_de(raiz)
    if not base:
        return []
    actual = git(raiz, "branch", "--show-current") or ""
    sucia = bool(git(raiz, "status", "--porcelain"))
    salida = []
    for b in (git(raiz, "for-each-ref", "--format=%(refname:short)", "refs/heads") or "").splitlines():
        b = b.strip()
        if not b or b in protegidas(raiz):
            continue
        mergeada = subprocess.run(["git", "-C", str(raiz), "merge-base", "--is-ancestor", b, base],
                                  capture_output=True).returncode == 0
        cambios = b == actual and sucia
        if mergeada and not cambios:
            continue
        salida.append({"rama": b, "fecha": git(raiz, "log", "-1", "--format=%cs", b) or "",
                       "cambios_sin_commitear": cambios})
    return salida


def dir_planes():
    """La carpeta donde Claude Code guarda los planes del modo plan."""
    return Path(os.environ.get("PLANES_CLAUDE", "~/.claude/plans")).expanduser()


def marcador_de(texto, repo, rama):
    primera = (texto or "").split("\n", 1)[0]
    return bool(re.search(r"<!--[^>]*\brepo\s+%s\b" % re.escape(repo), primera)) and \
        bool(re.search(r"<!--[^>]*\brama\s+%s\b" % re.escape(rama), primera))


def leer_plan(raiz, rama):
    """(ruta, texto) del plan de la rama: el del modo plan, en `~/.claude/plans/`, cuyo marcador nombra
    este repo y esta rama (el más reciente si hay varios). Antes de utils 6.1 el plan vivía en
    `tareas/planes/` del repo: si no hay otro, se busca ahí."""
    carpeta = dir_planes()
    if carpeta.is_dir():
        candidatos = sorted(carpeta.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        for f in candidatos[:200]:
            try:
                with f.open(encoding="utf-8") as h:
                    primera = h.readline()
            except OSError:
                continue
            if marcador_de(primera, Path(raiz).name, rama):
                defecto = Path("~/.claude/plans").expanduser()
                ruta = "~/.claude/plans/%s" % f.name if carpeta == defecto else str(f)
                return ruta, f.read_text(encoding="utf-8")
    return leer_plan_en_repo(raiz, rama)


def leer_plan_en_repo(raiz, rama):
    actual = git(raiz, "branch", "--show-current")
    def leer(nombre):
        if rama == actual:
            f = Path(raiz) / "tareas" / "planes" / nombre
            return f.read_text(encoding="utf-8") if f.exists() else None
        return git(raiz, "show", "%s:tareas/planes/%s" % (rama, nombre))
    texto = leer(rama + ".md")
    if texto:
        return "tareas/planes/%s.md" % rama, texto
    nombres = git(raiz, "ls-tree", "--name-only", rama, "tareas/planes/") or ""
    for ruta in nombres.splitlines():
        nombre = ruta.rsplit("/", 1)[-1]
        t = leer(nombre)
        if t and re.search(r"<!--[^>]*\brama\s+%s\b" % re.escape(rama), t):
            return "tareas/planes/%s" % nombre, t
    return None, None


def resumen_plan(texto):
    titulo = next((l[2:].strip() for l in texto.splitlines() if l.startswith("# ")), None)
    m = re.search(r"<!--[^>]*·\s*área\s+([^·>]+?)\s*(?:·|-->)", texto)
    area = m.group(1).strip() if m else None
    total = hechos = 0
    if "## Pasos" in texto:
        bloque = texto.split("## Pasos", 1)[1].split("\n## ", 1)[0]
        for linea in bloque.splitlines():
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if len(celdas) >= 2 and celdas[0].isdigit():
                total += 1
                hechos += bool(celdas[-1]) and not celdas[-1].startswith("{{")
    return titulo, area, total, hechos


def entrada(raiz, r, hoy):
    archivo, texto = leer_plan(raiz, r["rama"])
    titulo, area, total, hechos = resumen_plan(texto) if texto else (None, None, 0, 0)
    if total and hechos == total:
        falta = "los %d pasos hechos; falta el cierre (merge)" % total
    elif total:
        falta = "faltan %d de %d pasos" % (total - hechos, total)
    else:
        falta = "plan sin pasos marcados" if archivo else "sin plan"
    if r["cambios_sin_commitear"]:
        falta += "; cambios sin commitear"
    return "- **%s** · %s · rama `%s` · plan %s · %s — %s · sesión cerrada sin cierre" % (
        titulo or r["rama"], area or "—", r["rama"], "`%s`" % archivo if archivo else "—",
        r["fecha"] or hoy, falta)


def insertar(texto, seccion, lineas):
    cabecera = "## %s\n" % seccion
    if cabecera not in texto:
        texto = texto.rstrip() + "\n\n" + cabecera
    antes, despues = texto.split(cabecera, 1)
    cuerpo, sep, resto = despues.partition("\n## ")
    cuerpo = cuerpo.rstrip("\n")
    cuerpo = (cuerpo + "\n" if cuerpo.strip() else "\n") + "\n".join(lineas) + "\n"
    return antes + cabecera + cuerpo + ("\n## " + resto if sep else "")


def al_dia(raiz):
    """utils 5 o 6: tiene `config.md` o `toggl.md`. Un repo con el formato antiguo no se toca."""
    return bool(raiz) and any((raiz / "tareas" / n).exists() for n in ("config.md", "toggl.md"))


def capturar(ruta, hoy=None):
    """Añade a `## A medias` las ramas sin mergear que no figuran en `pendientes.md`. Devuelve sus nombres."""
    hoy = hoy or date.today().isoformat()
    raiz = raiz_de(ruta)
    if not al_dia(raiz):
        return []
    archivo = raiz / "tareas" / "pendientes.md"
    texto = archivo.read_text(encoding="utf-8") if archivo.exists() else ESQUELETO.read_text(encoding="utf-8")
    nuevas = [r for r in ramas_sin_mergear(raiz) if "rama `%s`" % r["rama"] not in texto]
    if not nuevas:
        return []
    archivo.write_text(insertar(texto, "A medias", [entrada(raiz, r, hoy) for r in nuevas]), encoding="utf-8")
    return [r["rama"] for r in nuevas]


def repos_de_la_agenda():
    try:
        texto = AGENDA.read_text(encoding="utf-8")
    except OSError:
        return []
    bloque = texto.split("## Repos", 1)[1].split("\n## ", 1)[0] if "## Repos" in texto else ""
    salida = []
    for linea in bloque.splitlines():
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) >= 2 and celdas[1].startswith(("~", "/")):
            salida.append(Path(celdas[1]).expanduser())
    return salida


def capturar_todos(hoy=None):
    return {str(r): capturar(r, hoy) for r in repos_de_la_agenda() if al_dia(r)}


def dias(fecha, hoy):
    try:
        return (date.fromisoformat(hoy) - date.fromisoformat(fecha)).days
    except ValueError:
        return None


def entradas(texto, seccion, hoy):
    cabecera = "## %s\n" % seccion
    if cabecera not in texto:
        return []
    bloque = texto.split(cabecera, 1)[1].split("\n## ", 1)[0]
    salida = []
    for linea in bloque.splitlines():
        if linea.startswith("- "):
            m = FECHA.search(linea)
            f = m.group(1) if m else None
            salida.append({"texto": linea[2:], "fecha": f, "dias": dias(f, hoy) if f else None})
    return sorted(salida, key=lambda e: -(e["dias"] or 0))


def listar(ruta, hoy=None):
    hoy = hoy or date.today().isoformat()
    raiz = raiz_de(ruta)
    if not raiz or not (raiz / "tareas").is_dir():
        return None
    def leer(nombre):
        f = raiz / "tareas" / nombre
        return f.read_text(encoding="utf-8") if f.exists() else ""
    pend = leer("pendientes.md")
    bandeja = [l for l in leer("por-revisar.md").splitlines() if l.startswith("- **")]
    fechas = sorted(m.group(1) for m in (FECHA.search(l) for l in bandeja) if m)
    return {
        "repo": raiz.name,
        "pendientes": {s: entradas(pend, s, hoy) for s in SECCIONES},
        "bandeja": {"entradas": len(bandeja), "mas_antigua": fechas[0] if fechas else None},
        "ramas_sin_mergear": ramas_sin_mergear(raiz),
        "sin_migrar": not (raiz / "tareas" / "config.md").exists(),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Lo abierto de un repo: captura y lista.")
    sub = p.add_subparsers(dest="orden", required=True)
    c = sub.add_parser("capturar")
    c.add_argument("--repo")
    c.add_argument("--gancho", action="store_true", help="lee el cwd de la entrada del gancho; nunca falla")
    c.add_argument("--todos", action="store_true", help="todos los repos de la agenda")
    c.add_argument("--hoy")
    l = sub.add_parser("listar")
    l.add_argument("--repo", action="append")
    l.add_argument("--todos", action="store_true")
    l.add_argument("--hoy")
    a = p.parse_args(argv)

    if a.orden == "capturar":
        try:
            if a.todos:
                r = capturar_todos(a.hoy)
            else:
                ruta = a.repo
                if a.gancho:
                    ruta = (json.loads(sys.stdin.read() or "{}").get("cwd")) or os.getcwd()
                r = {str(ruta or os.getcwd()): capturar(ruta or os.getcwd(), a.hoy)}
            print(json.dumps({"ok": True, "capturadas": r}, ensure_ascii=False))
        except Exception as e:  # noqa: BLE001 — al cerrar la sesión no hay a quién avisar
            if not a.gancho:
                raise
            print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 0

    rutas = repos_de_la_agenda() if a.todos else (a.repo or [os.getcwd()])
    salida = [x for x in (listar(r, a.hoy) for r in rutas) if x]
    print(json.dumps(salida, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
