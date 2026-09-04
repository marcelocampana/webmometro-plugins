#!/usr/bin/env python3
"""
Compara palabra por palabra dos versiones de una pieza de contenido y dice dónde difieren.

Determinista y exhaustivo: si difiere un carácter, sale en la salida. Es la capa 1 de
content-sync-check — dice DÓNDE difiere, no qué significa. La interpretación (si un texto se
movió o falta, si un reorden cambia el sentido) la hace el modelo con las reglas del skill.

Maneja tres formatos: el .md fuente del workspace, el .md del repo Nuxt, y el .dc.html del
proyecto de diseño (donde el texto vive en constantes JS, no en el marcado).

No depende de PyYAML — usa un parser mínimo de frontmatter, igual que salud_cluster.py del
skill content-cluster-builder.

Uso:
    python3 comparar_contenido.py <fuente> <destino>
    python3 comparar_contenido.py fuente.md destino.md --modo estricto
    python3 comparar_contenido.py fuente.md "Portada v2.dc.html" --variante desktop
    python3 comparar_contenido.py --auditar-mapeo contexto/configuracion.md --raiz .

Códigos de salida: 0 sin diferencias · 1 hay diferencias · 2 error de uso o parseo.
"""

import argparse
import difflib
import hashlib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path


# --- Normalización ---------------------------------------------------------------------------
#
# Hay DOS normalizaciones y no son intercambiables. Confundirlas es el error más caro de este
# módulo: una decide si dos textos coinciden, la otra solo sirve para reconocer un texto que
# cambió de lugar. Si se usa la difusa para verificar, "mama" y "mamá" pasan por iguales — y en
# contenido clínico eso es exactamente lo que no puede ocurrir.

_COMILLAS_SIMPLES = dict.fromkeys(map(ord, "‘’‚‛′"), "'")
_COMILLAS_DOBLES = dict.fromkeys(map(ord, "“”„‟«»″"), '"')
_GUIONES = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")
_ESPACIOS = dict.fromkeys(map(ord, "        "), " ")

_TIPOGRAFIA = {}
_TIPOGRAFIA.update(_COMILLAS_SIMPLES)
_TIPOGRAFIA.update(_COMILLAS_DOBLES)
_TIPOGRAFIA.update(_GUIONES)
_TIPOGRAFIA.update(_ESPACIOS)

_PUNTUACION = re.compile(r"[^\w\s]", re.UNICODE)
_WHITESPACE = re.compile(r"\s+")


def normalizar_estricta(s):
    """Normaliza para VERIFICAR. Preserva tildes, mayúsculas, ñ, dígitos y signos.

    'mama' != 'mamá' · '5.333' != '5,333' · 'puede' != 'Puede'

    Solo absorbe lo que no cambia lo que alguien lee: entidades HTML, la forma de composición
    Unicode, comillas y guiones tipográficos frente a rectos, y el espaciado.

    NO usar para emparejar texto movido — para eso está normalizar_difusa().
    """
    if s is None:
        return ""
    s = html.unescape(str(s))
    # NFC, nunca NFKD: NFKD descompone las tildes y las perderíamos al comparar.
    s = unicodedata.normalize("NFC", s)
    s = s.translate(_TIPOGRAFIA)
    s = s.replace("…", "...")
    return _WHITESPACE.sub(" ", s).strip()


def normalizar_difusa(s):
    """Normaliza para EMPAREJAR texto que cambió de lugar. Descarta tildes, caja y puntuación.

    NUNCA para decidir si dos textos coinciden: bajo esta normalización 'mamá' y 'mama' son
    iguales, y una diferencia clínica real pasaría por equivalente. Solo la consume la
    detección de reubicaciones y el emparejamiento de bloques.

    Es la misma normalización que describe dispositivos.md para buscar texto entre variantes.
    """
    s = normalizar_estricta(s).casefold()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = _PUNTUACION.sub(" ", s)
    return _WHITESPACE.sub(" ", s).strip()


# --- Tokenización ----------------------------------------------------------------------------

_TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


_MARCADOR = re.compile(r"\[PENDIENTE[^\]]*\]", re.IGNORECASE)
_ENFASIS = re.compile(r"(\*\*|\*|__|_|`)")
_ENLACE_MD = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def texto_visible(s):
    """Quita el marcado que no se lee: énfasis, comillas de código, y el destino de un enlace.

    El énfasis y los enlaces se comparan por su texto visible (comparacion.md). Que un enlace
    cambie de destino sí es hallazgo, pero eso lo cubre el bloque del propio campo `to`/`href`,
    no el texto del párrafo que lo contiene.
    """
    s = _ENLACE_MD.sub(r"\1", normalizar_estricta(s))
    s = _ENFASIS.sub("", s)
    # Los marcadores de pendiente son andamiaje editorial: que el destino no los arrastre no
    # es una diferencia de contenido. Se cuentan aparte, en marcadores_pendiente, porque una
    # pieza aprobada que aún los lleva es algo que hay que saber antes de publicar.
    s = _MARCADOR.sub("", s)
    return _WHITESPACE.sub(" ", s).strip()


def tokenizar(s):
    """Parte en palabras y signos. Cada signo de puntuación es un token propio: en contenido
    clínico un signo puede cambiar la lectura ('puede tratarse.' vs 'puede tratarse?')."""
    return _TOKEN.findall(texto_visible(s))


def tokenizar_difuso(s):
    return normalizar_difusa(s).split()


# --- Hash de contenido -----------------------------------------------------------------------

_SEP_CAMPO = "\x1f"
_SEP_BLOQUE = "\x1e"


