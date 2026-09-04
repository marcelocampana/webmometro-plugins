---
name: content-sync-check
description: >
  Verifica que el contenido aprobado del cliente coincida en todos sus destinos —el repo del sitio
  (Nuxt Content), el proyecto de Claude Design y su espejo local— y repara las diferencias con
  confirmación. Úsalo cuando el usuario pregunte "¿está sincronizado el contenido?", "¿el sitio tiene
  la última versión?", "¿Claude Design está actualizado?", "verifica que la página coincida con la
  fuente", "compara el contenido con lo publicado"; cuando diga que corrigió algo en un destino y no
  en los otros ("lo cambié en Nuxt pero no en Design", "el equipo editorial mandó correcciones");
  cuando vaya a publicar o dar por cerrada una página y quiera comprobarla antes; o cuando pida
  "pasa la corrección a Claude Design", "actualiza el sitio con la fuente", "sincroniza el
  contenido". **Actívalo solo si el proyecto tiene `contexto/`** —es el ancla del workspace de
  cliente—, o si el usuario pide montar la configuración. NO lo uses para redactar o corregir
  contenido (eso es de los skills de contenido), para revisar SEO o CRO de una página (seo-suite),
  ni para sincronizar código que no sea contenido editorial.
argument-hint: "[--init | --reparar | <página>]"
metadata:
  version: 1.1.0
---

# Verificación de contenido entre destinos (content-sync-check)

El contenido aprobado vive una vez en el workspace y se copia a varios destinos: el repo del sitio,
el proyecto de diseño y su espejo local. **Cada copia puede quedarse atrás sin que nada lo señale**,
y en contenido médico eso no es un detalle de forma. Este skill compara la fuente contra sus
destinos, dice qué difiere, y —con confirmación pieza por pieza— lo repara.

**La regla que gobierna todo: la fuente manda.** Las correcciones se hacen primero en el archivo
fuente; los destinos se alimentan de ella. Un cambio hecho solo en un destino es un hallazgo que
resolver, nunca una verdad que se propague sola.

**Este archivo es el núcleo.** El detalle de cada modo vive en `references/`.

## Qué leer según lo que se pida

| Si el usuario… | Lee |
| --- | --- |
| pide verificar, comparar o revisar si algo está al día | `references/verificacion.md` |
| pide aplicar, corregir, propagar o sincronizar (`--reparar`) | `references/reparacion.md` |
| pide montar la configuración, o el Paso 0 no la encuentra (`--init`) | `references/modo-inicio.md` |
| pregunta cómo se compara un campo concreto, o qué se ignora | `references/comparacion.md` |
| necesita sacar el texto de una página de diseño (`.dc.html`) | `references/extraccion.md` |
| compara escritorio contra móvil, o pregunta si una omisión importa | `references/dispositivos.md` |
| va a comparar, o el script devuelve algo que no sabe leer | `references/comparador.md` |
| pregunta si lo que se publicará es lo que validó el equipo médico, o hay que sellar una validación | `references/validacion.md` |
| encuentra que **varios lados divergen a la vez**, o pregunta cuál gobierna | `references/reconciliacion.md` |

**Se lee la referencia del modo invocado y ninguna más.**

## Paso 0 · Precondición (siempre, antes de todo)

1. **Resolver la raíz del cliente.** Sube desde el directorio activo hasta encontrar `contexto/`.
   Es el ancla del workspace de cliente; el skill opera en el **proyecto activo**, no en el repo
   del marketplace. Si no hay `contexto/` en ningún nivel: **retírate en silencio** si el usuario
   no pidió nada de sincronización; dilo en una línea si lo pidió.
2. **Leer los destinos** en `contexto/configuracion.md`, sección `## Destinos de publicación`.
   Tres desenlaces:
   - **Existe y está completa** → sigue al paso 3.
   - **Falta, o falta el repo del sitio** → `references/modo-inicio.md`.
   - **Existe pero incompleta** (páginas sin mapear, colecciones nuevas) → dilo en una línea y
     ofrece completarla; no la corrijas por tu cuenta.
3. **Verificar el repo del sitio.** Que la ruta exista y tenga su archivo de esquema
   (`content.config.ts` en Nuxt Content). Sin él no hay contra qué comparar campos: dilo y sigue
   solo con los destinos que sí resuelvan.
4. **Verificar el acceso al proyecto de diseño**, si hay `project_id` (`DesignSync`,
   `method: get_project`). Si falla o no hay id, **continúa sin ese destino diciéndolo** — nunca en
   silencio. Un chequeo parcial informado vale; uno que calla lo que no miró, no.

## Los destinos

```text
contexto/configuracion.md   ← dónde están los destinos (§ Destinos de publicación)
web/contenido/**            ← FUENTE: lo aprobado, lo único que se edita a mano
<repo-sitio>/content/**     ← destino: lo que sirve el sitio
<proyecto de diseño>        ← destino: lo que ve el cliente (vía DesignSync)
<repo-sitio>/htmls/         ← espejo local; no versionado, se desfasa solo
```

