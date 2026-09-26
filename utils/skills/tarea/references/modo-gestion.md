# Modo 1 · Gestión normal (sin flag)

`tareas.md` es la cola de lo confirmado: `## Ahora` más lo pendiente, en curso, pausado o bloqueado
de cada sección. Nada completado se queda aquí — se archiva en el mismo cierre.

**Repo conectado a Toggl** (marcador `<!-- tarea: toggl … -->`): crear, abrir, pausar y cerrar
añaden su parte según `toggl.md` —marcas locales y, solo al crear y al cerrar, Toggl en bloque—, sin
ninguna pregunta más. Donde abajo dice Inicio, Completada, Duración, `Vence` o `Coste`, en ese repo
salen de ahí y no se escriben en `tareas.md`.

**Abrir una tarea** — tres movimientos, en este orden. (Antes, si `tareas.md` está sobre el umbral,
ofrécelo en una línea: `archivado.md`.)

1. `git status` y `git fetch`; con `main` limpia y actualizada, `git switch -c <rama>` con un nombre
   que describa la tarea. **Nunca se trabaja sobre `main`**, y si un merge quedó pendiente **avisa de
   que `main` está desactualizada y decide antes de empezar**: la rama nueva no sale de la rama previa.
2. Anota el **Inicio** en la fila de su sección y el estado `🔵 En curso`. La hora sale de
   `date '+%Y-%m-%d %H:%M'`, **nunca inventada**.
3. **Sube su fila a `## Ahora`** con la misma Tarea, Sección, Estado, Vence y Coste, y el `#` que le
   corresponda por su posición. **El Inicio no se copia**: vive solo en la fila de la sección, que es
   la fuente de verdad. **Pregunta al usuario en qué posición va** — la prioridad la decide él, y
   abrir una tarea no dice dónde quiere el resto de la cola.

**Cerrar una tarea** — **una sola confirmación**; con ella se ejecuta la cadena entera sin pausas.

1. **¿Terminada?** Informa de lo hecho en 2-3 líneas y pide el visto bueno de cierre. Es la única
   pregunta: no hay una segunda pregunta para el commit ni una tercera para el merge.
2. **Con el visto bueno, anuncia la cadena en una línea** («Cierro, commiteo y mergeo a `main`») y
   ejecútala sin pausas:
   1. Cierra la fila: **cinco movimientos y ninguno es opcional**.
      1. Estado a `✅ Completada`, y rellena Completada y Duración.
      2. **Archiva el comentario y la fila juntos**, en el mismo paso: el texto íntegro (≤900 chars)
         va a `tareas/historial/AAAA-MM.md` bajo el `###` de su sección de origen (`archivado.md`).
      3. **Quita la fila de su sección en `tareas.md`** — no queda rastro por fila: ni resumen, ni
         enlace, ni la fila en `Completada`.
      4. **Actualiza el total acumulado en `secciones.md`**, en la entrada de esa sección (sube el
         total y el contador de archivadas; `secciones-catalogo.md`). Si la sección **se queda sin
         ninguna fila activa** en `tareas.md`, **quita también su header `##`** de `tareas.md` — la
         entrada en `secciones.md` es lo único que la conserva.
      5. **Borra su fila de `## Ahora`** —y si su Nota decía algo que valga, pásalo a Comentarios
         antes de archivar—, y renumera el `#` de las filas que queden.
   2. **Commit**, en la rama de la tarea: lo resuelto y la fila cerrada, en un solo commit.
   3. **Merge a `main`**, sin pedir un tercer visto bueno.

**Impacto documental** — con el merge hecho, busca en el diff de la rama (`git diff --name-only
main@{1}...`) señales de documentación corta: estructura, un archivo que el README enumera, un
comando, una dependencia o una convención de `CLAUDE.md`. **Sin señal, silencio total.** Con señal:
`impacto-documental.md`.

**Tres frenos, y solo esos, detienen la cadena** — no son ceremonia, son una excepción real que el
usuario tiene que decidir:

- **`main` no está limpia o está desactualizada** cuando toca mergear: detente ahí, dilo y espera.
- **El merge tiene conflictos**: detente, muestra qué archivos chocan y espera instrucción. No
  resuelvas un conflicto por tu cuenta.
- **Al ir a commitear aparecen cambios sin relación con la tarea**: detente y pregunta si van
  incluidos en el commit o se dejan fuera, antes de seguir.

Fuera de esos tres casos la cadena no se pausa. **Si el usuario encargó la tarea completa**
(«termínala sin pedirme confirmación»), ese encargo ya es el visto bueno del paso 1. El resumen del
comentario archivado se muestra **después**, en la línea de cierre.

La Duración es **tiempo de trabajo**, con las pausas descontadas (`tiempos.md`).

Al cerrar, **ofrece** para `revisar.md` lo que el trabajo dejó pendiente (propone y espera). Después
**para**: puedes sugerir la siguiente, no empezarla.

**Pausar o bloquear** — Estado en **los dos sitios**, la fila no se mueve, Nota obligatoria en
`Bloqueada`. Una `Bloqueada` **no se toma aunque sea la primera fila**: avisa y propón la siguiente
(`estados.md`).

**Crear y priorizar** — aquí vive la asistencia, con dos reglas no opcionales: **ninguna tarea se crea
sin contexto del proyecto** (`contextualizacion.md`) y **toda sugerencia se ancla en algo verificable**
—un archivo, una deuda declarada, un hallazgo de la conversación—; sin ancla, no se propone. Propón el
enunciado afinado y **espera**: el protocolo es **propone y espera**, también para lo que dicta el
usuario. Sugiere la sección por el ámbito del cambio. **Las tareas ordenan al usuario; el plan, a
Claude**: los pasos de un plan que Claude ejecuta de corrido son **una** tarea (`redaccion-tareas.md`,
«Cuándo partir una tarea»).

**La propuesta ya trae el `Coste` estimado**, y ahí ocurre toda la planificación de este skill: una
pregunta, con el número puesto y la posición como única decisión del usuario. **Si no hay base va `—`
y se dice**; nunca se inventa. Cómo se estima y cómo se presenta: `estimacion.md`. `Vence` solo se
pregunta si hay un compromiso externo real.

Una tarea nueva crea el header de su sección en `tareas.md` si esa sección ya existe en
`secciones.md` pero no tiene fila activa ahí, o propone la sección como nueva —ampliando el
catálogo— si no existe en ninguno de los dos (`secciones-catalogo.md`). Va en `Pendiente` y sin
Inicio; **sube a `## Ahora` solo cuando el usuario la prioriza**. Sobre el orden de la cola,
**recomienda con motivo y no reordenes solo**.

**Consultar** — «qué sigue», «qué hay bloqueado», «cuánto llevamos»: **solo lectura**. Avisa si el
orden tiene un conflicto real (la primera depende de una de más abajo). **No abras el historial.**

**`Vence` audita ese orden, no lo cambia.** Si sumando los `Coste` de la cola una tarea fechada cae
después de su límite, **dilo en una línea y ofrece subirla**; nunca la muevas solo. Sin `Coste` en las
filas de por medio no hay aviso que dar: no se avisa a ojo.

**La invariante de siempre: la siguiente tarea es la primera fila de `## Ahora` que no esté
`Bloqueada`.** No «la primera pendiente de arriba abajo», ni una de más abajo por parecer más rápida.

## Redacción y formato

**Verbo + objeto concreto + ámbito**, en una línea (`redaccion-tareas.md`); columnas y celdas en
`formato-tablas.md`. **El archivo no se recalcula solo.**
