#!/usr/bin/env python3
"""
Guardia de git del plugin utils. La ejecuta Claude Code, no Claude: no depende de ninguna
instrucción y vale en cualquier modo de permisos, también en el automático. Solo stdlib.

- `PreToolUse` (Bash, Write, Edit…): en **todo repo git**, bloquea
  - los commits sobre una rama protegida (`main`, `master`, la rama por defecto del remoto y la rama
    destino de `tareas/config.md`, o de `toggl.md` en un repo sin migrar), salvo el primer commit
    de un repo vacío y los que solo tocan la bandeja, los pendientes o el historial;
  - el merge y el push hacia una rama protegida, y `gh pr merge`, salvo con un permiso vigente;
  - forzar, borrar o reescribir una rama protegida;
  - escribir en el archivo de permisos o en la copia instalada de los plugins.
- `UserPromptSubmit`: si el usuario escribe «apruebo el merge», crea el permiso: **solo para esa
  sesión**, vence a los 10 minutos y da **un merge y un push**, en el primer repo donde se usen.
  Claude no puede crearlo: solo nace de un mensaje del usuario.

**Falla cerrado**: si algo falla al analizar un comando de git, lo bloquea.

Uso (desde `hooks.json`):
    guardia_git.py pre       # PreToolUse: sale con 2 y el motivo en stderr para bloquear
    guardia_git.py mensaje   # UserPromptSubmit: registra la aprobación; nunca bloquea
"""

import json
import os
import re
import shlex
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

VIGENCIA = 600  # segundos
PERMITIDOS = re.compile(r"^tareas/(por-revisar\.md|pendientes\.md|historial/[^/]+\.md)$")
OPERADORES = {";", "&&", "||", "|", "&", "(", ")", ";;", "|&"}
ESCRITURA = re.compile(r"(\brm\b|\bmv\b|\bcp\b|sed\s+-i|\btee\b|\btouch\b|\bchmod\b|\bln\b|\btruncate\b|\bunlink\b)")
AVISO = ("El merge y el push a una rama protegida los desbloquea solo el usuario, escribiendo "
         "«apruebo el merge» después de ver el resultado: muéstraselo y pídeselo. Para trabajar, usa "
         "una rama (git switch -c <rama>). No intentes rodear este bloqueo: ni con otro comando, ni "
         "con un script, ni editando la guardia o sus permisos.")


class Bloqueo(Exception):
    pass


def dir_aprobaciones():
    return Path(os.environ.get("GUARDIA_APROBACIONES", "~/.claude/utils/aprobaciones")).expanduser()


def dir_plugins():
    return Path(os.environ.get("GUARDIA_PLUGINS", "~/.claude/plugins")).expanduser()


# ── git ───────────────────────────────────────────────────────────────────────────────────────

def git(cwd, *args):
    try:
        r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("git no respondió: %s" % " ".join(args)) from e
    return r.stdout.strip() if r.returncode == 0 else None


def raiz(cwd):
    if not Path(cwd).is_dir():
        return None
    r = git(cwd, "rev-parse", "--show-toplevel")
    return Path(r) if r else None


def rama_actual(repo):
    return git(repo, "symbolic-ref", "--quiet", "--short", "HEAD")


def rama_destino(repo):
    for nombre in ("config.md", "toggl.md"):
        f = repo / "tareas" / nombre
        if f.exists():
            m = re.search(r"^## Rama destino\s*\n+\s*`([^`]+)`", f.read_text(encoding="utf-8"), re.M)
            if m:
                return m.group(1).strip()
            break
    return None


def protegidas(repo):
    p = {"main", "master"}
    destino = rama_destino(repo)
    if destino:
        p.add(destino)
    defecto = git(repo, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    if defecto:
        p.add(defecto.split("/", 1)[-1])
    return p


def solo_permitidos(archivos):
    archivos = [a for a in archivos if a]
    return bool(archivos) and all(PERMITIDOS.match(a) for a in archivos)


# ── el permiso ────────────────────────────────────────────────────────────────────────────────

def archivo_permiso(sesion):
    seguro = re.sub(r"[^A-Za-z0-9_.-]", "_", sesion or "sin-sesion")
    return dir_aprobaciones() / ("%s.json" % seguro)


def normalizar(texto):
    t = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t)


def es_aprobacion(prompt):
    t = normalizar(prompt)
    return bool(re.search(r"(?<!no )\bapruebo el merge\b", t))