def hash_contenido(bloques):
    """Huella del contenido comparable, no del archivo.

    Se calcula sobre el texto normalizado-estricto de cada bloque precedido de su id, en orden
    de documento. Consecuencias deliberadas:

    - Reordenar claves del frontmatter, cambiar una comilla recta por tipográfica o que iCloud
      reescriba los saltos de línea NO cambia el hash. Un ancla que grita en falso deja de
      creerse.
    - Mover un bloque SÍ cambia el hash: contra la versión validada, moverse es una diferencia.
    - La metadata de proceso queda fuera (ver CAMPOS_PROCESO), o escribir el hash cambiaría el
      hash.
    - Usa la MISMA normalización que el comparador. Si divergieran, el hash diría "igual" y el
      diff "distinto", y no habría a cuál creer.
    """
    # texto_visible, no normalizar_estricta: es exactamente lo que compara el diff. Si el hash
    # se calculara sobre otra cosa, diría "igual" donde el diff dice "distinto" y no habría a
    # cuál creer.
    #
    # Los campos del frontmatter van ORDENADOS POR id, no por posición en el archivo: en YAML
    # el orden de las claves no es contenido, y reordenarlas no cambia lo que nadie lee. Si el
    # hash dependiera de él, mover 'kind' dos líneas rompería el ancla y el equipo recibiría
    # "esto ya no es lo que validaste" por un cambio que no tocó una palabra.
    #
    # La prosa del cuerpo sí conserva su orden de documento: ahí la secuencia SÍ es contenido
    # —una advertencia antes o después de aquello a lo que advierte no dice lo mismo— y su id
    # ya lleva el número de párrafo, así que ordenar por id preserva esa secuencia.
    partes = sorted(b["id"] + _SEP_CAMPO + texto_visible(b["texto"]) for b in bloques)
    payload = _SEP_BLOQUE.join(partes).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


# --- Metadata que no se compara --------------------------------------------------------------
#
# Lista cerrada, tomada de references/comparacion.md. Vive en la fuente porque el equipo la
# necesita y no viaja al destino por diseño: su ausencia allí es lo esperado, no un hallazgo.

CAMPOS_PROCESO = frozenset({
    "origen_spoke", "pilar", "keyword_objetivo", "keywords_secundarias",
    "volumen_mensual", "intencion", "audiencia", "voz", "estado",
    "fecha_aprobacion", "fecha_redaccion", "schema_sugerido",
    "spokes_relacionados", "url_existente",
    # Campos del ancla de validación: también son proceso.
    "validado_por", "fecha_validacion", "hash_validado", "copia_validada",
    "variaciones_dispositivo",
})


# --- Parser mínimo de frontmatter YAML -------------------------------------------------------
#
# Extiende el de salud_cluster.py con listas de objetos anidados (stats.groups[].items[]) y
# escalares de bloque (| y >), que las fuentes de este workspace sí usan.

def _leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def _parse_scalar(s):
    """Devuelve el valor como TEXTO siempre, salvo null y booleanos.

    Deliberadamente NO convierte a int/float, al contrario que salud_cluster.py, que sí lo
    hace porque calcula métricas. Aquí todo se compara como texto, y la conversión numérica
    destruiría justo el dato que más importa: con float(), '+5.500' (cinco mil quinientos, con
    separador de miles español) se leería como 5.5, y '670.000' como 670.0. Una cifra clínica
    corrompida antes de compararla es peor que no compararla.
    """
    s = s.strip()
    if s in ("", "null", "~"):
        return None
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    return s


def _parse_block_scalar(lines, i, indent, plegado):
    """Escalar de bloque: | conserva saltos, > los plieg a espacios."""
    trozos = []
    while i < len(lines):
        if lines[i].strip() == "":
            trozos.append("")
            i += 1
            continue
        if _leading_spaces(lines[i]) < indent:
            break
        trozos.append(lines[i][indent:])
        i += 1
    while trozos and trozos[-1] == "":
        trozos.pop()
    return (" ".join(t.strip() for t in trozos) if plegado else "\n".join(trozos)), i


def _parse_map(lines, i, indent):
    result = {}
    while i < len(lines):
        if lines[i].strip() == "" or lines[i].lstrip().startswith("#"):
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
        if rest in ("|", "|-", ">", ">-"):
            hijo = indent + 2
            for j in range(i, len(lines)):
                if lines[j].strip():
                    hijo = _leading_spaces(lines[j])
                    break
            value, i = _parse_block_scalar(lines, i, hijo, rest.startswith(">"))
        elif rest == "":
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
    """Lista de escalares o de objetos. El caso de objetos es el que salud_cluster.py no cubre
    y que stats.groups[].items[] necesita."""
    result = []
    while i < len(lines):
        if lines[i].strip() == "" or lines[i].lstrip().startswith("#"):
            i += 1
            continue
        if _leading_spaces(lines[i]) < indent:
            break
        stripped = lines[i].strip()
        if not stripped.startswith("-"):
            break
        resto = stripped[1:].strip()
        i += 1
        # "- clave: valor" abre un objeto cuyas claves siguen indentadas al nivel del guión.
        if resto and ":" in resto and not (resto[0] in ("'", '"')):
            clave, _, val = resto.partition(":")
            sangria_obj = indent + (len(stripped) - len(stripped.lstrip("- ")))
            sub = ["{}{}".format(" " * sangria_obj, resto)]
            while i < len(lines):
                if lines[i].strip() == "":
                    sub.append("")
                    i += 1
                    continue
                if _leading_spaces(lines[i]) < sangria_obj:
                    break
                if _leading_spaces(lines[i]) == sangria_obj and lines[i].strip().startswith("- "):
                    break
                sub.append(lines[i])
                i += 1
            obj, _ = _parse_map(sub, 0, sangria_obj)
            result.append(obj)
        else:
            result.append(_parse_scalar(resto))
    return result, i


def parse_frontmatter(text):
    """Devuelve (frontmatter, cuerpo)."""
    if not text.startswith("---"):
        return {}, text
    partes = text.split("---", 2)
    if len(partes) < 3:
        return {}, text
    data, _ = _parse_map(partes[1].split("\n"), 0, 0)
    return data, partes[2]


# --- Extractores: de archivo a lista de bloques ----------------------------------------------
#
# Un Documento es {"formato", "bloques", "frontmatter_crudo", "avisos"}. Cada bloque es
# {"id", "tipo", "texto", "orden"}: el id nombra dónde vive el texto para que el reporte pueda
# decir "stats.groups[2].items[0].value" y no "algo en stats".

