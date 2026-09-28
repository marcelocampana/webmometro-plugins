---
name: plan-semanal
description: >
  Planifica la semana del usuario con todos sus proyectos de Toggl: propone qué tarea va cada día
  según la jornada y las estimaciones, y con su visto bueno escribe el plan en Toggl 2.0 (día y
  estimación de cada tarea) y guarda la versión original para medir después plan contra realidad.
  Úsalo cuando el usuario diga "planifica la semana", "planifiquemos", "qué hago esta semana",
  "arma mi semana", "replanifica", "cambia el plan", "mueve X al jueves", o cuando una rutina
  programada pida la planificación del lunes. Lee la cola por la copia local de `tarea`. **Solo
  escribe días y estimaciones, con visto bueno: nunca crea, cierra ni reordena tareas.** Si un repo
  de la agenda aún no está migrado a Toggl, ofrece migrarlo. NO lo uses para la vista de hoy (eso es
  `agenda`), para abrir o cerrar tareas (eso es `tarea`) ni para revisar la semana pasada (eso es
  `balance`).
argument-hint: "[--replanificar]"
metadata:
  version: 2.0.2
---

# Planificar la semana (plan-semanal)

`tarea` lleva la lista en Toggl; `agenda` dice qué toca hoy; `balance` mira hacia atrás. Este skill hace
lo que faltaba: **decidir de antemano qué día va cada cosa**, con el menor esfuerzo posible para el
usuario. **Claude prepara la propuesta; el usuario solo corrige y aprueba.**

El sistema sigue funcionando igual si un lunes no se planifica: la agenda ordena por prioridad y
el orden de los proyectos y `balance` dice que no hubo plan. Planificar es una mejora, no un requisito.

## Qué es el plan

| | Dónde vive | Qué es |
| --- | --- | --- |
| **Plan** | Toggl: `start_date` = `end_date` = el día; `estimated_mins` | Una tarea con día y estimación, **sin registros de tiempo** |
| **Realidad** | El registro de presencia (tu tiempo); Toggl guarda el trabajo de Claude por proyecto | Lo que `tarea` mide al cerrar |
| **Plan original** | `presencia.py plan` (local) | La versión del lunes, porque Toggl solo guarda la última |

**Por día, no por hora.** Una hora exacta obliga a replanificar cada vez que la mañana cambia; un
día aguanta. El orden dentro del día lo da la prioridad de cada tarea.

## Paso 0 · Qué hay

1. **Configuración:** la de `agenda` (el orden de los repos, que desempata entre proyectos) y la
   global de Toggl (`toggl.md`). Sin la de `agenda`, se dice y se planifica solo por vence y
   prioridad; no se adivinan repos.
2. **Semana:** la que empieza el lunes próximo, o la actual si es lunes o se pide replanificar.
   Las fechas salen de `date`, nunca de la memoria.
3. **Candidatas:** `cola.py leer --vista pendientes --json` —todos los proyectos, con o sin repo, en
   una sola lectura—, sin la bandeja (`por-revisar`) ni lo bloqueado. **Nunca `tasks list` del MCP.**
   Las tareas principales no se planifican: se planifican sus pasos, y la principal toma la fecha del
   último.
4. **Capacidad:** `capacities get-computations` de la semana (una llamada): la jornada de cada día y
   lo ya estimado en él. Si la configuración de `agenda` trae `## Capacidad`, esa manda.
5. **Arrastre:** tareas con día de la semana pasada que no están hechas. Van primero.
6. **Planificado a mano:** lo que el usuario ya fechó en Toggl para esta semana se respeta tal cual.
7. **Un repo del registro sin `tareas/toggl.md`** (sin migrar o sin enlazar): se ofrece, en una
   línea, `tarea-repo --migrar` allí; mientras, sus tareas no se ven.

Consultas a Toggl: una lectura (por la copia), una de capacidad y una para escribir. **No se lee el
historial.**

## Paso 1 · Proponer

`references/propuesta.md`: cómo se llena cada día, qué hacer con lo que no tiene estimación, los
avisos y la plantilla. **Una pantalla**, una tabla por semana, y una sola pregunta al final.

## Paso 2 · Escribir, con visto bueno

Con el sí, y con las correcciones que el usuario haya dicho:

1. **Toggl, una llamada:** `tasks bulk-patch` con `start_date` y `end_date` = el día, y
   `estimated_mins` si el usuario dio o corrigió una estimación; **en la misma llamada**, cada tarea
   principal toma la fecha del último de sus pasos. Las tareas que salen del plan pierden su fecha
   (`null`). Después, `cola.py invalidar`.
2. **Plan original, local:** `presencia.py plan guardar --semana AAAA-Www` con la lista
   `{repo, tarea, nombre, dia, estimado_min}`. La primera versión de la semana es la que
   `balance` compara; replanificar añade versiones sin pisar la original.
3. **Una línea de cierre:** «Semana planificada: 9 tareas, ~14h de 20h. Guardado en Toggl».

Toggl pide un código de confirmación por cambio: lo resuelve el skill, porque el visto bueno del
usuario ya lo cubre.

## Replanificar (`--replanificar`)

A media semana: se parte del plan **vigente** (`plan leer --vigente`), se mueve lo pedido o lo que
quedó atrás, y se escribe igual que en el Paso 2. Es normal y no es un fracaso: `balance` distingue
lo que se replanificó de lo que se abandonó.

## Reglas invariantes

1. **Solo escribe fechas y estimaciones** en Toggl, con visto bueno: no crea, cierra ni reordena
   tareas. Si el plan choca con una dependencia, lo dice.
2. **No inventa estimaciones.** Sin estimación, se pregunta en la misma propuesta (una sola vez,
   para todas) o la tarea va al pie como «sin estimar».
3. **No escribe sin visto bueno**, ni en Toggl ni en local.
4. **La capacidad es la jornada de Toggl** (o la de la configuración de `agenda` si la trae): horas
   de trabajo, no de reloj.
5. **Sin planificar también funciona**: nada en `tarea`, `agenda` ni `balance` depende de que exista
   un plan.

## Idioma

Español neutro. Tareas y repos, tal cual se llaman. Días en palabras («martes 29»), horas a la
chilena (`1h 20m`).
