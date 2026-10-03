# Gestión: empezar y cerrar el trabajo de Claude en un repo

El trabajo de Claude no está en Toggl: se identifica por el **slug** de su plan. El tiempo de Claude
y lo que se crea en Toggl son de `tarea/references/ciclo.md`; aquí va lo que añade el repo.

## Planificar

Claude arma su plan como siempre (en modo plan, si el usuario lo usa). **Ninguna propuesta sin
contexto del proyecto** (`contextualizacion.md`), y toda sugerencia se ancla en algo verificable.

- **El plan se guarda** en `tareas/planes/<slug>.md` desde `assets/plan.esqueleto.md`: el contenido
  del plan aprobado, sin reformatearlo, más el marcador y la tabla de pasos con su **skill** y su
  **contexto**. El slug: el objetivo en minúsculas y con guiones.
- **Termina con «Esto te toca a ti»** si hay algo que Claude no puede hacer y que le ocupa tiempo al
  usuario (`tarea`). El usuario elige qué va a Toggl, cuando quiera.
- **Las decisiones** se piden en el momento; si quedan abiertas, van a `pendientes.md`, `Espera tu
  decisión`.
- **Si no cabe en una sesión**, se dice al planificar: lo que no se alcance irá a `pendientes.md`
  como `Por hacer`, con el plan ya escrito.
- **Área** (una de `config.md`) y **coste** estimado desde el historial (`estimacion.md`), en la
  cabecera del plan.

Se aprueba **una vez**, y eso cubre la ejecución entera. El plan se commitea con el primer paso.

## Abrir

1. `git status` y `git fetch`; con la **rama destino** (`config.md` § Rama destino; `main` si no la
   declara) limpia y actualizada, `git switch -c <slug> <destino>`. La rama sale **de la destino**,
   no de `main`. **Nunca se trabaja sobre la destino ni sobre `main`**: la guardia de git bloquea
   esos commits.
2. `presencia.py marca --repo R --tarea <slug> --evento abrir`. En Toggl, nada.
3. Si el trabajo sale de `pendientes.md`, la entrada se queda ahí hasta el cierre.

## Ejecutar

Los pasos se encadenan **sin preguntar por el siguiente**. **Al empezar cada paso**, Claude relee su
fila y usa ese skill y ese contexto; **al terminarlo**, marca «Hecho» con dónde se ve (`✓ commit
a1b2c3`) y pone al día «Estado». Los commits en la rama son **puntos de guardado** y no piden nada.
Un desvío del plan, una línea en «Notas».

**Si el trabajo se detiene sin cerrarse** —lo decide el usuario, un bloqueo, falta una decisión o se
acaba la sesión—, se anota en `pendientes.md` (`modo-pendientes.md`) **sin preguntar**, con el
motivo, y se dice en una línea. La rama queda viva y con lo hecho commiteado.

## Cerrar

Informa en 2–3 líneas con **dónde verlo** —la rama, el preview, capturas si es visual, los commits
por paso— y pide el visto bueno: **el merge y el push los desbloquea solo el mensaje del usuario
«apruebo el merge»** (la guardia de git del plugin). Ni un encargo previo («complétala») ni el plan
aprobado lo sustituyen. Sin él, el trabajo se queda commiteado en su rama y se espera. Con él,
anuncia la cadena en una línea y ejecútala sin pausas:

0. **Plan:** todos los pasos con «Hecho». Si falta alguno, no es un cierre: es `A medias`.
1. **Tiempo de Claude:** `marca --evento cerrar`, `tramos` y `asentar` (`tarea/references/ciclo.md`).
2. **Historial:** la entrada en `tareas/historial/AAAA-MM.md` (`archivado.md`); el comentario
   enlaza el plan. Si el trabajo venía de `pendientes.md`, la entrada sale de ahí.
3. **Lo que queda:** lo que el trabajo dejó abierto va a `pendientes.md` (decidido) o a
   `por-revisar.md` (idea sin decidir), y se dice en una línea.
4. **Commit** en la rama: lo resuelto, el historial y `pendientes.md`, juntos.
5. **Merge a la rama destino** y **push** a `origin`. Si el push falla, se dice y la destino queda
   mergeada en local.

**Si la destino no es `main`** (por ejemplo `preview`), el cierre termina ahí. **Pasar de la destino
a `main` es otro acto**, con su propio «apruebo el merge», fuera de toda tarea.

**Tres frenos, y solo esos, detienen la cadena:** la destino sucia o desactualizada al mergear; un
conflicto de merge (muestra qué archivos chocan y espera); cambios sin relación con el trabajo al
commitear (pregunta si van o se quedan fuera).

**Impacto documental:** con el merge hecho, busca en el diff de la rama (`git diff --name-only
<destino>@{1}...`) señales de documentación corta. **Sin señal, silencio total.** Con señal:
`impacto-documental.md`.

Después **para**: puedes sugerir lo siguiente (de `pendientes.md`), no empezarlo.