_SLUG = re.compile(r"[^\w\s-]", re.UNICODE)


def _slug(s, limite=48):
    s = _SLUG.sub("", normalizar_estricta(s)).strip()
    return _WHITESPACE.sub("-", s)[:limite] or "s-n"


_RUTA_IMAGEN = re.compile(r"^[\w./~-]+\.(png|jpe?g|svg|webp|avif|gif)$", re.IGNORECASE)


def _es_ruta_imagen(texto):
    return bool(_RUTA_IMAGEN.match(texto.strip()))


def _aplanar(valor, prefijo, bloques, avisos):
    """Recorre el frontmatter y emite un bloque por cada texto comparable."""
    if valor is None or isinstance(valor, bool):
        return
    if isinstance(valor, dict):
        for clave, sub in valor.items():
            if not prefijo and clave in CAMPOS_PROCESO:
                continue
            _aplanar(sub, "{}.{}".format(prefijo, clave) if prefijo else str(clave),
                     bloques, avisos)
        return
    if isinstance(valor, list):
        for idx, sub in enumerate(valor):
            _aplanar(sub, "{}[{}]".format(prefijo, idx), bloques, avisos)
        return
    texto = str(valor).strip()
    if not texto:
        return
    # Las rutas de imagen se comparan por nombre de archivo, no por ruta: '/images/x.png' y
    # 'assets/x.png' apuntan al mismo recurso y el destino resuelve las suyas (comparacion.md).
    # Si el NOMBRE difiere, sigue siendo hallazgo.
    if _es_ruta_imagen(texto):
        bloques.append({"id": prefijo, "tipo": "imagen", "texto": Path(texto).name,
                        "texto_completo": texto, "orden": len(bloques)})
        return
    bloques.append({"id": prefijo, "tipo": "campo", "texto": texto, "orden": len(bloques)})


_NOTA_INTERNA = re.compile(r"<!--(.*?)-->", re.DOTALL)
_ENCABEZADO = re.compile(r"^(#{1,6})\s+(.*)$")


def _bloques_prosa(cuerpo, bloques, avisos):
    """Trocea el cuerpo por encabezado y párrafo. Los comentarios HTML no son contenido: son
    notas internas del equipo, y si aparecen en un destino eso sí es un hallazgo."""
    for m in _NOTA_INTERNA.finditer(cuerpo):
        avisos.append({"tipo": "nota_interna", "texto": m.group(1).strip()[:200]})
    cuerpo = _NOTA_INTERNA.sub("\n", cuerpo)

    seccion, n = "cuerpo", 0
    for parrafo in re.split(r"\n\s*\n", cuerpo):
        parrafo = parrafo.strip()
        if not parrafo:
            continue
        enc = _ENCABEZADO.match(parrafo)
        if enc:
            seccion = _slug(enc.group(2))
            n = 0
            bloques.append({"id": "cuerpo:{}".format(seccion), "tipo": "encabezado",
                            "texto": enc.group(2).strip(), "orden": len(bloques)})
            continue
        n += 1
        bloques.append({"id": "cuerpo:{}#{}".format(seccion, n), "tipo": "prosa",
                        "texto": parrafo, "orden": len(bloques)})


def extraer_md(texto, formato):
    """Extractor de los dos .md: el fuente del workspace y el del repo Nuxt. Comparten forma;
    lo único que cambia es qué metadata trae cada uno, y esa ya se filtra por CAMPOS_PROCESO."""
    fm, cuerpo = parse_frontmatter(texto)
    bloques, avisos = [], []
    _aplanar(fm, "", bloques, avisos)
    _bloques_prosa(cuerpo, bloques, avisos)
    return {"formato": formato, "bloques": bloques, "frontmatter_crudo": fm, "avisos": avisos}


def detectar_formato(ruta, texto):
    nombre = str(ruta).lower()
    if nombre.endswith(".dc.html") or nombre.endswith(".html"):
        return "dc-html"
    if "web/contenido/" in str(ruta).replace("\\", "/"):
        return "md-fuente"
    fm, _ = parse_frontmatter(texto)
    if any(c in fm for c in ("estado", "fecha_aprobacion", "origen_spoke",
                             "keyword_objetivo", "voz", "hash_validado")):
        return "md-fuente"
    return "md-nuxt"


def cargar(ruta, formato_pedido="auto", variante="desktop"):
    texto = Path(ruta).read_text(encoding="utf-8")
    formato = detectar_formato(ruta, texto) if formato_pedido == "auto" else formato_pedido
    if formato == "dc-html":
        doc = extraer_dc_html(texto, variante)
    else:
        doc = extraer_md(texto, formato)
    doc["ruta"] = str(ruta)
    doc["formato_detectado"] = formato
    return doc


# --- Extractor .dc.html ----------------------------------------------------------------------
#
# Una página .dc.html no guarda su texto en el marcado: lo guarda en constantes de un script y
# lo renderiza con plantillas. Buscarlo en el HTML visible da por ausente lo que sí está.

_SECCION_VARIANTE = re.compile(r"<!--\s*=*\s*(DESKTOP|MOBILE|M[OÓ]VIL)\s*=*\s*-->", re.I)
_CONST = re.compile(r"const\s+([A-Za-z_$][\w$]*)\s*=\s*\[")
_COMENTARIO_SECCION = re.compile(r"<!--\s*([^=][^-]*?)\s*-->")
_NO_CONTENIDO = re.compile(r"^(tf|t[A-Z]\w*|styles?|colors?|state|cfg|config|opts|els?|refs?)$")
_CLAVES_PROSA = frozenset({
    "q", "a", "t", "title", "label", "body", "v", "value", "k", "speaker", "desc",
    "descripcion", "text", "texto", "name", "nombre", "caption", "alt", "cita", "quote",
    "subtitle", "subtitulo", "scope", "note", "nota",
})


