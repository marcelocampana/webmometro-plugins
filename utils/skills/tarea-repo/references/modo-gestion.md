# Gestión: crear, abrir y cerrar una tarea de repo

La tarea vive en Toggl y su ciclo (estados, marcas, registros de tiempo) es de
`tarea/references/ciclo.md`. Aquí va solo lo que añade el repo.

## Crear

**Ninguna tarea se crea sin contexto del proyecto** (`contextualizacion.md`), y **toda sugerencia se
ancla en algo verificable** —un archivo, una deuda declarada, un hallazgo de la conversación—; sin
ancla, no se propone. Se propone y se espera, también para lo que dicta el usuario.

- **Enunciado:** verbo + objeto concreto + ámbito, en una línea (`redaccion-tareas.md`).
- **Área:** una de las que lista `tareas/toggl.md`, por el ámbito del cambio; va en la primera línea
  de la descripción (`Área: Informes`). Un área nueva se propone y, con el sí, se añade al `toggl.md`.
- **Coste:** lo propone el skill desde el historial (`estimacion.md`) y lo confirma el usuario. Sin
  base, se dice y va sin estimación.
- **Vence:** solo si hay un compromiso externo real.
- **Un plan de varios pasos que Claude ejecuta de corrido es una tarea principal con los pasos como
  subtareas**, no una tarea por paso (`tarea`, «Tareas con pasos»).

La posición en la cola la decide el usuario: se recomienda con motivo, no se reordena solo.

## Abrir

1. `git status` y `git fetch`; con `main` limpia y actualizada, `git switch -c <rama>` con un nombre
   que describa la tarea. **Nunca se trabaja sobre `main`**, y si un merge quedó pendiente, **avisa
   de que `main` está desactualizada y decide antes de empezar**.
2. En Toggl y en el registro local, lo de `tarea` (estado In Progress, `P marca --evento abrir`).

Si hay otra tarea de repo en curso, se dice en una línea antes de abrir.

## Cerrar

**Una sola confirmación.** Informa de lo hecho en 2-3 líneas y pide el visto bueno; con él, anuncia
la cadena en una línea («Cierro, commiteo y mergeo a `main`») y ejecútala sin pausas:

1. **Toggl:** los pasos de cierre de `tarea/references/ciclo.md` (tramos, registros, Done, `enviado`).
2. **Historial:** la entrada en `tareas/historial/AAAA-MM.md`, con los datos de `tramos`
   (`archivado.md`).
3. **Commit** en la rama de la tarea: lo resuelto y la entrada del historial, juntos.
4. **Merge a `main`**, sin pedir otro visto bueno.

**En una tarea con pasos**, cada paso cierra su subtarea (pasos 1 y, si se quiere, 3) sin preguntar;
el historial, la confirmación y el merge son de la principal.

**Tres frenos, y solo esos, detienen la cadena:** `main` sucia o desactualizada al mergear; un
conflicto de merge (muestra qué archivos chocan y espera, no lo resuelvas solo); cambios sin relación
con la tarea al commitear (pregunta si van o se quedan fuera).

**Impacto documental:** con el merge hecho, busca en el diff de la rama (`git diff --name-only
main@{1}...`) señales de documentación corta —estructura, un archivo que el README enumera, un
comando, una dependencia, una convención de `CLAUDE.md`—. **Sin señal, silencio total.** Con señal:
`impacto-documental.md`.

Al cerrar, **ofrece** para la bandeja (`por-revisar`) lo que el trabajo dejó pendiente: propone y
espera. Después **para**: puedes sugerir la siguiente, no empezarla.

## Consultar

«Qué sigue», «qué hay bloqueado»: `cola.py leer --vista hoy` (o `pendientes --proyecto <ID>` para
este repo), solo lectura. Avisa si el orden tiene un conflicto real (la primera depende de otra que
va después). **No abras el historial para esto.**
