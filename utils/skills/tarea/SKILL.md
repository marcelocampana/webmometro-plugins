---
name: tarea
description: >
  Sistema de tareas del usuario, con Toggl 2.0 como única lista de pendientes para todos sus
  proyectos. Crea, abre, pausa y cierra tareas en Toggl, envía en bloque al cerrar el trabajo de
  Claude en cada proyecto (con tarea o sin ella) y mide aparte el tiempo real del usuario frente al
  computador. Úsalo cada vez que el usuario hable de una tarea o de su
  trabajo pendiente: "qué sigue", "empiezo X", "anota esto", "haz lo siguiente", "listo, ya está",
  "pausa", "qué tengo abierto", "crea una tarea", "tengo que facturar", "estuve en una reunión",
  "terminé la llamada", o cuando pase un archivo o una conversación de la que extraer tareas. Si la
  tarea es de un proyecto enlazado a un repo (su `tareas/toggl.md`), el trabajo además lleva rama,
  commit e historial: esa parte la pone `tarea-repo`. NO lo uses para la vista de hoy (eso es
  `agenda`), para planificar la semana (`plan-semanal`) ni para revisarla (`balance`), ni para TODOs
  efímeros de la sesión.
argument-hint: "[lo que el usuario quiere hacer]"
metadata:
  version: 4.3.1
---

# Tareas (tarea)

**Toggl es la única lista de pendientes.** Una sola vista para todos los proyectos, que el usuario
también edita a mano. Cada repo guarda solo lo que ya se hizo y por qué (`tareas/historial/`), que
es lo que le da contexto a Claude; esa parte es de `tarea-repo`.

`C=utils/skills/tarea/scripts/cola.py` y `P=utils/skills/tarea/scripts/presencia.py` (en el repo del
plugin o en su caché).

## Cómo es una tarea en Toggl

| Campo | Qué lleva |
| --- | --- |
| Proyecto | El repo (lo enlaza su `tareas/toggl.md`) o un proyecto sin repo, como «Administración» |
| Etiqueta de área | La del área de la tarea (las áreas del repo están en su `toggl.md`): es lo que se ve y se filtra en Toggl |
| Descripción | 1.ª línea `Área: <área>`, la misma de la etiqueta (respaldo para los scripts); después, qué se espera. La escribe Claude al crear |
| Notas | Comentarios sobre la marcha, del usuario a mano o de Claude mientras trabaja |
| Estado | Todo · In Progress · Blocked · Done |
| `estimated_mins` / `end_date` | El coste y el vence |
| `start_date` = `end_date` | El día planificado (`plan-semanal`) |
| Asignación | Toda tarea real, al usuario: sin eso `capacities` no la cuenta |
| Otras etiquetas | Las transversales: `imprevisto` y `por-revisar` (la bandeja) |

**El área es una etiqueta**, una por tarea, con el nombre exacto del área; si no existe en el espacio
de trabajo, se crea al crear la tarea. Subproyectos, no. El orden: el día entre proyectos, `priority`
dentro del día, `position` dentro del proyecto.

## Leer: siempre por la copia

`python3 $C leer --vista hoy|semana|pendientes [--proyecto ID]` y `python3 $C tarea ID`. **Nunca
`tasks list` del MCP**: cada tarea cruda pesa ~2.000 caracteres. Tras cualquier escritura en Toggl,
`python3 $C invalidar`. Si sale con código 3 (sesión caducada), una consulta cualquiera por el MCP la
renueva y se reintenta; con código 4, se dice y se sigue sin Toggl.

## El ciclo

| Momento | Toggl (MCP) | Local |
| --- | --- | --- |
| **Crear** | 1 llamada: proyecto, descripción, asignación, estimación y, si hay fecha, `start_date` + `end_date` (Toggl rechaza una sin la otra) | `P marca --repo R --tarea ID --evento crear --coste …` |
| **Abrir** | 1 llamada: estado In Progress | `--evento abrir` |
| **Pausar / bloquear / retomar** | 1 llamada: Todo, Blocked o In Progress; lo bloqueado lleva el motivo en las notas | `--evento pausar` / `retomar` |
| **Cerrar** | 2 llamadas: registros de tiempo y estado Done | `--evento cerrar`, `P tramos`, envío, `--evento enviado` |

`R` es el nombre del repo, o `sin-repo` si el proyecto no tiene repo. El detalle de cada momento
—campos, formato de los registros, trabajo fuera del computador, tiempo declarado, varias abiertas,
si Toggl falla— está en `references/ciclo.md`.

**¿Tiene repo?** Lo dice el proyecto. Si el `tareas/toggl.md` del repo actual enlaza el proyecto de
la tarea, abrir y cerrar llevan además rama, commit, merge e historial: se invoca `tarea-repo` con lo
que dijo el usuario. Si ningún repo lo enlaza, no hay git: **cerrar no pide confirmación aparte**,
«listo» ya lo es. Un repo que aún tiene `tareas/tareas.md` está **sin migrar**: se dice en una línea
y se ofrece `tarea-repo --migrar`.

## Tareas con pasos

Cuando un trabajo tiene varios pasos que Claude ejecuta de corrido, es **una tarea principal con los
pasos como subtareas** (`parent_task_id`), no una tarea por paso.

- **Se confirma solo la principal.** Los pasos se encadenan sin pedir visto bueno entre uno y otro:
  cada uno se abre, se cierra y envía su tiempo solo. Pedir confirmación por paso obliga al usuario a
  estar frente a la pantalla. Solo se para por un freno real (conflicto, `main` sucia, cambios ajenos
  o una decisión que es del usuario). **Nunca se termina un paso con «¿sigo con el siguiente?»**, y
  «empieza con el paso 1» arranca la cadena entera, no solo ese paso.
- **La principal va sin asignar y sin estimación**, así no cuenta dos veces en la capacidad; los
  pasos sí llevan las suyas.
- **Su fecha es la del último paso**, para que en la vista por fecha se vean como árbol. Quien mueva
  un paso de día la recalcula en la misma llamada. Si los pasos cruzan de semana, los que quedan
  atrás se ven con la ruta «Paso › Principal»: se acepta.
- **Un solo nivel.** Un paso no tiene subtareas.

## Consultar

«Qué tengo abierto», «qué sigue»: `C leer --vista hoy` más `P abiertas`, en una sola lista. Para la
vista de todos los proyectos con la capacidad del día, se remite a `agenda`.

## Reglas invariantes

1. **Toggl es la única lista.** No se escriben pendientes en ningún markdown.
2. **Se lee por la copia**, nunca con `tasks list` crudo.
3. **Crear proyectos o clientes en Toggl pide visto bueno**; crear, abrir y cerrar tareas se hace con
   lo que el usuario dijo.
4. **Tiempo medido y tiempo declarado no se mezclan**: el declarado se marca como tal.
5. **Si Toggl falla**, las marcas locales quedan y el siguiente cierre lo envía; se dice en una línea.

## Infraestructura

Vive aquí y no cambia de ruta, porque el agente del Mac y el gancho apuntan a ella:
`scripts/presencia.py` (presencia, marcas, tramos, plan), `scripts/cola.py` (la copia de la cola:
usa la sesión del conector y nunca la renueva) y `assets/` (instalación del registro y del gancho, y
la configuración global de Toggl).

## Idioma

Español neutro. Los nombres de las tareas, tal cual.
