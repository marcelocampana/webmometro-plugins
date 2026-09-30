# El ciclo de una tarea, en detalle

`C=…/tarea/scripts/cola.py`, `P=…/tarea/scripts/presencia.py`. `R` es el nombre del repo, o
`sin-repo` para un proyecto sin repo (las marcas antiguas con `suelta` siguen valiendo).

## Crear

- **Proyecto:** el del repo actual (su `tareas/toggl.md`), o el que corresponda por cliente
  («Webmómetro › Administración»). Si no existe, se propone crearlo en una línea; si ningún cliente
  encaja, se ofrece crear uno. **Los proyectos se crean públicos**: los privados son de pago (402).
- **Nombre:** verbo + objeto concreto + ámbito, en una línea. Corto: en la vista por fecha, lo que no
  cabe se corta.
- **Área:** una de las que lista el `toggl.md` del repo (o una nueva, que se añade ahí con visto
  bueno). Va como **etiqueta** (`tag_ids`; `tags list` da los ids, y la que falte se crea con `tags
  create` antes) **y** en la primera línea de la descripción, `Área: <área>`.
- **Descripción:** tras la línea del área, qué se espera y el contexto que haga falta. Las
  dependencias («necesita X») van aquí o en las notas: deciden el orden.
- **Asignada al usuario**, con `estimated_mins` si hay base (desde el historial del repo,
  `tarea-repo/references/estimacion.md`); sin base, sin estimación y se dice.
- Un lote de tareas relacionadas va en **una** llamada (`tasks bulk-create`); una tarea con las
  subtareas del usuario, en dos: la tarea y después las subtareas con su `parent_task_id`. Los pasos
  de Claude no se crean en Toggl: van al plan.
- Al crear varias, se suma su estimación y se dice («suman ~2h 40m»).

## Abrir

`P marca --evento abrir` y el estado a In Progress en Toggl. Si el usuario empieza algo que no
existe, se crea antes (una llamada más). Con `P sesion`, si la sesión continua pasa de `sesion_min`
(90), una línea: «Llevas 2h 10m seguidas; toca una pausa». No bloquea nada.

**Varias abiertas a la vez** se permite (una llamada mientras se factura), y se avisa en una línea:
el tiempo de Claude va a la que se abrió después, y el tuyo cuenta una vez (`balance`).

## Qué va a Toggl

**Solo lo tuyo**: tus tareas, tus subtareas, sus estados y el tiempo que cronometras tú con la app
de Toggl —subtareas, reuniones, llamadas—. **Nada de Claude va a Toggl**: ni sus pasos (van al plan)
ni su tiempo, que `P asentar` escribe en su registro local
(`~/Obsidian/Global/claude/registro-tiempo/<nombre>-AAAA-MM.md`), un archivo por mes: **con repo,
lleva el nombre del repo; sin repo, el del proyecto de Toggl**. El repo es el de los archivos que
toca, no el de la carpeta donde se abrió la sesión. Por eso una tarea sin repo se marca con su
proyecto: `P marca --repo sin-repo --tarea ID --evento crear --proyecto "<nombre en Toggl>"`. `P tramos`
sigue dando tu tiempo como `duracion` y el de Claude como `claude`, para el historial; «Verificar tu
tiempo» (`tarea`) contrasta el tuyo con el Mac.

## Cerrar

En este orden, dentro de la misma cadena y sin pregunta aparte:

0. **Antes de nada:** una subtarea del usuario abierta o un paso del plan sin hacer frenan el cierre;
   se dice cuál y la tarea sigue abierta.
1. `P marca --repo R --tarea ID --evento cerrar`.
2. `P tramos --repo R --tarea ID`: devuelve `duracion` (tu tiempo, para el historial), `descontado`,
   `coste`, `vence` y `claude` (total, `con_usuario` y `solo`, para la columna Claude del historial).
3. `P asentar`: el tiempo de Claude desde el último asiento —el de esta tarea y el que hizo sin tarea
   en cualquier repo— al registro local. Idempotente; el agente de launchd también lo corre una vez al
   día.
4. `tasks bulk-patch` con el estado Done. Una llamada: **es la única escritura del cierre en Toggl.**
5. `C invalidar`.

**El cálculo lo hace el script, no el modelo**: las mismas marcas dan siempre los mismos tramos. Claude no
usa cronómetro: Toggl admite uno solo por persona, y es el del usuario.

## Imprevistos

Si `P resumen` del día muestra a Claude trabajando en un repo sin tarea abierta más de
`imprevisto_min` (30), se dice en una línea y se ofrece crear la tarea (etiqueta `imprevisto`, y su
`abrir` con `--hora` de cuando empezó de verdad). Su tiempo no se pierde: `asentar` lo registra igual,
con tarea `—`.

## Si Toggl falla

La parte local y la de git se hacen igual —el tiempo de Claude nunca dependió de Toggl—, y se dice
qué estado quedó sin cambiar. `tarea-repo --toggl` reconcilia los estados después. **Con 402 por límite**, se
avisa y no se reintenta en bucle. Cada escritura del MCP pide un código de confirmación: lo resuelve
el skill, porque lo que dijo el usuario ya lo cubre.
