# Toggl y el tiempo de Claude, en detalle

`C=…/tarea/scripts/cola.py`, `P=…/tarea/scripts/presencia.py`. `R` es el nombre del repo, o
`sin-repo` para un proyecto sin repo (las marcas antiguas con `suelta` siguen valiendo).

## Crear las tareas que el usuario eligió

Solo las que eligió de «Esto te toca a ti» o las que dicta él («crea una tarea: facturar a X»).

- **Proyecto:** el del repo actual (el marcador de su `tareas/config.md`, o `toggl.md` en un repo sin
  migrar), o el que corresponda por cliente («Webmómetro › Administración»). Si no existe, se
  propone crearlo en una línea. **Los proyectos se crean públicos**: los privados son de pago (402).
- **Nombre:** verbo + objeto concreto + ámbito, en una línea, tal como iba en la lista.
- **Área:** una de las del `config.md` del repo. Va como **etiqueta** (`tag_ids`; `tags list` da
  los ids, y la que falte se crea con `tags create` antes) **y** en la primera línea de la
  descripción, `Área: <área>`.
- **Descripción:** tras la línea del área, qué se espera y una línea de origen: `Sale de:
  <repo> · ~/.claude/plans/<nombre>.md` (o la conversación, si no hay plan).
- **Asignada al usuario** (`user_account_id`), con `estimated_mins` = el tiempo que decía la lista.
  Sin fecha, salvo que el usuario la diga: **planificar es suyo**. Si la dice, `start_date` y
  `end_date` juntas (Toggl rechaza una sin la otra).
- **Subtarea o suelta:** si el trabajo salió de una tarea del usuario en Toggl, `parent_task_id` de
  esa tarea (`C tarea ID` la confirma). Si no, suelta.
- Todas en **una** llamada (`tasks bulk-create`), validada antes con `dry_run`. Después
  `C invalidar` y una línea: «Creadas 2 en Toggl (suman ~40m)».

Claude no cambia el estado de ninguna tarea de Toggl: abrir, pausar y cerrar los hace el usuario.

## El tiempo de Claude: marcas locales

El trabajo de Claude se identifica por el **slug** de su plan (`completar-bien-el-trabajo`), no por
un id de Toggl.

| Momento | Local |
| --- | --- |
| **Abrir** | `P marca --repo R --tarea <slug> --evento abrir` |
| **Pausar / retomar** | `--evento pausar` / `retomar` |
| **Cerrar** | `--evento cerrar`, `P tramos --repo R --tarea <slug>` (para el historial) y `P asentar` |

- `P tramos` devuelve `duracion` (el tiempo del usuario con la tarea abierta), `descontado` y
  `claude` (total, `con_usuario` y `solo`) para la columna Claude del historial.
- `P asentar` escribe el tiempo de Claude desde el último asiento —el de esta tarea y el que hizo
  sin tarea en cualquier repo— en `~/Obsidian/Global/claude/registro-tiempo/<nombre>-AAAA-MM.md`:
  con repo, el nombre del repo; sin repo, el del proyecto (`marca --proyecto "<nombre>"`). El repo
  es el de los archivos que toca, no el de la carpeta donde se abrió la sesión. Es idempotente; el
  agente de launchd también lo corre una vez al día.
- Con `P sesion`, si la sesión continua del usuario pasa de `sesion_min` (90), una línea: «Llevas
  2h 10m seguidas; toca una pausa». No bloquea nada.

**El cálculo lo hace el script, no el modelo**: las mismas marcas dan siempre los mismos tramos.
Claude no usa cronómetro: Toggl admite uno solo por persona, y es el del usuario.

## Trabajo sin plan

Si Claude trabaja en un repo sin una tarea abierta, su tiempo no se pierde: `asentar` lo registra
igual, con tarea `—`. No se ofrece crear nada en Toggl.

## Si Toggl falla

Lo local y lo de git se hacen igual, y se dice qué no se pudo crear. **Con 402 por límite**, se avisa
y no se reintenta en bucle. Cada escritura del MCP pide un código de confirmación: lo resuelve el
skill, porque la elección del usuario ya lo cubre.
