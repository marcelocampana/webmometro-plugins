---
name: tarea
description: >
  Sistema de tareas del usuario y de Claude. Toggl 2.0 es del usuario y lo lleva él a mano (crea,
  planifica, cronometra y cierra); Claude solo crea en Toggl las tareas que el usuario elige de la
  sección «Esto te toca a ti» de un plan, y lee sus registros para verificarlos contra su actividad
  en el Mac. El trabajo de Claude vive en su plan y su rama; lo que queda sin hacer, en
  `pendientes.md`, y lo anotado sin decidir, en `por-revisar.md`. Asienta el tiempo de Claude en su
  registro local (nunca en Toggl). Úsalo cuando el usuario hable de sus tareas o de lo pendiente:
  "esto te toca a ti", "agrega la 1 y la 3 a Toggl", "crea una tarea", "tengo que facturar", "qué
  tengo en Toggl", "qué quedó pendiente", "anota esto", "verifica mis registros", "¿a qué hora dejé
  de trabajar?", "¿está bien mi tiempo de hoy?", o cuando pase un archivo o una conversación de la
  que extraer tareas. Si el trabajo es de un repo con `tareas/`, la rama, el plan, el historial y
  los pendientes los pone `tarea-repo`. NO lo uses para la vista de hoy (eso es `agenda`), para
  planificar la semana (`plan-semanal`) ni para revisarla (`balance`), ni para TODOs efímeros de
  la sesión.
argument-hint: "[lo que el usuario quiere hacer]"
metadata:
  version: 6.0.1
---

# Tareas (tarea)

**Toggl es del usuario y lo lleva él, a mano**: crea sus tareas, planifica, corre y para el timer, y
cierra. Así sus tareas le son propias. Claude toca Toggl en dos casos y solo en esos:

1. **Crear las tareas que el usuario eligió** de «Esto te toca a ti».
2. **Leer sus registros** para verificarlos, cuando lo pide.

Claude **no** abre, pausa ni cierra tareas, no cambia estados, no planifica ni escribe nada de su
propio trabajo en Toggl.

`C=utils/skills/tarea/scripts/cola.py` y `P=utils/skills/tarea/scripts/presencia.py` (en el repo del
plugin o en su caché).

## Qué va a Toggl

**Lo que hace el usuario y le ocupa tiempo**: lo que tiene que meter en su día o su semana y que
quiere medir. **Una decisión no va**: se pide en el momento («necesito tu decisión sobre X») y, si
queda abierta, se anota en `pendientes.md`, sección `Espera tu decisión`. El trabajo de Claude
tampoco va: vive en su plan y su rama.

## «Esto te toca a ti»

Claude planifica como siempre. **Al final de su plan**, si hay algo que no puede hacer él y que le
ocupa tiempo al usuario, agrega una sección corta:

```text
## Esto te toca a ti
1. Validar el copy con la clínica (~30 min) — necesita su visto bueno
2. Subir el sitemap en Search Console (~10 min) — Claude no tiene acceso
```

No es un formato aparte ni pide nada: el usuario elige («la 1 y la 2 a Toggl») cuando quiera, y
Claude crea **solo esas**, en una llamada (`references/ciclo.md`, «Crear»):

- Si el trabajo salió de una tarea que el usuario ya tenía en Toggl, van como **subtareas** de esa.
- Si no, como **tareas sueltas**, con una línea de origen en la descripción.

Lo mismo vale para lo que surja durante el trabajo o al cerrar.

## Leer Toggl

`python3 $C leer --vista hoy|semana|pendientes [--proyecto ID]` y `python3 $C tarea ID`, cuando el
usuario pregunta qué tiene o hace falta la tarea madre. **Nunca `tasks list` del MCP**: cada tarea
cruda pesa ~2.000 caracteres. Tras crear, `python3 $C invalidar`. Con código 3 (sesión caducada),
una consulta cualquiera por el MCP la renueva y se reintenta; con 4, se dice y se sigue sin Toggl.

## Lo de Claude: plan, rama y pendientes

- **En un repo con `tareas/`**, el trabajo de Claude lleva rama, plan (`tareas/planes/<slug>.md`),
  historial y `pendientes.md`: lo pone `tarea-repo`.
- **Sin repo**, lo pendiente va a `~/Obsidian/Global/pendientes.md` y lo anotado sin decidir a
  `~/Obsidian/Global/por-revisar.md`, una sección por proyecto, siguiendo
  `tarea-repo/references/modo-pendientes.md` y `modo-revisar.md` sin la parte de git.
- **Nada sale sin rastro**: lo pendiente sale al historial, hecho o descartado con su motivo.
- **El tiempo de Claude** va a su registro local: `P marca` al abrir y cerrar, con el slug como id,
  y `P asentar` (`references/ciclo.md`). Nunca a Toggl.

## Verificar tu tiempo

«Verifica mis registros de hoy», «¿a qué hora dejé de trabajar?»: se leen por el MCP
(`time-entries list`) los registros del período (sin los antiguos de la etiqueta `claude`), y
`P verificar --entradas <json>` los compara con la actividad del Mac. Una línea por registro, solo
con lo que no cuadra: «Revisar el copy: 1h 30m registrados, 1h 05m activo; siguió 20m tras tu última
actividad». Se dicen sus límites una vez: lo hecho fuera del computador parece inactividad, y dos
trabajos en las mismas aplicaciones no se separan. **Solo lee:** corregir un registro pide el sí del
usuario, registro por registro.

## Reglas invariantes

1. **Toggl es del usuario.** Claude solo crea lo que el usuario eligió, y nada de su propio trabajo.
2. **Se lee por la copia**, nunca con `tasks list` crudo.
3. **Crear proyectos o clientes en Toggl pide visto bueno.**
4. **Tiempo medido y tiempo declarado no se mezclan**: el declarado se marca como tal.

## Infraestructura

Vive aquí y no cambia de ruta, porque el agente del Mac y el gancho apuntan a ella:
`scripts/presencia.py` (presencia, marcas, tramos, el registro de tiempo de Claude, plan),
`scripts/cola.py` (la copia de la cola: usa la sesión del conector y nunca la renueva) y `assets/`
(instalación del registro y del gancho, y la configuración global de Toggl).

## Idioma

Español neutro. Los nombres de las tareas, tal cual.
