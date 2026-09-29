---
name: agenda
description: >
  Compone la **vista diaria del usuario con todos sus proyectos**: lee la cola de Toggl (la copia
  local de `tarea`) y la capacidad del día en Toggl, y responde qué toca hoy y si cabe en el tiempo
  disponible. Úsalo cuando el usuario pregunte "qué me toca hoy", "mi agenda", "qué tengo pendiente
  en todos los proyectos", "cuánto me cabe hoy", "cómo voy", o cuando una rutina programada pida el
  resumen diario. Avisa de lo vencido, de lo que vence hoy, de varias tareas abiertas a la vez y de
  las tareas sin estimación. **Solo lee: nunca escribe en Toggl ni en ningún repo, ni reordena
  nada.** NO lo uses para abrir, cerrar, crear, priorizar ni mover una tarea —eso es `tarea`—, ni
  para planificar la semana (`plan-semanal`).
argument-hint: "[--hoy | --dia AAAA-MM-DD | --config]"
metadata:
  version: 2.0.1
---

# Agenda diaria (agenda)

El día del usuario no es un proyecto: es la suma de todos. Toggl ya los tiene en una sola lista; este
skill responde a una sola pregunta —**qué toca hoy y si cabe en el tiempo que hay**— y no hace nada
más.

## Solo lee. Esa es la garantía, no un detalle

**No escribe en Toggl, ni en ningún repo, ni reordena nada.** El único archivo que puede crear o
modificar es su propia configuración, y solo si el usuario lo pide. Es lo que le permite correr
desatendido desde una rutina: lo peor que puede pasar es un informe incompleto. Cuando algo hay que
cambiar —una estimación que falta, un orden que no cuadra—, **lo dice y remite a `tarea`**.

## Paso 0 · Qué hay

```bash
C=…/tarea/scripts/cola.py; P=…/tarea/scripts/presencia.py
python3 "$C" leer --vista hoy --json          # en curso, vencidas y las de hoy
python3 "$C" leer --vista pendientes --json   # para el relleno, solo si hace falta
python3 "$P" resumen --desde HOY --hasta HOY  # horas trabajadas y atención sin tarea
```

- **La cola, por la copia**, nunca con `tasks list` del MCP. Con código 3 (sesión caducada), una
  consulta cualquiera por el MCP la renueva y se reintenta; con código 4 o sin MCP (una rutina
  desatendida), se usa la copia que haya y se dice su edad. Sin copia, la agenda lo dice y termina.
- **La capacidad del día**, de Toggl: `capacities get-computations` para hoy (`group: users`,
  `unit: day`, `include_task_estimates: true`, el usuario del perfil). Da `working_minutes` (la
  jornada) y `estimated_minutes` (lo asignado y fechado para hoy). **Una llamada.** Si la
  configuración de la agenda aún trae `## Capacidad`, esa cifra manda y se dice en una línea.
- **El orden entre proyectos**, de la configuración (`${AGENDA_CONFIG:-~/Github/AI-kit/config/context/agenda.md}`):
  el orden de su tabla `## Repos`. El proyecto de cada repo sale de la primera línea de su
  `tareas/toggl.md`. Los proyectos sin repo van después. Sin configuración, se dice y se sigue sin
  ese orden (solo por día y prioridad).

## Paso 1 · Componer la vista

`references/vista-diaria.md`: qué entra y en qué orden, cómo se llena la capacidad, qué avisos se dan
y la plantilla. **Cabe en una pantalla.** Lo que no entra en la capacidad no se lista, se cuenta.

## Cuando la dispara una rutina

**Nadie está delante**, así que **no pregunta: informa y termina**. Si falta la configuración, si la
copia es vieja o si Toggl no responde, eso *es* la salida de ese día. La rutina se monta fuera del
repo, como tarea programada del usuario.

## Reglas invariantes

1. **No escribe en Toggl ni en ningún repo**, ni siquiera para corregir un error evidente.
2. **No reordena nada**, ni propone reordenar sin decir qué tarea y a dónde.
3. **No inventa una estimación.** Una tarea sin ella se cuenta aparte, nunca se estima aquí.
4. **No abre tareas.** Sugerir por dónde empezar sí; empezar, no.
5. **Una fuente caída no aborta la agenda**; se reporta y se sigue.

## Idioma

Español neutro. Los nombres de las tareas y de los proyectos, **tal cual están en Toggl**.