def _cerrar_literal(texto, inicio):
    """Devuelve el índice tras el ] que cierra el array abierto en `inicio`.

    Se hace con balance de corchetes y máquina de estados de comillas, no con regex: los
    literales traen \' escapados y corchetes dentro de las cadenas, y una regex los cortaría
    por el sitio equivocado.
    """
    prof, i, n = 0, inicio, len(texto)
    comilla = None
    while i < n:
        c = texto[i]
        if comilla:
            if c == "\\":
                i += 2
                continue
            if c == comilla:
                comilla = None
        elif c in ("'", '"', "`"):
            comilla = c
        elif c == "[":
            prof += 1
        elif c == "]":
            prof -= 1
            if prof == 0:
                return i + 1
        i += 1
    return -1


def _cadenas_js(literal):
    """Extrae [(clave, valor)] de un literal JS. clave es None en arrays de strings planos."""
    salida = []
    i, n = 0, len(literal)
    clave = None
    while i < n:
        c = literal[i]
        if c in ("'", '"', "`"):
            j, buf = i + 1, []
            while j < n:
                if literal[j] == "\\" and j + 1 < n:
                    buf.append(literal[j + 1])
                    j += 2
                    continue
                if literal[j] == c:
                    break
                buf.append(literal[j])
                j += 1
            valor = "".join(buf)
            # ¿es una clave entre comillas seguida de ':'?
            k = j + 1
            while k < n and literal[k] in " \t\n":
                k += 1
            if k < n and literal[k] == ":":
                clave = valor
                i = k + 1
                continue
            salida.append((clave, valor))
            clave = None
            i = j + 1
            continue
        if c.isalpha() or c == "_":
            j = i
            while j < n and (literal[j].isalnum() or literal[j] in "_$"):
                j += 1
            palabra = literal[i:j]
            k = j
            while k < n and literal[k] in " \t\n":
                k += 1
            if k < n and literal[k] == ":":
                clave = palabra
                i = k + 1
                continue
            i = j
            continue
        i += 1
    return salida


def _quitar(texto, etiqueta):
    return re.sub(r"<{0}\b.*?</{0}>".format(etiqueta), " ", texto, flags=re.S | re.I)


def extraer_dc_html(texto, variante="desktop"):
    avisos, bloques = [], []

    # 1 · Partir por variante. La portada real trae DESKTOP y MOBILE en el mismo archivo.
    marcas = list(_SECCION_VARIANTE.finditer(texto))
    if marcas:
        quiere_movil = variante == "movil"
        tramos = []
        for idx, m in enumerate(marcas):
            fin = marcas[idx + 1].start() if idx + 1 < len(marcas) else len(texto)
            es_movil = m.group(1).upper().startswith("M")
            if es_movil == quiere_movil:
                tramos.append(texto[m.end():fin])
        cuerpo = "\n".join(tramos) if tramos else texto
        if not tramos:
            avisos.append("no hay tramo {} en el archivo; se comparó el documento entero"
                          .format(variante))
    else:
        cuerpo = texto
        avisos.append("el archivo no separa DESKTOP/MOBILE; se comparó entero")

    # 2 · Constantes JS. Aquí vive casi todo el texto.
    for m in _CONST.finditer(texto):
        nombre = m.group(1)
        if _NO_CONTENIDO.match(nombre):
            avisos.append("const {} ignorada: no es contenido".format(nombre))
            continue
        fin = _cerrar_literal(texto, m.end() - 1)
        if fin < 0:
            avisos.append("const {}: no se pudo cerrar el literal".format(nombre))
            continue
        pares = _cadenas_js(texto[m.end() - 1:fin])
        utiles = [(k, v) for k, v in pares
                  if v.strip() and (k is None or k in _CLAVES_PROSA)]
        if not utiles:
            avisos.append("const {} ignorada: sin claves de prosa".format(nombre))
            continue
        # Un elemento nuevo empieza cada vez que se repite una clave ya vista: así
        # {q,a},{q,a} numera 0 y 1 aunque falte alguna clave en medio.
        idx, vistas = 0, set()
        for k, v in utiles:
            if k is None:
                ident = "js:{}[{}]".format(nombre, idx)
                idx += 1
            else:
                if k in vistas:
                    idx += 1
                    vistas = set()
                vistas.add(k)
                ident = "js:{}[{}].{}".format(nombre, idx, k)
            bloques.append({"id": ident, "tipo": "js", "texto": v, "orden": len(bloques)})

    # 3 · Texto fijo del marcado, sin scripts ni estilos ni plantillas sin resolver.
    visible = _quitar(_quitar(cuerpo, "script"), "style")
    seccion = "html"
    for trozo in re.split(r"(<!--.*?-->)", visible, flags=re.S):
        com = _COMENTARIO_SECCION.fullmatch(trozo.strip()) if trozo.strip().startswith("<!--") else None
        if com:
            seccion = _slug(com.group(1))
            continue
        plano = re.sub(r"<[^>]+>", "\n", trozo)
        for linea in plano.split("\n"):
            linea = linea.strip()
            if not linea or "{{" in linea or len(linea) < 2:
                continue
            bloques.append({"id": "html:{}#{}".format(seccion, len(bloques)),
                            "tipo": "html", "texto": linea, "orden": len(bloques)})

    if len(bloques) < 20:
        avisos.append("solo {} bloques extraídos de un .dc.html: sospecha de extracción "
                      "fallida, no de página vacía".format(len(bloques)))

    doc = {"formato": "dc-html", "bloques": bloques, "frontmatter_crudo": {}, "avisos": avisos}
    doc["variante"] = variante
    return doc


_FILA = re.compile(r"^\|(.+)\|\s*$")


def _limpiar_celda(c):
    """Quita el marcado de la celda: backticks, énfasis y notas en cursiva del tipo
    `ruta.md` *(sin publicar)*. Lo que queda es la ruta desnuda, o nada."""
    c = re.sub(r"\*\([^)]*\)\*|\*[^*]*\*", " ", c)
    # Solo backticks y asteriscos: el guion bajo NO es marcado aquí, es parte de nombres de
    # campo reales como project_id o design_system.
    return re.sub(r"[`*]", "", c).strip()


