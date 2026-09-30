---
name: tarea
description: >
  Sistema de tareas del usuario, con Toggl 2.0 como única lista de pendientes para todos sus
  proyectos. Crea, abre, pausa y cierra tareas en Toggl, guarda el paso a paso de Claude en el plan
  de la tarea (no en Toggl), asienta el tiempo de Claude en su registro local (nunca en Toggl, que es
  solo del usuario), lleva la bandeja de lo anotado sin decidir (`por-revisar.md`) y lo delegado a
  Claude (`para-claude.md`), y verifica los registros que el usuario cronometra contra su actividad en
  el Mac. Úsalo cada vez que el usuario hable de una tarea o de su
  trabajo pendiente: "qué sigue", "empiezo X", "anota esto", "haz lo siguiente", "listo, ya está",
  "pausa", "qué tengo abierto", "crea una tarea", "tengo que facturar", "estuve en una reunión",
  "terminé la llamada", "verifica mis registros", "¿está bien mi tiempo de hoy?", o cuando pase un archivo o una conversación de la que extraer tareas. Si la
  tarea es de un proyecto enlazado a un repo (su `tareas/toggl.md`), el trabajo además lleva rama,
  commit e historial: esa parte la pone `tarea-repo`. NO lo uses para la vista de hoy (eso es
  `agenda`), para planificar la semana (`plan-semanal`) ni para revisarla (`balance`), ni para TODOs
  efímeros de la sesión.
argument-hint: "[lo que el usuario quiere hacer]"
metadata:
  version: 5.0.0
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
| Otras etiquetas | La transversal: `imprevisto`. La bandeja ya no es una etiqueta: es `por-revisar.md` |

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
| **Cerrar** | 1 llamada: estado Done | `--evento cerrar`, `P tramos` (para el historial), `P asentar` |

`R` es el nombre del repo, o `sin-repo` si el proyecto no tiene repo. El detalle de cada momento
—campos, formato de los registros, trabajo fuera del computador, tiempo declarado, varias abiertas,
si Toggl falla— está en `references/ciclo.md`.

**¿Tiene repo?** Lo dice el proyecto. Si el `tareas/toggl.md` del repo actual enlaza el proyecto de
la tarea, abrir y cerrar llevan además rama, commit, merge e historial: se invoca `tarea-repo` con lo
que dijo el usuario. Si ningún repo lo enlaza, no hay git: **cerrar no pide confirmación aparte**,
«listo» ya lo es. Un repo que aún tiene `tareas/tareas.md` está **sin migrar**: se dice en una línea
y se ofrece `tarea-repo --migrar`.

## La tarea, tus subtareas y el plan de Claude

**Toggl organiza al usuario; el plan organiza a Claude.**

- **La tarea es el objetivo del usuario** («Publicar la landing de láser CO2»): asignada a él, con
  estimación y día. Se planifica con él antes de empezar.
- **Subtareas, solo lo que le toca al usuario** para lograrla: decidir, validar con alguien, hacer
  algo en una consola o fuera del computador. Asignadas a él, con su día. **Las cronometra él** con la
  app de Toggl; Claude no les registra tiempo. Un solo nivel.
- **Los pasos de Claude no van a Toggl.** Van al plan de la tarea, con el skill y el contexto de cada
  paso: en un repo, `tareas/planes/<id>-<slug>.md` (`tarea-repo`); sin repo, en la descripción. El
  plan se aprueba una vez.
- **Se ejecuta de corrido.** Aprobado el plan, los pasos se encadenan sin pedir visto bueno; solo se
  para por un freno real (conflicto, la rama destino sucia, cambios ajenos, algo que es del usuario)
  y, en un repo, **siempre antes del merge**, que lleva la aprobación del usuario tras ver el resultado. **Nunca
  se termina un paso con «¿sigo con el siguiente?»**, y «empieza con el paso 1» arranca la cadena.
- **Al retomar**, el usuario no relee el plan: Claude lo lee y da el estado en 2–3 líneas (cuántos
  pasos van, cuál sigue, qué le toca al usuario).
- **Nada de Claude va a Toggl**: su tiempo lo escribe `P asentar` en
  `~/Obsidian/global/claude/registro-tiempo/<nombre>-AAAA-MM.md` (el nombre del repo; sin repo, el
  del proyecto de Toggl). Toggl es solo tu trabajo.

## La bandeja y lo de Claude

- **Anotar no decide nada.** Lo que surge de paso —un TODO, una idea tuya, algo que el trabajo dejó
  a medias— va a `por-revisar.md`, en una línea y sin frenar. Nada va a Toggl.
- **Revisar es otro paso**, a mano o con Claude, y puede dejar la entrada, crearla en Toggl como
  tarea tuya (con visto bueno), delegarla a Claude (pasa a `para-claude.md`) o descartarla.
- **Lo de Claude** se ejecuta cuando lo pides («haz lo de Claude»), con su plan, y nunca va a Toggl.
- **Dónde:** en un repo, en su `tareas/` (lo lleva `tarea-repo`); sin repo, en
  `~/Obsidian/global/por-revisar.md` y `para-claude.md`, una sección por proyecto, siguiendo
  `tarea-repo/references/modo-revisar.md` y `modo-claude.md` sin la parte de git.

## Verificar tu tiempo

«Verifica mis registros de hoy»: se leen por el MCP (`time-entries list`) los registros del período
(sin los antiguos de la etiqueta `claude`, anteriores a utils 5.0.0), y `P verificar --entradas <json>` los compara con la actividad del
Mac. Una línea por registro, solo con lo que no cuadra: «Revisar el copy: 1h 30m registrados, 1h 05m
activo; siguió 20m tras tu última actividad». Se dicen sus límites una vez: lo hecho fuera del
computador parece inactividad, y dos trabajos en las mismas aplicaciones no se separan. **Solo lee:**
corregir un registro pide el sí del usuario, registro por registro.

## Consultar

«Qué tengo abierto», «qué sigue»: `C leer --vista hoy` más `P abiertas`, en una sola lista. Para la
vista de todos los proyectos con la capacidad del día, se remite a `agenda`.

## Reglas invariantes

1. **Toggl es la única lista de tus pendientes, y solo tuya.** Lo anotado sin decidir va a
   `por-revisar.md` y lo delegado a Claude a `para-claude.md`; nada de eso, ni el tiempo de Claude,
   va a Toggl.
2. **Se lee por la copia**, nunca con `tasks list` crudo.
3. **Crear proyectos o clientes en Toggl pide visto bueno**; crear, abrir y cerrar tareas se hace con
   lo que el usuario dijo.
4. **Tiempo medido y tiempo declarado no se mezclan**: el declarado se marca como tal.
5. **Si Toggl falla**, las marcas locales quedan y el siguiente cierre lo envía; se dice en una línea.

## Infraestructura

Vive aquí y no cambia de ruta, porque el agente del Mac y el gancho apuntan a ella:
`scripts/presencia.py` (presencia, marcas, tramos, el registro de tiempo de Claude, plan), `scripts/cola.py` (la copia de la cola:
usa la sesión del conector y nunca la renueva) y `assets/` (instalación del registro y del gancho, y
la configuración global de Toggl).

## Idioma

Español neutro. Los nombres de las tareas, tal cual.
