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
el tiempo de proyecto cuenta las dos; el del usuario, una vez (`balance`).

## Qué va a Toggl

**Solo el trabajo de Claude**, con la etiqueta `claude` (`etiqueta_claude` de la configuración
global; si falta, se crea una vez con `tags create` y su id se anota ahí). Su proyecto es el del repo
cuyos archivos toca, no el de la carpeta donde se abrió la sesión. **El tiempo del usuario lo
cronometra él** con la app de Toggl —sus subtareas, reuniones, llamadas—; `P tramos` lo sigue dando
como `duracion` para el historial, y «Verificar tu tiempo» (`tarea`) lo contrasta con el Mac.

## Cerrar

En este orden, dentro de la misma cadena y sin pregunta aparte:

0. **Antes de nada:** una subtarea del usuario abierta o un paso del plan sin hacer frenan el cierre;
   se dice cuál y la tarea sigue abierta.
1. `P marca --repo R --tarea ID --evento cerrar`.
2. `P tramos --repo R --tarea ID`: devuelve `registros` (lo que va a Toggl: el trabajo de Claude en
   el repo mientras la tarea estuvo abierta, ya con `tag_ids`; vacío si `fuente` es `ninguno`),
   `duracion` (tu tiempo, para el historial), `descontado`, `coste`, `vence` y `claude` (total, `con_usuario` y
   `solo`).
3. `time-entries bulk-create` con esos `registros` y `task_id` = ID (fechas RFC3339 con zona). Una
   llamada, **en el mismo cierre**. Si la API no acepta `tag_ids` al crear, se ponen justo después con
   `bulk-patch` sobre los ids creados. Sin registros, se salta.
4. `tasks bulk-patch` con el estado Done. Una llamada.
5. `P marca --evento enviado`.
6. **Lo que Claude trabajó sin tarea**: `P sin-tarea --hasta <ahora>` da, por repo, los tramos de
   Claude en que no había ninguna tarea de ese repo abierta, con el `proyecto_toggl` de su
   `tareas/toggl.md`. Van en una llamada `time-entries bulk-create` sin `task_id` y con
   `project_id` (también con la etiqueta); después `P sin-tarea --enviado --hasta <el mismo ahora>`.
   Un repo sin `proyecto_toggl` no se envía y se dice en una línea. La rutina nocturna que hacía esto
   mismo cada noche es opcional y está pausada (`assets/presencia-instalacion.md`, paso 3).
7. `C invalidar`.

**El cálculo lo hace el script, no el modelo**: las mismas marcas dan siempre los mismos tramos. Claude no
usa cronómetro: Toggl admite uno solo por persona, y es el del usuario.

## Imprevistos

Si `P resumen` del día muestra a Claude trabajando en un repo sin tarea abierta más de
`imprevisto_min` (30), se dice en una línea y se ofrece crear la tarea (etiqueta `imprevisto`, y su
`abrir` con `--hora` de cuando empezó de verdad). Su tiempo no se pierde: va con `sin-tarea`.

## Si Toggl falla

La parte local y la de git se hacen igual, y se dice qué quedó sin enviar. Las marcas siguen en el
registro: el siguiente cierre, o `tarea-repo --toggl`, envía lo pendiente. **Con 402 por límite**, se
avisa y no se reintenta en bucle. Cada escritura del MCP pide un código de confirmación: lo resuelve
el skill, porque lo que dijo el usuario ya lo cubre.