def _celdas(linea):
    return [_limpiar_celda(c) for c in linea.strip().strip("|").split("|")]


def _vacia(celda):
    """— , (sin publicar), (falta fuente) y variantes significan ausencia."""
    return celda.strip() in ("", "-", "—", "–") or celda.strip().startswith("(")


def _seccion(texto, titulo):
    m = re.search(r"^###\s*{}\s*$".format(re.escape(titulo)), texto, re.M)
    if not m:
        return ""
    resto = texto[m.end():]
    # Corta en el siguiente encabezado de cualquier nivel, incluido otro ### hermano.
    sig = re.search(r"^#{2,6}\s", resto, re.M)
    return resto[:sig.start()] if sig else resto


def _clave_valor(bloque):
    """Lee tanto la forma tabular (| Campo | Valor |) como la de lista (clave: valor).

    modo-inicio.md especifica listas, pero la configuración real de este workspace usa
    tablas. Se aceptan las dos: un parser que solo entienda lo documentado no sirve para lo
    que hay en disco.
    """
    datos = {}
    for linea in bloque.split("\n"):
        m = _FILA.match(linea)
        if m:
            c = _celdas(linea)
            # Se descartan la fila de cabecera y la separadora (|---|---|), que tras limpiar
            # el marcado quedan vacías o con solo guiones.
            clave = c[0].lower()
            if len(c) >= 2 and clave and clave != "campo" and not set(clave) <= set("-: "):
                datos.setdefault(clave, c[1])
            continue
        if ":" in linea and not linea.strip().startswith(("#", ">", "|")):
            k, _, v = linea.partition(":")
            if k.strip() and " " not in k.strip():
                datos.setdefault(k.strip().lower(), v.strip())
    return datos


def auditar_mapeo(ruta_config, raiz="."):
    """Diagnostica qué piezas del mapeo quedan fuera del chequeo y qué rutas no resuelven.

    NO escribe nada. Existe porque una pieza sin `estado:` se salta en silencio: el reporte
    sale limpio y parece completo sin serlo.
    """
    raiz = Path(raiz).resolve()
    texto = Path(ruta_config).read_text(encoding="utf-8")
    m = re.search(r"^##\s*Destinos de publicaci[óo]n\s*$", texto, re.M)
    if not m:
        raise ValueError("no hay seccion 'Destinos de publicacion' en {}".format(ruta_config))
    sig = re.search(r"^##\s", texto[m.end():], re.M)
    seccion = texto[m.end():m.end() + sig.start()] if sig else texto[m.end():]

    repo = _clave_valor(_seccion(seccion, "Repo del sitio"))
    design = _clave_valor(_seccion(seccion, "Claude Design"))
    ruta_repo = Path(repo["ruta"]).expanduser() if repo.get("ruta") else None

    piezas, rutas_rotas, fuera = [], [], []
    for linea in _seccion(seccion, "Mapeo de páginas").split("\n"):
        if not _FILA.match(linea):
            continue
        c = _celdas(linea)
        if len(c) < 2 or c[0].lower().startswith("fuente") or set(c[0]) <= set("-: "):
            continue

        fila = {"fuente": None if _vacia(c[0]) else c[0],
                "sitio": None if len(c) < 2 or _vacia(c[1]) else c[1],
                "canvas_desktop": None if len(c) < 3 or _vacia(c[2]) else c[2],
                "canvas_movil": None if len(c) < 4 or _vacia(c[3]) else c[3]}

        if fila["fuente"]:
            ruta_f = raiz / "web" / "contenido" / fila["fuente"]
            fila["existe"] = ruta_f.exists()
            if not ruta_f.exists():
                rutas_rotas.append({"declarado": fila["fuente"], "tipo": "fuente",
                                    "no_encontrado_en": str(ruta_f)})
                fila["estado"] = None
            else:
                fm, _ = parse_frontmatter(ruta_f.read_text(encoding="utf-8"))
                fila["estado"] = fm.get("estado")
                fila["validada"] = bool(fm.get("hash_validado"))
                if not fila["estado"]:
                    fuera.append({"fuente": fila["fuente"],
                                  "motivo": "sin campo estado: en el frontmatter"})
                elif fila["estado"] not in ("aprobado", "validado", "publicado"):
                    fuera.append({"fuente": fila["fuente"],
                                  "motivo": "estado '{}': no entra al chequeo"
                                            .format(fila["estado"])})
        else:
            fila["existe"] = False
            fuera.append({"fuente": None, "sitio": fila["sitio"],
                          "motivo": "sin archivo fuente: no hay contra que comparar"})

        if fila["sitio"] and ruta_repo:
            rs = ruta_repo / "content" / fila["sitio"]
            if not rs.exists():
                rutas_rotas.append({"declarado": fila["sitio"], "tipo": "sitio",
                                    "no_encontrado_en": str(rs)})
        piezas.append(fila)

    avisos = []
    if ruta_repo and not ruta_repo.exists():
        avisos.append("la ruta del repo del sitio no existe: {}".format(ruta_repo))
    espejo = repo.get("espejo_disenos")
    if ruta_repo and espejo:
        pe = ruta_repo / espejo.split()[0].strip("`/") if espejo.split() else ruta_repo
        if not pe.exists():
            avisos.append("el espejo local declarado no existe: {}".format(pe))
        elif not any(pe.iterdir()):
            avisos.append("el espejo local esta vacio: {}".format(pe))
    if not design.get("project_id"):
        avisos.append("sin project_id de Claude Design: ese destino no se puede verificar")

    return {
        "version_esquema": 1,
        "configuracion": str(ruta_config),
        "repo_sitio": repo.get("ruta"),
        "project_id_design": design.get("project_id"),
        "piezas": piezas,
        "resumen": {
            "mapeadas": len(piezas),
            "verificables": sum(1 for p in piezas if p.get("estado") in
                                ("aprobado", "validado", "publicado")),
            "fuera_del_chequeo": len(fuera),
            "rutas_rotas": len(rutas_rotas),
        },
        "fuera_del_chequeo": fuera,
        "rutas_rotas": rutas_rotas,
        "avisos": avisos,
    }

