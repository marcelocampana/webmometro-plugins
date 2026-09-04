#!/usr/bin/env python3
"""
Sella y verifica la versión de una pieza que revisó el equipo médico.

`estado: aprobado` dice que la redacción está cerrada, pero no dice QUÉ VERSIÓN revisó nadie.
Si la fuente se corrige después de la validación, una verificación de sincronía diría "todo en
orden" contra una fuente que ya no es la validada. Este script cierra ese hueco: congela una
copia del contenido revisado, guarda su huella, y luego permite comprobar si la fuente sigue
siendo esa.

Escribir es lo único que hace, y solo con --validado-por. Sin flags, muestra.

Uso:
    python3 sellar_validacion.py <fuente.md> --mostrar
    python3 sellar_validacion.py <fuente.md> --verificar
    python3 sellar_validacion.py <fuente.md> --validado-por "Dra. X, Observatorio del Cáncer"

Códigos de salida: 0 todo en orden · 1 la fuente cambió tras validarse · 2 error.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_contenido import cargar, hash_contenido  # noqa: E402

DIR_VALIDADO = ".validado"

LEEME = """# Copias congeladas de validación

Cada archivo de esta carpeta es la versión exacta de una pieza que revisó el equipo médico,
guardada tal cual quedó ese día. Sirve para responder una sola pregunta: ¿lo que se va a
publicar es idéntico a lo que se validó?

**No se editan a mano.** Las escribe `sellar_validacion.py`, del skill content-sync-check.
Editar una copia congelada destruye la única evidencia de qué se revisó.

