---
name: plan-semanal
description: >
  Planifica la semana del usuario cruzando todos sus repos: propone qué tarea va cada día según su
  capacidad y las estimaciones, y con su visto bueno escribe el plan en Toggl 2.0 (fecha y
  estimación de cada tarea) y guarda la versión original para medir después plan contra realidad.
  Úsalo cuando el usuario diga "planifica la semana", "planifiquemos", "qué hago esta semana",
  "arma mi semana", "replanifica", "cambia el plan", "mueve X al jueves", o cuando una rutina
  programada pida la planificación del lunes. Si un proyecto de la agenda aún no está en Toggl,
  ofrece conectarlo en ese momento. **Escribe en Toggl, nunca reordena `## Ahora` ni crea filas en
  ninguna lista de tareas por su cuenta**: el orden de cada repo lo decide el usuario con `tarea`.
  NO lo uses para la vista de hoy (eso es `agenda`), para abrir o cerrar tareas (eso es `tarea`) ni
  para revisar la semana pasada (eso es `balance`).
argument-hint: "[--replanificar]"
metadata:
  version: 1.0.0
---

# Planificar la semana (plan-semanal)

`tarea` ordena cada repo; `agenda` dice qué toca hoy; `balance` mira hacia atrás. Este skill hace
lo que faltaba: **decidir de antemano qué día va cada cosa**, con el menor esfuerzo posible para el
usuario. **Claude prepara la propuesta; el usuario solo corrige y aprueba.**

El sistema sigue funcionando igual si un lunes no se planifica: la agenda ordena por `## Ahora`
como siempre y `balance` dice que no hubo plan. Planificar es una mejora, no un requisito.

## Qué es el plan

| | Dónde vive | Qué es |
| --- | --- | --- |
| **Plan** | Toggl: `start_date` = `end_date` = el día; `estimated_mins` | Una tarea con día y estimación, **sin registros de tiempo** |
| **Realidad** | Toggl: registros de tiempo; y el registro de presencia | Lo que `tarea` mide al cerrar |
| **Plan original** | `presencia.py plan` (local) | La versión del lunes, porque Toggl solo guarda la última |

**Por día, no por hora.** Una hora exacta obliga a replanificar cada vez que la mañana cambia; un
día aguanta. El orden dentro del día lo sigue dando `## Ahora`.

## Paso 0 · Qué hay

1. **Configuración:** la de `agenda` (registro de repos y capacidad por día) y la global de Toggl
   (`toggl.md`). Sin la de `agenda`, se dice y se ofrece crearla; no se adivinan repos.
2. **Semana:** la que empieza el lunes próximo, o la actual si es lunes o se pide replanificar.
   Las fechas salen de `date`, nunca de la memoria.
3. **Por repo**, en el orden del registro:
   - **Conectado a Toggl** (marcador `<!-- tarea: toggl … -->`): candidatas = filas de `## Ahora`
     en su orden, y después las `Pendiente` de sus secciones. Una consulta a Toggl (`tasks list`
     del proyecto) da estimación, fechas y estado.
   - **No conectado:** se ofrece conectarlo en ese momento, en una línea («cdz no está en Toggl:
     ¿lo conecto para planificarlo?»). Con el sí, se sigue `tarea/references/toggl-conexion.md`
     en ese repo; con el no, sus tareas salen al pie como «sin planificar».
4. **Arrastre:** tareas con día de la semana pasada que no están `Done`. Van primero.
5. **Planificado a mano:** tareas que el usuario ya fechó en Toggl para esta semana se respetan tal
   cual, aunque no estén en `## Ahora`.

Consultas a Toggl: una por repo conectado, más una para escribir. **No se lee el historial.**

## Paso 1 · Proponer

`references/propuesta.md`: cómo se llena cada día, qué hacer con lo que no tiene estimación, los
avisos y la plantilla. **Una pantalla**, una tabla por semana, y una sola pregunta al final.

## Paso 2 · Escribir, con visto bueno

Con el sí, y con las correcciones que el usuario haya dicho:

1. **Toggl, una llamada:** `tasks bulk-patch` con `start_date` y `end_date` = el día, y
   `estimated_mins` si el usuario dio o corrigió una estimación. Las tareas que salen del plan
   pierden su fecha (`null`).
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

1. **No reordena `## Ahora` ni escribe filas** en ninguna lista. Si el plan choca con el orden de un
   repo, lo dice y remite a `tarea` allí.
2. **No inventa estimaciones.** Sin estimación, se pregunta en la misma propuesta (una sola vez,
   para todas) o la tarea va al pie como «sin estimar».
3. **No escribe sin visto bueno**, ni en Toggl ni en local.
4. **La capacidad es la declarada** en la configuración de `agenda`: horas de trabajo, no de reloj.
5. **Sin planificar también funciona**: nada en `tarea`, `agenda` ni `balance` depende de que exista
   un plan.

## Idioma

Español neutro. Tareas y repos, tal cual se llaman. Días en palabras («martes 29»), horas a la
chilena (`1h 20m`).