# --- Emparejamiento de bloques ---------------------------------------------------------------

UMBRAL_EMPAREJAMIENTO = 0.60


def _similitud(a, b):
    return difflib.SequenceMatcher(None, tokenizar_difuso(a), tokenizar_difuso(b),
                                   autojunk=False).ratio()


def emparejar_bloques(doc_a, doc_b, umbral=UMBRAL_EMPAREJAMIENTO):
    """Empareja primero por id idéntico; lo que sobra, por parecido de contenido.

    El segundo paso es lo que permite comparar una fuente con stats.groups[2].items[0] contra
    un destino con stats.items[1]: nombres distintos, mismo dato. Sin él, cada reestructuración
    del esquema produciría el hallazgo doble (falta aquí / sobra allá) que reparar duplicaría.
    """
    por_id_b = {b["id"]: b for b in doc_b["bloques"]}
    pares, resto_a = [], []
    usados = set()

    for a in doc_a["bloques"]:
        b = por_id_b.get(a["id"])
        # El id solo se acepta si además el contenido coincide. Los ids de prosa llevan el
        # número de párrafo dentro de su sección, así que dos párrafos intercambiados casan
        # por id con el texto cruzado: emparejarlos así produciría dos diferencias falsas en
        # vez de un reordenamiento. Con contenido distinto se deja al emparejador por
        # similitud, que sí los reencuentra en su nueva posición.
        if b is not None and a["id"] not in usados and \
                texto_visible(a["texto"]) == texto_visible(b["texto"]):
            pares.append((a, b))
            usados.add(a["id"])
        else:
            resto_a.append(a)

    resto_b = [b for b in doc_b["bloques"] if b["id"] not in usados]

    # Greedy sobre los mejores candidatos: se ordenan todas las combinaciones por similitud y
    # se van tomando las que no consuman un bloque ya emparejado.
    candidatos = []
    for a in resto_a:
        for b in resto_b:
            s = _similitud(a["texto"], b["texto"])
            if s >= umbral:
                candidatos.append((s, a["orden"], b["orden"], a, b))
    candidatos.sort(key=lambda c: (-c[0], c[1], c[2]))

    tomados_a, tomados_b = set(), set()
    for s, _, _, a, b in candidatos:
        if a["orden"] in tomados_a or b["orden"] in tomados_b:
            continue
        pares.append((a, b))
        tomados_a.add(a["orden"])
        tomados_b.add(b["orden"])

    solo_a = [a for a in resto_a if a["orden"] not in tomados_a]
    solo_b = [b for b in resto_b if b["orden"] not in tomados_b]

    # Último recurso: un bloque que quedó sin par pero cuyo id existe en el otro lado y
    # también quedó libre. Es el campo reescrito de arriba abajo —una cifra sustituida, un
    # párrafo rehecho— que no llega al umbral de similitud. Sin este paso se reportaría como
    # "falta aquí" y "sobra allá", el hallazgo doble que al repararse duplica el contenido.
    libres_b = {b["id"]: b for b in solo_b}
    rescatados_a, rescatados_b = [], set()
    for a in solo_a:
        b = libres_b.get(a["id"])
        if b is not None and b["id"] not in rescatados_b:
            pares.append((a, b))
            rescatados_a.append(a["orden"])
            rescatados_b.add(b["id"])

    solo_a = [a for a in solo_a if a["orden"] not in rescatados_a]
    solo_b = [b for b in solo_b if b["id"] not in rescatados_b]
    return pares, solo_a, solo_b


# --- Diff ------------------------------------------------------------------------------------

CONTEXTO_TOKENS = 5


def diff_bloque(bloque_a, bloque_b):
    """Diff palabra por palabra de un par de bloques. Devuelve [] si son idénticos."""
    ta, tb = tokenizar(bloque_a["texto"]), tokenizar(bloque_b["texto"])
    if ta == tb:
        return []

    # autojunk=False es obligatorio: con listas de más de 200 elementos, difflib descarta los
    # tokens "populares", y en prosa española eso significa descartar 'no', 'de', 'la'. Un diff
    # que ignora 'no' por frecuente es justo el fallo que este script viene a eliminar.
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    opcodes = [o for o in sm.get_opcodes() if o[0] != "equal"]

    # Cuando el bloque se reescribió casi entero, trocearlo en fragmentos no ayuda a nadie:
    # se emite una sola diferencia con las dos versiones literales. La regla de comparacion.md
    # es que el texto se cita, y media frase citada no se puede juzgar.
    if sm.ratio() < 0.5 or len(opcodes) > 3:
        return [{
            "op": "reescrito",
            "bloque": bloque_a["id"],
            "bloque_destino": bloque_b["id"],
            "fuente": texto_visible(bloque_a["texto"]),
            "destino": texto_visible(bloque_b["texto"]),
            "similitud": round(sm.ratio(), 2),
        }]

    salida = []
    for op, i1, i2, j1, j2 in opcodes:
        salida.append({
            "op": op,
            "bloque": bloque_a["id"],
            "bloque_destino": bloque_b["id"],
            "fuente": " ".join(ta[i1:i2]),
            "destino": " ".join(tb[j1:j2]),
            "contexto_izq": " ".join(ta[max(0, i1 - CONTEXTO_TOKENS):i1]),
            "contexto_der": " ".join(ta[i2:i2 + CONTEXTO_TOKENS]),
        })
    return salida


# --- Orden de bloques ------------------------------------------------------------------------