def registrar_aprobacion(sesion, ahora=None):
    ahora = ahora or time.time()
    f = archivo_permiso(sesion)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"sesion": sesion, "creada": ahora, "vence": ahora + VIGENCIA, "repo": None,
                             "merge": False, "push": False}), encoding="utf-8")
    return f


def usar_permiso(sesion, repo, accion, ahora=None, consumir=True):
    """True si hay un permiso vigente de esta sesión para `accion` ('merge' o 'push') en `repo`."""
    ahora = ahora or time.time()
    f = archivo_permiso(sesion)
    if not f.exists():
        return False
    d = json.loads(f.read_text(encoding="utf-8"))
    if d.get("sesion") != sesion or ahora > d.get("vence", 0):
        return False
    if d.get("repo") not in (None, str(repo)):
        return False
    if accion == "cerrar-merge":  # el commit que concluye un merge ya autorizado
        return bool(d.get("merge")) and d.get("repo") == str(repo)
    if d.get(accion):
        return False
    if consumir:
        d[accion] = True
        d["repo"] = str(repo)
        f.write_text(json.dumps(d), encoding="utf-8")
    return True


# ── análisis del comando ──────────────────────────────────────────────────────────────────────

def saltos_a_punto_y_coma(cmd):
    """Los saltos de línea fuera de comillas separan comandos: se vuelven `;`."""
    salida, comilla, escape = [], None, False
    for ch in cmd:
        if escape:
            salida.append(ch)
            escape = False
            continue
        if ch == "\\" and comilla != "'":
            escape = True
            salida.append(ch)
            continue
        if comilla:
            if ch == comilla:
                comilla = None
        elif ch in "'\"":
            comilla = ch
        elif ch == "\n":
            salida.append(" ; ")
            continue
        salida.append(ch)
    return "".join(salida)


