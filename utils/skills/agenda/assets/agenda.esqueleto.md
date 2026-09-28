<!-- agenda: config · la leen los skills `agenda`, `plan-semanal` y `balance` (plugin utils) · vive fuera de todo repo -->

# Agenda

Registro de repos. **Este archivo se edita a mano**; los skills solo lo leen, salvo cuando el usuario
les pide crearlo o cambiarlo.

Ubicación esperada: `~/Github/AI-kit/config/context/agenda.md`. La variable `AGENDA_CONFIG` tiene
prioridad sobre ella.

## Repos

**El orden de esta tabla es la prioridad entre proyectos** cuando una tarea no tiene día: la agenda y
el plan de la semana la usan para desempatar. El proyecto de Toggl de cada repo sale de su
`tareas/toggl.md`; `balance` lee de aquí dónde está cada historial.

| Etiqueta | Ruta |
| --- | --- |
| clientes | ~/Github/Projects/cliente-principal |
| plugins | ~/Github/AI-kit/plugins/webmometro-plugins |

- **La etiqueta es corta y reconocible**, sin ruta.
- **La ruta apunta al repo**, no a su `tareas/`.
- **Un repo archivado se borra de aquí.**
- `~` se expande, y una **ruta relativa se resuelve respecto a este archivo**.

## Capacidad

La jornada vive en Toggl (horario de trabajo del usuario): `capacities` la da por día. **Solo si
hace falta otra cifra**, se pone aquí una tabla `| Día | Capacidad |` y manda sobre la de Toggl; la
agenda lo dice cada vez que la usa.

## Lo que no va aquí

Estados, estimaciones o fechas de ninguna tarea: viven en Toggl, una sola vez.
