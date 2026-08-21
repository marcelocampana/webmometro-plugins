# Archivado del historial

El comentario y la fila de una tarea cerrada pesan mucho más que lo que se consulta después: el
comentario ~10× más que el resto de la fila (30% del archivo frente a 3%), y una fila `Completada`
que se queda en `tareas.md` es justo el peso que ese archivo no debería cargar.

**Un solo movimiento al cerrar, y un solo archivo mensual por mes.** El comentario y la fila completa
se archivan juntos, en el instante del cierre — no hay una espera de un mes ni una etapa posterior.

```text
tareas/historial/
├── 2026-08.md   ← comentarios y filas de todo lo cerrado este mes
└── 2026-07.md
```

## El archivado, al cerrar

**Todo lo de una tarea cerrada sale de `tareas.md` en el mismo cierre**: el comentario íntegro y la
fila completa. `tareas.md` queda con solo lo abierto o por abrirse en breve; el peso del historial no
se acumula ni un día dentro del archivo principal.

**El comentario** (≤900 chars: trampa, decisión no evidente, efecto colateral, medidas no
recuperables del repo) va bajo `## Comentarios` del mensual, como `### <ancla>` en kebab-case sin
tildes.

**La fila** (ya `✅ Completada`, con Completada y Duración) va bajo `## Tareas archivadas` del mismo
mensual, agrupada por su sección de origen — ver «El formato del mensual» abajo. Su enlace en
Comentarios pasa a ser ancla del mismo archivo (`[detalle](#el-ancla)`) — nunca
`historial/AAAA-MM.md#...`, porque fila y comentario viven en el mismo mensual desde el principio.

**En `tareas.md` no queda ningún rastro de la fila** — ni resumen, ni enlace, ni una fila en
`Completada`. El único rastro es el total acumulado y el contador de archivadas, y viven en
`tareas/secciones.md`, en la entrada de esa sección (`secciones-catalogo.md`). Mientras la sección
siga teniendo alguna fila activa, ese mismo total se refleja también bajo su tabla en `tareas.md`.

**Si la sección se queda sin ninguna fila activa**, su header `##` se quita de `tareas.md` en el
mismo movimiento: no hay secciones vacías ni con solo `Completada` dentro del archivo principal.

**Confirmación:** va dentro de la única confirmación de cierre, así que no añade una pregunta aparte.
Di en una línea que la tarea quedó archivada en el mensual y **muestra el resumen del comentario**
para que el usuario lo corrija si hace falta.

## El umbral

Red de seguridad, no mecanismo principal —de eso se encarga el archivado al cerrar—. Se anota al
inicio de `tareas.md`:

```markdown
<!-- task-flow: umbral 40000 chars · holgura 70% · última revisión 2026-08-20 -->
```

Por defecto ~40.000 chars (~10k tokens). Al vivir en el archivo es visible y editable; el skill lo
respeta y no lo reescribe sin permiso. **Se mide con `wc -c`**: exacto y sin depender de un
tokenizador (4 chars ≈ 1 token, solo para explicárselo al usuario).

Con archivado inmediato, el umbral **nunca puede deberse a filas cerradas acumuladas** — lo que ya
cerró se movió al mensual en su momento. Si el archivo supera el umbral, el peso está en lo abierto
o en comentarios largos de tareas en curso — y ahí **dilo y no archives nada**: no hay ninguna fila
cerrada que mover, porque ya se movió al cerrarse.

## El formato del mensual

Desde `assets/historial.esqueleto.md`: zona `## Comentarios` (un `### <título>` en kebab-case sin
tildes por comentario — es el ancla del enlace) y zona `## Tareas archivadas`, que agrupa por
sección de origen con **un header real por sección**: un `### <Sección>` por cada sección que tenga
alguna fila archivada ese mes, y bajo cada uno su tabla con las mismas columnas que en `tareas.md`
(`Estado | Tarea | Inicio | Completada | Duración | Comentarios`). El nombre del `###` es **el mismo
nombre de la sección de origen** en `tareas.md` — no se abrevia ni se renombra. Columnas idénticas =
mover una fila es cortar y pegar, sin reformatear.

El orden de los `###` es **de la sección más reciente en tener una fila archivada a la más antigua**
dentro del mes — no el orden de `tareas.md` — porque lo que se consulta primero al abrir un mensual
es lo que se acaba de cerrar. El total agregado del mes va al pie, una sola cifra (el total por
sección vive en `secciones.md`, no aquí).

## Reversión

Recuperar una tarea archivada la devuelve a su sección **con el comentario íntegro**, no con el
resumen recortado, y la quita del mensual — de las dos zonas: su `###` de Comentarios y su fila en
Tareas archivadas. El historial no es un destino de solo ida.

**Si la sección ya no tiene header en `tareas.md`** (se había vaciado), se recrea en su posición de
orden estable (`seccionamiento.md`) y se resta 1 del contador de archivadas en `secciones.md`. El
total acumulado en `secciones.md` no se toca: sigue contando ese tiempo como trabajo ya hecho,
independientemente de que la tarea vuelva a estar abierta.

**Si era la única fila archivada de esa sección ese mes**, se retira también su `### <Sección>` ya
vacío de `## Tareas archivadas` en el mensual.

## Errores

- **Enlace a un mensual o ancla que no existe** → dilo y ofrece reconstruirlo; no inventes el
  comentario.
- **Fila en el mensual sin su comentario, o al revés** → avisa y ofrece reunirlos.
- **Umbral editado a un valor absurdo** → dilo y propón uno razonable; no lo cambies solo.
- **Un comentario no baja de 900 sin perder lo accionable** → deja lo que quepa y dilo. Antes perder
  relato que perder la trampa.
- **Piden archivar una tarea abierta** → no se hace: solo `✅ Completada`.
- **Piden reabrir una archivada** → se revierte, ver «Reversión» arriba.
- **La sección de una fila reactivada no existe ni en `tareas.md` ni en `secciones.md`** → no
  debería pasar (el catálogo es persistente); si ocurre, dilo y ofrece reconstruir la entrada del
  catálogo antes de devolver la fila.