def segmentos(cmd):
    lex = shlex.shlex(saltos_a_punto_y_coma(cmd), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    actual, salida = [], []
    for tok in lex:
        if tok in OPERADORES:
            if actual:
                salida.append(actual)
            actual = []
        else:
            actual.append(tok)
    if actual:
        salida.append(actual)
    return salida


def args_no_opcion(args, con_valor=()):
    salida, saltar = [], False
    for i, a in enumerate(args):
        if saltar:
            saltar = False
            continue
        if a == "--":
            salida.extend(args[i + 1:])
            break
        if a.startswith("-"):
            if a in con_valor:
                saltar = True
            continue
        salida.append(a)
    return salida


def bloquear(motivo):
    raise Bloqueo(motivo)


def revisar_commit(repo, rama, args, sesion, ahora):
    if git(repo, "rev-parse", "--verify", "--quiet", "HEAD") is None:
        return  # primer commit de un repo vacío
    if git(repo, "rev-parse", "--verify", "--quiet", "MERGE_HEAD") and \
            usar_permiso(sesion, repo, "cerrar-merge", ahora):
        return
    archivos = (git(repo, "diff", "--cached", "--name-only") or "").splitlines()
    cortas = [a for a in args if re.match(r"^-[A-Za-z]+$", a)]
    if "--all" in args or any("a" in c for c in cortas):
        archivos += (git(repo, "diff", "--name-only") or "").splitlines()
    rutas = args_no_opcion(args, {"-m", "--message", "-F", "--file", "-C", "-c", "--author", "--date",
                                  "--fixup", "--squash", "-t", "--template", "--trailer"})
    if rutas:
        prefijo = git(repo, "rev-parse", "--show-prefix") or ""
        archivos += [os.path.normpath(prefijo + r) for r in rutas]
    if solo_permitidos(archivos):
        return
    bloquear("commit sobre la rama protegida `%s`" % rama)


def destinos_push(repo, rama, args):
    if "--all" in args or "--mirror" in args or "--branches" in args:
        return list(protegidas(repo)), True
    resto = args_no_opcion(args, {"-o", "--push-option", "--repo", "--receive-pack", "--exec"})
    refspecs = resto[1:]
    if not refspecs:
        if "--tags" in args:
            return [], False
        return ([rama] if rama else []), False
    salida = []
    for r in refspecs:
        r = r.lstrip("+")
        if r.startswith("refs/tags/"):
            continue
        origen, _, destino = r.partition(":")
        destino = destino or origen
        if destino == "HEAD":
            destino = rama or "HEAD"
        destino = re.sub(r"^refs/heads/", "", destino)
        salida.append((origen or "", destino))
    return salida, False


def revisar_push(repo, rama, args, sesion, ahora):
    destinos, masivo = destinos_push(repo, rama, args)
    prot = protegidas(repo)
    if masivo:
        if usar_permiso(sesion, repo, "push", ahora):
            return
        bloquear("push de todas las ramas (incluye las protegidas)")
    pares = [(rama or "HEAD", d) if isinstance(d, str) else d for d in destinos]
    for origen, destino in pares:
        if destino not in prot:
            continue
        if "--delete" in args or "-d" in args or origen == "":
            bloquear("borrar la rama protegida `%s` del remoto" % destino)
        origen = origen if origen not in ("", "HEAD") else (rama or "HEAD")
        remoto = "refs/remotes/origin/%s" % destino
        if git(repo, "rev-parse", "--verify", "--quiet", remoto):
            nuevos = git(repo, "rev-list", "%s..%s" % (remoto, origen))
            if nuevos == "":
                continue  # nada que subir
            archivos = (git(repo, "log", "--format=", "--name-only", "%s..%s" % (remoto, origen)) or "").splitlines()
            fusiones = git(repo, "rev-list", "--merges", "%s..%s" % (remoto, origen))
            if not fusiones and solo_permitidos(archivos):
                continue  # solo la bandeja, los pendientes o el historial
        if usar_permiso(sesion, repo, "push", ahora):
            return
        bloquear("push a la rama protegida `%s`" % destino)


def revisar_git(tokens, cwd, sesion, ahora):
    i = 1
    while i < len(tokens) and tokens[i].startswith("-"):
        t = tokens[i]
        if t == "-C" and i + 1 < len(tokens):
            cwd = os.path.join(cwd, os.path.expanduser(tokens[i + 1]))
            i += 2
            continue
        if t in ("-c", "--git-dir", "--work-tree", "--namespace") and i + 1 < len(tokens):
            i += 2
            continue
        if t.startswith("--work-tree=") or t.startswith("--git-dir="):
            i += 1
            continue
        i += 1
    if i >= len(tokens):
        return
    sub, args = tokens[i], tokens[i + 1:]
    repo = raiz(cwd)
    if repo is None:
        return  # fuera de un repo: init, clone, o un error del propio git
    rama = rama_actual(repo)
    prot = protegidas(repo)
    en_protegida = rama in prot

    if sub == "commit" and en_protegida:
        revisar_commit(repo, rama, args, sesion, ahora)
    elif sub in ("cherry-pick", "revert", "am", "rebase") and en_protegida:
        if any(a in args for a in ("--abort", "--quit", "--skip")):
            return
        bloquear("`git %s` sobre la rama protegida `%s`" % (sub, rama))
    elif sub == "merge" and en_protegida:
        if any(a in args for a in ("--abort", "--quit")):
            return
        if args_no_opcion(args, {"-m", "-F", "--file", "-s", "--strategy", "-X"}) == ["origin/%s" % rama]:
            return  # ponerse al día con el remoto de la misma rama
        if not usar_permiso(sesion, repo, "merge", ahora):
            bloquear("merge hacia la rama protegida `%s`" % rama)
    elif sub == "pull" and en_protegida:
        resto = args_no_opcion(args)
        if len(resto) > 1 and any(r.split(":")[0] != rama for r in resto[1:]):
            if not usar_permiso(sesion, repo, "merge", ahora):
                bloquear("pull de otra rama hacia la rama protegida `%s`" % rama)
    elif sub == "push":
        revisar_push(repo, rama, args, sesion, ahora)
    elif sub == "branch":
        if any(a in args for a in ("-f", "--force", "-D", "-d", "--delete", "-M", "-m", "--move", "-C", "-c")):
            tocadas = [a for a in args_no_opcion(args) if a in prot]
            if tocadas:
                bloquear("forzar, mover o borrar la rama protegida `%s`" % tocadas[0])
    elif sub in ("switch", "checkout"):
        for flag in ("-B", "-C", "--force-create"):
            if flag in args:
                k = args.index(flag)
                if k + 1 < len(args) and args[k + 1] in prot:
                    bloquear("reescribir la rama protegida `%s`" % args[k + 1])
    elif sub == "update-ref":
        for a in args_no_opcion(args):
            if re.sub(r"^refs/heads/", "", a) in prot and a.startswith("refs/heads/"):
                bloquear("reescribir la rama protegida `%s`" % a)


def toca_zona_protegida(texto):
    t = os.path.expanduser(texto)
    return str(dir_aprobaciones()) in t or "utils/aprobaciones" in t or \
        str(dir_plugins()) in t or ".claude/plugins/" in t


SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
SUSTITUCION = re.compile(r"\$\(([^()]*)\)|`([^`]*)`")


def interior_de_shell(tokens):
    """El texto de `bash -c '…'` (o `-lc`, `-ec`…), o None si el shell no lleva `-c`."""
    for k, t in enumerate(tokens[1:], start=1):
        if re.match(r"^-[A-Za-z]*c[A-Za-z]*$", t):
            return tokens[k + 1] if k + 1 < len(tokens) else ""
        if not t.startswith("-"):
            return None
    return None


def revisar_bash(cmd, cwd, sesion, ahora=None, profundidad=0):
    """Levanta Bloqueo con el motivo si el comando no debe correr. Mira también dentro de
    `bash -c '…'`, `eval …`, `$(…)` y las comillas invertidas."""
    ahora = ahora or time.time()
    if profundidad > 5:
        bloquear("comando anidado demasiadas veces para revisarlo")
    destinos = re.findall(r">>?\s*['\"]?([^\s'\";&|]+)", cmd)
    if (toca_zona_protegida(cmd) and ESCRITURA.search(cmd)) or any(toca_zona_protegida(d) for d in destinos):
        bloquear("escribir en los permisos de la guardia o en la copia instalada de los plugins")
    if not re.search(r"(^|[^\w-])(git|gh)(\s|$)", cmd):
        return
    for m in SUSTITUCION.finditer(cmd):
        revisar_bash(m.group(1) or m.group(2) or "", cwd, sesion, ahora, profundidad + 1)
    for tokens in segmentos(cmd):
        while tokens and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]):
            tokens = tokens[1:]
        if tokens and tokens[0] in ("env", "command", "nohup", "time", "sudo"):
            tokens = tokens[1:]
        if not tokens:
            continue
        if tokens[0] == "cd":
            destino = os.path.expanduser(tokens[1]) if len(tokens) > 1 else str(Path.home())
            cwd = os.path.join(cwd, destino)
            continue
        nombre = os.path.basename(tokens[0])
        if nombre in SHELLS:
            interior = interior_de_shell(tokens)
            if interior is not None:
                revisar_bash(interior, cwd, sesion, ahora, profundidad + 1)
            continue
        if nombre == "eval":
            revisar_bash(" ".join(tokens[1:]), cwd, sesion, ahora, profundidad + 1)
            continue
        if nombre == "git":
            revisar_git(tokens, cwd, sesion, ahora)
        elif os.path.basename(tokens[0]) == "gh" and tokens[1:3] == ["pr", "merge"]:
            repo = raiz(cwd) or Path(cwd)
            if not usar_permiso(sesion, repo, "merge", ahora):
                bloquear("`gh pr merge`")