def comparar_orden(pares_identicos):
    """Detecta bloques que coinciden en contenido pero cambiaron de posición.

    Es el caso que ninguna otra comprobación cubre: el diff dice "todo presente" y nadie ve que
    el orden visible cambió. En contenido clínico importa — una advertencia separada de aquello
    a lo que advierte, un dato lejos de la fuente que lo respalda.
    """
    # Solo la prosa del cuerpo tiene orden significativo. El orden de las claves del
    # frontmatter no es contenido —reordenarlas no cambia lo que nadie lee— y levantarlo como
    # hallazgo enseñaría a ignorar esta sección, que existe para el caso que sí importa: una
    # advertencia que se separó de aquello a lo que advierte.
    pares_identicos = [(a, b) for a, b in pares_identicos
                       if a["id"].startswith("cuerpo:") or a["id"].startswith("html:")]
    if not pares_identicos:
        return {"identico": True, "movidos": []}

    sec_a = [a["orden"] for a, _ in pares_identicos]
    orden_b = {a["orden"]: b["orden"] for a, b in pares_identicos}
    # Los bloques "en su sitio" son los de la subsecuencia común más larga entre el orden de A
    # y el orden en que aparecen en B.
    sec_b_por_a = [orden_b[o] for o in sec_a]
    ranking = sorted(range(len(sec_b_por_a)), key=lambda i: sec_b_por_a[i])
    esperado = sorted(range(len(sec_a)))
    sm = difflib.SequenceMatcher(None, esperado, ranking, autojunk=False)
    en_sitio = set()
    for i1, j1, n in sm.get_matching_blocks():
        for k in range(n):
            en_sitio.add(esperado[i1 + k])

    movidos = []
    for idx, (a, b) in enumerate(pares_identicos):
        if idx not in en_sitio:
            movidos.append({
                "bloque": a["id"], "bloque_destino": b["id"],
                "posicion_fuente": a["orden"], "posicion_destino": b["orden"],
                "texto": a["texto"][:120],
            })
    return {"identico": not movidos, "movidos": movidos}


# --- Reubicaciones ---------------------------------------------------------------------------

VENTANA_REUBICACION = 9


def detectar_reubicaciones(solo_a, solo_b, doc_b):
    """Antes de declarar que un texto falta, lo busca en TODO el destino, no solo en su bloque.

    El diff es ciego a esto por diseño: un párrafo que el diseño movió aparece como una
    eliminación aquí y una inserción allá. Leído así produce dos hallazgos falsos — y si se
    repara el primero sin ver el segundo, el párrafo queda duplicado.
    """
    indice = []
    for b in doc_b["bloques"]:
        toks = tokenizar_difuso(b["texto"])
        indice.append((b, toks, set(
            " ".join(toks[i:i + VENTANA_REUBICACION])
            for i in range(max(1, len(toks) - VENTANA_REUBICACION + 1))
        )))

    reubicaciones, restantes_a = [], []
    consumidos_b = set()
    for a in solo_a:
        toks = tokenizar_difuso(a["texto"])
        if len(toks) < 4:
            restantes_a.append(a)
            continue
        ventanas = [" ".join(toks[i:i + VENTANA_REUBICACION])
                    for i in range(max(1, len(toks) - VENTANA_REUBICACION + 1))]
        mejor, mejor_cob = None, 0.0
        for b, _, vent_b in indice:
            if not ventanas:
                continue
            cob = sum(1 for v in ventanas if v in vent_b) / len(ventanas)
            if cob > mejor_cob:
                mejor, mejor_cob = b, cob
        if mejor is not None and mejor_cob >= 0.5:
            reubicaciones.append({
                "tipo": "reubicacion", "origen": a["id"], "destino": mejor["id"],
                "cobertura": round(mejor_cob, 2), "texto": a["texto"][:200],
            })
            consumidos_b.add(mejor["id"])
        else:
            restantes_a.append(a)

    restantes_b = [b for b in solo_b if b["id"] not in consumidos_b]
    return reubicaciones, restantes_a, restantes_b


# --- Orquestación ----------------------------------------------------------------------------

def _marcadores(doc):
    cuenta = {}
    for b in doc["bloques"]:
        for m in _MARCADOR.findall(b["texto"]):
            cuenta[m] = cuenta.get(m, 0) + 1
    return ["{} ×{}".format(k, v) for k, v in sorted(cuenta.items())]


def comparar(doc_a, doc_b, modo="normal", umbral=UMBRAL_EMPAREJAMIENTO):
    pares, solo_a, solo_b = emparejar_bloques(doc_a, doc_b, umbral)

    diferencias, identicos = [], []
    for a, b in pares:
        d = diff_bloque(a, b)
        if d:
            diferencias.extend(d)
        else:
            identicos.append((a, b))

    reubicaciones, solo_a, solo_b = detectar_reubicaciones(solo_a, solo_b, doc_b)
    orden = comparar_orden(identicos)

    hay_dif = bool(diferencias or solo_a or solo_b)
    if hay_dif:
        veredicto = "difiere"
    elif reubicaciones or not orden["identico"]:
        veredicto = "identico_reordenado"
    else:
        veredicto = "identico"

    # En modo estricto se compara contra la versión que validó el equipo médico: cualquier
    # diferencia bloquea, incluidas las reubicaciones y el reorden. Contra la validada, "solo
    # se movió" no atenúa nada.
    if modo == "estricto":
        bloquea = veredicto != "identico"
    else:
        bloquea = False

    fm_a = doc_a.get("frontmatter_crudo") or {}
    notas_en_destino = [a for a in doc_b.get("avisos", [])
                        if isinstance(a, dict) and a.get("tipo") == "nota_interna"]

    return {
        "version_esquema": 1,
        "modo": modo,
        "veredicto": veredicto,
        "bloquea_publicacion": bloquea,
        "fuente": {
            "ruta": doc_a.get("ruta"), "formato_detectado": doc_a.get("formato_detectado"),
            "bloques": len(doc_a["bloques"]),
            "estado": fm_a.get("estado"), "fecha_aprobacion": fm_a.get("fecha_aprobacion"),
            "hash_actual": hash_contenido(doc_a["bloques"]),
        },
        "destino": {
            "ruta": doc_b.get("ruta"), "formato_detectado": doc_b.get("formato_detectado"),
            "bloques": len(doc_b["bloques"]), "variante": doc_b.get("variante"),
            "hash_actual": hash_contenido(doc_b["bloques"]),
        },
        "resumen": {
            "bloques_identicos": len(identicos),
            "bloques_con_diferencia": len({d["bloque"] for d in diferencias}),
            "solo_en_fuente": len(solo_a), "solo_en_destino": len(solo_b),
            "reubicaciones": len(reubicaciones), "orden_identico": orden["identico"],
        },
        "diferencias": diferencias,
        "solo_en_fuente": [{"bloque": b["id"], "texto": b["texto"]} for b in solo_a],
        "solo_en_destino": [{"bloque": b["id"], "texto": b["texto"]} for b in solo_b],
        "reubicaciones": reubicaciones,
        "orden": orden,
        "marcadores_pendiente": _marcadores(doc_a),
        "notas_internas_en_destino": notas_en_destino,
        "avisos": [a for a in doc_a.get("avisos", []) + doc_b.get("avisos", [])
                   if not (isinstance(a, dict) and a.get("tipo") == "nota_interna")],
    }


