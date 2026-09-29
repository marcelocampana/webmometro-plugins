# Gestión: crear, abrir y cerrar una tarea de repo

La tarea vive en Toggl y su ciclo (estados, marcas, registros de tiempo) es de
`tarea/references/ciclo.md`. Aquí va solo lo que añade el repo.

## Crear

**Ninguna tarea se crea sin contexto del proyecto** (`contextualizacion.md`), y **toda sugerencia se
ancla en algo verificable** —un archivo, una deuda declarada, un hallazgo de la conversación—; sin
ancla, no se propone. Se propone y se espera, también para lo que dicta el usuario.

- **Enunciado:** verbo + objeto concreto + ámbito, en una línea (`redaccion-tareas.md`).
- **Área:** una de las que lista `tareas/toggl.md`, por el ámbito del cambio; va como etiqueta y en la
  primera línea de la descripción (`Área: Informes`). Un área nueva se propone y, con el sí, se añade
  al `toggl.md`.
- **Coste:** lo propone el skill desde el historial (`estimacion.md`) y lo confirma el usuario. Sin
  base, se dice y va sin estimación.
- **Vence:** solo si hay un compromiso externo real.
La posición en la cola la decide el usuario: se recomienda con motivo, no se reordena solo.

## Planificar

La tarea es el objetivo del usuario; antes de ejecutarla se acuerda qué hace falta. Se propone en
una tabla corta y se espera **un** visto bueno, que cubre la ejecución entera y el cierre:

- **Pasos de Claude** → el plan, `tareas/planes/<id>-<slug>.md` desde `assets/plan.esqueleto.md`.
  Cada paso: verbo + resultado revisable, el **skill** y el **contexto** que se leerán antes. Lo
  mecánico (instalar, cargar, desplegar) va dentro del paso al que sirve, no como paso propio.
- **Lo que le toca al usuario** (decidir, validar con alguien, hacer algo en una consola) → subtareas
  en Toggl, con su día; las cronometra él (`tarea/references/ciclo.md`, «Crear»).
- La descripción de la tarea en Toggl añade la línea `Plan: tareas/planes/<archivo>`.

El plan se crea en la rama de la tarea y se commitea con el primer paso. **Al empezar cada paso**,
Claude relee su fila y usa ese skill y ese contexto; **al terminarlo**, marca «Hecho» con dónde se ve
(`✓ commit a1b2c3`, `✓ web/contenido/laser-co2.md`) y pone al día «Estado». Si se aparta del plan,
lo anota en «Notas» en una línea.

**Al retomar** la tarea otro día, se lee el plan y se le da al usuario el estado en 2–3 líneas: cuántos
pasos van, cuál sigue, qué le toca a él. No se le pide releer el plan.

## Abrir

1. `git status` y `git fetch`; con la **rama destino** (la de `tareas/toggl.md` § Rama destino; `main`
   si no la declara) limpia y actualizada, `git switch -c <rama> <destino>` con un nombre que describa
   la tarea. La rama sale **de la destino**, no de `main`: si fueran distintas y saliera de `main`, le
   faltaría lo que ya está en prueba. **Nunca se trabaja sobre la destino ni sobre `main`**, y si un
   merge quedó pendiente, **avisa de que la destino está desactualizada y decide antes de empezar**.
2. En Toggl y en el registro local, lo de `tarea` (estado In Progress, `P marca --evento abrir`).

Si hay otra tarea de repo en curso, se dice en una línea antes de abrir.

## Cerrar

**Los commits en la rama de la tarea son puntos de guardado**: se hacen durante los pasos sin pedir
nada, porque no tocan la rama destino. **El merge a la rama destino, en cambio, siempre lleva la
aprobación del usuario, dada después de ver el resultado.** Ni un encargo previo («complétala», «no
me pidas confirmación») ni el plan aprobado la sustituyen: una autorización dada antes de que el
trabajo exista no certifica que esté bien. Es regla fija, no una opción de `toggl.md`.

**Una sola confirmación.** Informa de lo hecho en 2-3 líneas con **dónde verlo** —la rama, el
preview si lo hay, capturas si es visual, los commits por paso— y pide el visto bueno. Sin él, el
trabajo se queda commiteado en su rama y se espera. Con él, anuncia la cadena en una línea («Cierro,
commiteo, mergeo a `<destino>` y subo») y ejecútala sin pausas:

0. **Plan:** todos los pasos con «Hecho» y ninguna subtarea del usuario abierta; si no, se dice qué
   falta y la tarea no se cierra.
1. **Toggl:** los pasos de cierre de `tarea/references/ciclo.md` (tramos, registros, Done, `enviado`).
2. **Historial:** la entrada en `tareas/historial/AAAA-MM.md`, con los datos de `tramos`
   (`archivado.md`); el comentario enlaza el plan.
3. **Commit** en la rama de la tarea: lo resuelto y la entrada del historial, juntos.
4. **Merge a la rama destino** y **push** a `origin`, sin pedir otro visto bueno. Si el push falla,
   se dice y la destino queda mergeada en local.

**Si la destino no es `main`** (una rama de pruebas como `preview`), el cierre de la tarea termina
ahí. **Pasar de la destino a `main` es otro acto**, con su propia aprobación y fuera de toda tarea,
porque puede llevar varias: se pide cuando el usuario lo dice, nunca como coletilla de un cierre.

**Tres frenos, y solo esos, detienen la cadena:** la destino sucia o desactualizada al mergear; un
conflicto de merge (muestra qué archivos chocan y espera, no lo resuelvas solo); cambios sin relación
con la tarea al commitear (pregunta si van o se quedan fuera).

**Impacto documental:** con el merge hecho, busca en el diff de la rama (`git diff --name-only
<destino>@{1}...`) señales de documentación corta —estructura, un archivo que el README enumera, un
comando, una dependencia, una convención de `CLAUDE.md`—. **Sin señal, silencio total.** Con señal:
`impacto-documental.md`.

Al cerrar, **ofrece** para la bandeja (`por-revisar`) lo que el trabajo dejó pendiente: propone y
espera. Después **para**: puedes sugerir la siguiente, no empezarla.

## Consultar

«Qué sigue», «qué hay bloqueado»: `cola.py leer --vista hoy` (o `pendientes --proyecto <ID>` para
este repo), solo lectura. Avisa si el orden tiene un conflicto real (la primera depende de otra que
va después). **No abras el historial para esto.**
