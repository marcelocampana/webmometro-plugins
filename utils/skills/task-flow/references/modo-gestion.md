# Modo 1 · Gestión normal (sin flag)

**Abrir una tarea** — tres movimientos, en este orden. (Antes, si `tareas.md` está sobre el umbral o
hay cerradas de más de un mes, ofrécelo en una línea: `archivado.md`.)

1. `git status` y `git fetch`; con `main` limpia y actualizada, `git switch -c <rama>` con un nombre
   que describa la tarea. **Nunca se trabaja sobre `main`**, y si un merge quedó pendiente **avisa de
   que `main` está desactualizada y decide antes de empezar**: la rama nueva no sale de la rama previa.
2. Anota el **Inicio** en la fila de su sección y el estado `🔵 En curso`. La hora sale de
   `date '+%Y-%m-%d %H:%M'`, **nunca inventada**.
3. **Sube su fila a `## Ahora`** con la misma Tarea, Sección, Estado e Inicio, y el `#` que le
   corresponda por su posición. **Pregunta al usuario en qué posición va** — la prioridad la decide
   él, y abrir una tarea no dice dónde quiere el resto de la cola.

**Cerrar una tarea** — **tres confirmaciones, en este orden, y ninguna se da por supuesta**:

1. **¿Terminada?** Informa de lo hecho y pregunta si queda cerrada. Con el visto bueno, cierra la
   fila: son **cinco movimientos y ninguno es opcional**.
   1. Estado a `✅ Completada`, y rellena Completada y Duración.
   2. Baja esa fila al final de su sección, bajo las que sigan abiertas.
   3. Actualiza **el total de la sección** (el total va por sección, no al pie del archivo).
   4. **Borra su fila de `## Ahora`** —y si su Nota decía algo que valga, pásalo a Comentarios antes—,
      y renumera el `#` de las filas que queden.
   5. **Archiva el comentario**: el texto íntegro (≤900 chars) va a `tareas/historial/AAAA-MM.md` y en
      la celda queda un **resumen ≤240 chars + el enlace `[detalle](...)`**. Muestra el resumen en una
      línea para que el usuario lo corrija. Cómo se escribe: `archivado.md`.
2. **¿Commit?** En la rama de la tarea: lo resuelto y la fila cerrada, en un solo commit.
3. **¿Merge a `main`?** Hecho el commit, propón integrar la rama.

La Duración sale de `git reflog`/`git log` y es **tiempo de trabajo**: las pausas largas se descuentan
y se explican en Comentarios; las estimadas llevan `~`. Comandos y casos: `tiempos.md`.

Al cerrar, **ofrece** para `revisar.md` lo que el trabajo dejó pendiente (propone y espera). Comprueba
también si hay tareas cerradas hace **más de un mes** para mover su fila al historial (etapa 2,
`archivado.md`) — con confirmación. Después **para**: puedes sugerir la siguiente, no empezarla.

**Pausar o bloquear** — Estado en **los dos sitios**, la fila no se mueve, Nota obligatoria en
`Bloqueada`. Una `Bloqueada` **no se toma aunque sea la primera fila**: avisa y propón la siguiente.
Reglas completas en `estados.md`.

**Crear y priorizar** — aquí vive la asistencia, con dos reglas no opcionales: **ninguna tarea se crea
sin contexto del proyecto** y **toda sugerencia se ancla en algo verificable** (un archivo, una deuda
declarada, un hallazgo de la conversación); sin ancla, no se propone. Qué leer: `contextualizacion.md`.
Propón el enunciado afinado y tus observaciones, y **espera**: el protocolo es **propone y espera**, en
las tres listas y también para lo que dicta el usuario. Sugiere la sección por el ámbito del cambio. Una tarea nueva va en la
sección de su área, sobre las `Completada`, en `Pendiente` y sin Inicio; **sube a `## Ahora` solo
cuando el usuario la prioriza**. Sobre el orden de la cola, **recomienda con motivo y no reordenes
solo**.

**Consultar** — «qué sigue», «qué hay bloqueado», «cuánto llevamos»: **solo lectura**. Al responder
añade el aviso si el orden tiene un conflicto real (la primera depende de una de más abajo). Usa los
resúmenes de la celda Comentarios: **no abras detalles del historial en una consulta**.

**La invariante de siempre: la siguiente tarea es la primera fila de `## Ahora` que no esté
`Bloqueada`.** No «la primera pendiente leyendo de arriba abajo», ni una de más abajo porque parezca
más rápida.

## Redacción de tareas

Verbo + objeto concreto + ámbito: «Corregir el desplegable del menú en móvil (`AppHeader.vue`)», no
«arreglar el menú». La Tarea es **una línea**; el detalle va a Comentarios. Si el enunciado necesita
una «y», probablemente son dos tareas. Si el usuario rechaza tu redacción, se usa la suya.

Anatomía, cuándo partir una tarea y ejemplos antes/después: `redaccion-tareas.md`.

## Formato de las tablas

Las columnas verbatim, las reglas de celda (`<br>`, `\|` escapado) y la forma de una celda cerrada
están en `formato-tablas.md`. Lo imprescindible: la Tarea es una línea, el detalle va a Comentarios, y
**el archivo no se recalcula solo**.