def render_texto(r):
    L = []
    L.append("{} → {}".format(r["fuente"]["ruta"], r["destino"]["ruta"]))
    L.append("{} · {} bloques vs {}".format(
        r["veredicto"].upper(), r["fuente"]["bloques"], r["destino"]["bloques"]))
    if r["bloquea_publicacion"]:
        L.append("*** BLOQUEA PUBLICACIÓN ***")
    s = r["resumen"]
    L.append("  {} idénticos · {} con diferencia · {} solo en fuente · {} solo en destino"
             " · {} reubicaciones · orden {}".format(
                 s["bloques_identicos"], s["bloques_con_diferencia"], s["solo_en_fuente"],
                 s["solo_en_destino"], s["reubicaciones"],
                 "igual" if s["orden_identico"] else "distinto"))
    if r["diferencias"]:
        L.append("\nDIFERENCIAS")
        for d in r["diferencias"]:
            L.append("  {} [{}]".format(d["bloque"], d["op"]))
            L.append("    fuente : {}".format(d["fuente"] or "(nada)"))
            L.append("    destino: {}".format(d["destino"] or "(nada)"))
    if r["solo_en_fuente"]:
        L.append("\nSOLO EN LA FUENTE (no llegó al destino)")
        for b in r["solo_en_fuente"]:
            L.append("  {}: {}".format(b["bloque"], b["texto"][:110]))
    if r["solo_en_destino"]:
        L.append("\nSOLO EN EL DESTINO (nadie lo aprobó)")
        for b in r["solo_en_destino"]:
            L.append("  {}: {}".format(b["bloque"], b["texto"][:110]))
    if r["reubicaciones"]:
        L.append("\nREUBICACIONES (mismo texto, otro bloque)")
        for x in r["reubicaciones"]:
            L.append("  {} → {} ({:.0%})".format(x["origen"], x["destino"], x["cobertura"]))
    if not r["orden"]["identico"]:
        L.append("\nORDEN")
        for m in r["orden"]["movidos"]:
            L.append("  {}: posición {} → {}".format(
                m["bloque"], m["posicion_fuente"], m["posicion_destino"]))
    if r["marcadores_pendiente"]:
        L.append("\nMARCADORES DE PENDIENTE: " + ", ".join(r["marcadores_pendiente"]))
    if r["notas_internas_en_destino"]:
        L.append("\n⚠ NOTAS INTERNAS FILTRADAS AL DESTINO: {}".format(
            len(r["notas_internas_en_destino"])))
    if r["avisos"]:
        L.append("\nAVISOS")
        for a in r["avisos"]:
            L.append("  {}".format(a if isinstance(a, str) else json.dumps(a, ensure_ascii=False)))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(
        description="Compara palabra por palabra dos versiones de una pieza de contenido.")
    ap.add_argument("fuente", nargs="?")
    ap.add_argument("destino", nargs="?")
    ap.add_argument("--formato-fuente", default="auto",
                    choices=["auto", "md-fuente", "md-nuxt", "dc-html"])
    ap.add_argument("--formato-destino", default="auto",
                    choices=["auto", "md-fuente", "md-nuxt", "dc-html"])
    ap.add_argument("--variante", default="desktop", choices=["desktop", "movil"])
    ap.add_argument("--modo", default="normal", choices=["normal", "estricto"])
    ap.add_argument("--umbral-emparejamiento", type=float, default=UMBRAL_EMPAREJAMIENTO)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--texto", action="store_true")
    ap.add_argument("--auditar-mapeo", metavar="CONFIGURACION")
    ap.add_argument("--raiz", default=".")
    args = ap.parse_args()

    if args.auditar_mapeo:
        try:
            r = auditar_mapeo(args.auditar_mapeo, args.raiz)
        except Exception as e:
            print("error: {}".format(e), file=sys.stderr)
            return 2
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    if not args.fuente or not args.destino:
        ap.error("hacen falta <fuente> y <destino>, o --auditar-mapeo")

    try:
        doc_a = cargar(args.fuente, args.formato_fuente, args.variante)
        doc_b = cargar(args.destino, args.formato_destino, args.variante)
    except FileNotFoundError as e:
        print("error: no existe {}".format(e.filename), file=sys.stderr)
        return 2
    except Exception as e:
        print("error al leer o parsear: {}".format(e), file=sys.stderr)
        return 2

    r = comparar(doc_a, doc_b, args.modo, args.umbral_emparejamiento)

    # JSON por defecto salvo que se pida texto explícitamente o stdout sea un terminal.
    if args.json or (not args.texto and not sys.stdout.isatty()):
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(render_texto(r))

    return 1 if r["veredicto"] != "identico" else 0


if __name__ == "__main__":
    sys.exit(main())