El nombre lleva la fecha porque una pieza puede revalidarse: la más reciente es la vigente y
las anteriores quedan como registro.
"""


def _hoy():
    return subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True,
                          check=True).stdout.strip()


def _leer_fm(ruta):
    """Frontmatter crudo de la pieza, incluida la metadata de proceso."""
    doc = cargar(ruta)
    return doc, doc.get("frontmatter_crudo") or {}


def _escribir_campos(ruta, campos):
    """Inserta o actualiza claves escalares en el frontmatter, conservando todo lo demás.

    Se hace por líneas y no reserializando el YAML: reescribir el archivo entero desde el
    árbol parseado perdería comentarios, orden y estilo de comillas — y en una pieza que
    alguien acaba de validar, cualquier cambio no pedido es inaceptable.
    """
    texto = Path(ruta).read_text(encoding="utf-8")
    if not texto.startswith("---"):
        raise ValueError("la pieza no tiene frontmatter: {}".format(ruta))
    cierre = texto.index("\n---", 3)
    cabeza, cuerpo = texto[4:cierre], texto[cierre:]
    lineas = cabeza.split("\n")

    for clave, valor in campos.items():
        linea = '{}: "{}"'.format(clave, valor) if isinstance(valor, str) and (
            ":" in valor or valor.startswith(("'", '"'))) else "{}: {}".format(clave, valor)
        patron = re.compile(r"^{}\s*:".format(re.escape(clave)))
        for i, l in enumerate(lineas):
            if patron.match(l):
                lineas[i] = linea
                break
        else:
            lineas.insert(0, linea)

    Path(ruta).write_text("---\n" + "\n".join(lineas) + cuerpo, encoding="utf-8")


def mostrar(ruta):
    _, fm = _leer_fm(ruta)
    return {
        "pieza": str(ruta),
        "estado": fm.get("estado"),
        "validada": bool(fm.get("hash_validado")),
        "validado_por": fm.get("validado_por"),
        "fecha_validacion": fm.get("fecha_validacion"),
        "hash_validado": fm.get("hash_validado"),
        "copia_validada": fm.get("copia_validada"),
    }


def verificar(ruta):
    """¿La fuente sigue siendo la que se validó?"""
    ruta = Path(ruta)
    doc, fm = _leer_fm(ruta)
    hash_actual = hash_contenido(doc["bloques"])
    hash_sellado = fm.get("hash_validado")

    r = {"pieza": str(ruta), "hash_actual": hash_actual, "hash_validado": hash_sellado,
         "estado": fm.get("estado")}

    if not hash_sellado:
        r["veredicto"] = "sin_validar"
        r["mensaje"] = ("la pieza no tiene ancla de validación. No se puede afirmar que "
                        "coincida con nada revisado.")
        return r, 0

    rel = fm.get("copia_validada")
    copia = (ruta.parent / rel) if rel else None
    if copia is None or not copia.exists():
        r["veredicto"] = "copia_ausente"
        r["mensaje"] = ("hay hash de validación pero falta la copia congelada ({}). No se "
                        "puede mostrar qué se validó.".format(rel))
        return r, 1

    r["copia_validada"] = str(copia)
    if hash_actual == hash_sellado:
        r["veredicto"] = "coincide"
        r["mensaje"] = "la fuente es la misma que se validó el {}.".format(
            fm.get("fecha_validacion"))
        return r, 0

    r["veredicto"] = "difiere"
    r["bloquea_publicacion"] = True
    r["mensaje"] = ("la fuente cambió después de validarse el {}. Nada se puede dar por "
                    "sincronizado hasta resolverlo: revalidar con el equipo, o revertir a la "
                    "copia congelada.".format(fm.get("fecha_validacion")))
    r["como_ver_el_cambio"] = 'comparar_contenido.py "{}" "{}" --modo estricto'.format(
        copia, ruta)
    return r, 1


def sellar(ruta, validado_por, fecha=None):
    ruta = Path(ruta)
    fecha = fecha or _hoy()
    doc, fm = _leer_fm(ruta)

    destino_dir = ruta.parent / DIR_VALIDADO
    destino_dir.mkdir(exist_ok=True)
    leeme = destino_dir / "README.md"
    if not leeme.exists():
        leeme.write_text(LEEME, encoding="utf-8")

    copia = destino_dir / "{}.{}.md".format(ruta.stem, fecha)
    shutil.copy2(ruta, copia)

    huella = hash_contenido(doc["bloques"])
    _escribir_campos(ruta, {
        "estado": "validado",
        "validado_por": validado_por,
        "fecha_validacion": fecha,
        "hash_validado": huella,
        "copia_validada": "{}/{}".format(DIR_VALIDADO, copia.name),
    })

    # Se relee y se comprueba: el vault vive en iCloud, y una escritura que no sincronizó se
    # parece mucho a una que falló. Regla invariante 3 del skill.
    doc2, fm2 = _leer_fm(ruta)
    ok = (fm2.get("hash_validado") == huella
          and hash_contenido(doc2["bloques"]) == huella
          and copia.exists())

    return {
        "pieza": str(ruta), "veredicto": "sellada" if ok else "verificacion_fallida",
        "validado_por": validado_por, "fecha_validacion": fecha,
        "hash_validado": huella, "copia_validada": str(copia),
        "relectura_ok": ok,
        "mensaje": ("sellada y releída correctamente." if ok else
                    "SE ESCRIBIÓ PERO LA RELECTURA NO COINCIDE. Revisar a mano antes de "
                    "confiar en esta validación."),
    }, (0 if ok else 2)


def main():
    ap = argparse.ArgumentParser(
        description="Sella y verifica la versión validada por el equipo médico.")
    ap.add_argument("pieza")
    ap.add_argument("--validado-por", metavar="QUIÉN",
                    help="sella una validación nueva. ESCRIBE en la pieza y crea la copia.")
    ap.add_argument("--fecha", metavar="AAAA-MM-DD")
    ap.add_argument("--verificar", action="store_true")
    ap.add_argument("--mostrar", action="store_true")
    args = ap.parse_args()

    if not Path(args.pieza).exists():
        print("error: no existe {}".format(args.pieza), file=sys.stderr)
        return 2

    try:
        if args.validado_por:
            print("AVISO: esta invocación escribe en {} y crea su copia congelada."
                  .format(args.pieza), file=sys.stderr)
            r, code = sellar(args.pieza, args.validado_por, args.fecha)
        elif args.verificar:
            r, code = verificar(args.pieza)
        else:
            r, code = mostrar(args.pieza), 0
    except Exception as e:
        print("error: {}".format(e), file=sys.stderr)
        return 2

    print(json.dumps(r, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