## Qué se compara y qué no

**Solo se verifica lo aprobado**: una pieza entra si su frontmatter dice `estado: aprobado`,
`validado` o `publicado`. **`validado` es distinto de `aprobado`**: hay una copia congelada de lo
que revisó el equipo médico y un hash, y contra ella el diff manda sin excepción (`validacion.md`). Un borrador que no coincide con el sitio no es un hallazgo, es un borrador. Ese campo
lo mantiene `task-flow` al cerrar la tarea que aprueba la pieza.

**Ante la duda, se reporta.** Solo se descarta lo identificable con certeza —un campo de proceso
con nombre conocido, una diferencia tipográfica, andamiaje—, nunca por parecer poco importante: un
aviso de más cuesta una línea, uno de menos puede dejar sin ver una cifra. Y se clasifica **por lo
que dice el texto, no por el bloque donde vive**.

**Lo que nunca es un hallazgo** (lista cerrada en `comparacion.md`): la metadata de proceso
editorial que no viaja al sitio (`origen_spoke`, `keyword_objetivo`, `voz`, notas internas), las
diferencias de capitalización en nombres de archivo, y la ausencia de una variante de dispositivo
que no existe.

**Lo que siempre es un hallazgo**: un campo presente en la fuente y ausente en el destino, un texto
que difiere, y un destino modificado después de la fecha de aprobación de la fuente.

**Dos cosas parecen hallazgo y no lo son**: texto que solo cambió de bloque (`comparacion.md`) y
diferencias entre escritorio y móvil, donde condensar es diseño (`dispositivos.md`).

## Las tres direcciones, y la que no existe

| Dirección | Qué significa | Se propaga |
| --- | --- | --- |
| fuente → sitio | Lo aprobado no llegó a publicarse | Sí, con confirmación |
| fuente → Claude Design | El canvas quedó atrás de una corrección | Sí, con confirmación |
| Claude Design → fuente | El cambio se acordó sobre el diseño y no volvió | Sí, con confirmación |
| **sitio → fuente** | **Se editó el sitio directamente** | **No.** Se reporta y se pide decisión |

La cuarta no se propaga a propósito: aceptar el sitio como origen consagraría la práctica que este
skill corrige. Se informa y decide el usuario.

## Reglas invariantes

1. **Nada se escribe sin visto bueno**, en ningún destino, y la confirmación es **por pieza**: una
   aprobación no autoriza el resto del lote.
2. **Antes de escribir se muestra** qué destino, qué campo, texto actual y texto propuesto.
3. **Tras escribir se relee** el archivo y se verifica que quedó como debía.
4. **El chequeo no modifica la fuente** salvo en la dirección Claude Design → fuente, y con la
   misma confirmación explícita.
5. **Un destino inaccesible se declara**; no se omite del reporte ni se da por coincidente.
6. **Solo se compara contra artefactos publicados**: la página del proyecto de diseño, no el
   material temporal que el usuario le pasó al chat como contexto.
7. **Cuando divergen varios lados a la vez, el skill no elige**: reconstruye qué pasó, muestra las
   versiones literales y deja la decisión al usuario (`reconciliacion.md`).
8. **La fuente se actualiza primero**, incluso cuando el contenido viene de un destino; la
   propagación al resto sale siempre de ella.
9. **Se lee la referencia del modo invocado y ninguna más.**

## Manejo de errores del Paso 0

| Situación | Qué hacer |
| --- | --- |
| No hay `contexto/` y no se pidió nada | Retírate en silencio. No lo menciones. |
| No hay `## Destinos de publicación` | `modo-inicio.md` si el usuario pidió algo; si no, dilo en una línea. |
| La ruta del repo del sitio no existe | Dilo, ofrece corregirla en `configuracion.md`, y sigue con los demás destinos. |
| Falta el `project_id` de Claude Design | Sigue sin ese destino y anótalo como pendiente en el reporte. |
| `get_project` falla (sin acceso, id inválido) | Dilo en una línea con el id probado; no reintentes en bucle. Si es de permisos, `modo-inicio.md`. |
| Una pieza sin `estado:` | No la verifiques; ofrece añadírselo (lo pone `task-flow` al aprobar). |

Los errores propios de cada modo están en su referencia.

## Recursos

- `scripts/comparar_contenido.py` — diff determinista palabra por palabra entre dos archivos
  (`.md` fuente, `.md` de Nuxt, `.dc.html`). Salida JSON. Uso: `references/comparador.md`.
- `scripts/sellar_validacion.py` — sella y verifica la versión que validó el equipo médico.
  Uso: `references/validacion.md`.

Si un script no corre, dilo y compara leyendo (`comparacion.md`). Nunca des por coincidente lo que
no se pudo procesar.

## Idioma

Español neutro con el usuario. El contenido comparado, en el idioma del proyecto — **el texto de
las piezas nunca se traduce ni se reescribe de estilo**: se compara y se copia literal.