def revisar_edicion(ruta):
    if ruta and toca_zona_protegida(str(Path(os.path.expanduser(ruta)).resolve())):
        bloquear("editar los permisos de la guardia o la copia instalada de los plugins")


# ── entrada ───────────────────────────────────────────────────────────────────────────────────

def pre(entrada):
    if os.environ.get("GUARDIA_FORZAR_ERROR"):
        raise RuntimeError("error forzado para probar que la guardia falla cerrada")
    herramienta = entrada.get("tool_name", "")
    datos = entrada.get("tool_input") or {}
    sesion = entrada.get("session_id") or ""
    cwd = entrada.get("cwd") or os.getcwd()
    if herramienta == "Bash":
        revisar_bash(datos.get("command", ""), cwd, sesion)
    elif herramienta in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        revisar_edicion(datos.get("file_path") or datos.get("notebook_path"))


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    orden = argv[0] if argv else "pre"
    crudo = sys.stdin.read()
    if orden == "mensaje":
        try:
            entrada = json.loads(crudo or "{}")
            if es_aprobacion(entrada.get("prompt", "")):
                registrar_aprobacion(entrada.get("session_id") or "")
                print(json.dumps({"hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": "Guardia de git: aprobación registrada para esta sesión "
                                         "(un merge y un push a una rama protegida, durante 10 minutos)."}},
                    ensure_ascii=False))
        except Exception:  # noqa: BLE001 — un mensaje del usuario nunca se bloquea
            pass
        return 0
    try:
        pre(json.loads(crudo or "{}"))
        return 0
    except Bloqueo as b:
        print("Guardia de git: bloqueado — %s. %s" % (b, AVISO), file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001 — falla cerrado
        print("Guardia de git: no pude analizar el comando (%s), así que lo bloqueo. Si es un comando "
              "de git legítimo, divídelo en pasos simples. %s" % (e, AVISO), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
