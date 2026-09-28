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
- Un lote de tareas relacionadas va en **una** llamada (`tasks bulk-create`); una principal con sus
  pasos, en dos: la principal y después los pasos con su `parent_task_id`.
- Al crear varias, se suma su estimación y se dice («suman ~2h 40m»).

## Abrir

`P marca --evento abrir` y el estado a In Progress en Toggl. Si el usuario empieza algo que no
existe, se crea antes (una llamada más). Con `P sesion`, si la sesión continua pasa de `sesion_min`
(90), una línea: «Llevas 2h 10m seguidas; toca una pausa». No bloquea nada.

**Varias abiertas a la vez** se permite (una llamada mientras se factura), y se avisa en una línea:
el tiempo de proyecto cuenta las dos; el del usuario, una vez (`balance`).

## Cerrar

En este orden, dentro de la misma cadena y sin pregunta aparte:

1. `P marca --repo R --tarea ID --evento cerrar`.
2. `P tramos --repo R --tarea ID`: devuelve `registros` (los tramos en que la tarea estuvo abierta
   **y** el usuario presente), `duracion`, `descontado`, `coste`, `vence` y `claude` (lo que trabajó
   Claude en la tarea: total, `con_usuario` y `solo`). `claude` no va a Toggl: lo guarda el
   historial del repo.
3. `time-entries bulk-create` con esos `registros` y `task_id` = ID (fechas RFC3339 con zona). Una
   llamada.
4. `tasks bulk-patch` con el estado Done. Una llamada. **En una tarea con pasos**, el último paso y la
   principal van juntos en esta misma llamada.
5. `P marca --evento enviado` y `C invalidar`.

**El cálculo lo hace el script, no el modelo**: las mismas marcas dan siempre los mismos tramos. No
se usa cronómetro: Toggl admite uno solo por persona y dos sesiones en paralelo se lo quitarían.

**Si hay `descontado`**, se dice en la línea de cierre: «descontados 25 min sin actividad; si
estabas, lo mantengo».

## Trabajo fuera del computador

Una reunión presencial o una llamada no deja teclado ni mensajes: la presencia la daría por ausencia.
Por eso, **al cerrar, si `tramos` descuenta más de 10 min en una tarea sin repo**, se pregunta una
sola vez:

> Descontaría 45 min sin actividad en el Mac. ¿Estuviste en la reunión fuera del computador?

- **Sí** → `P tramos … --completo`: se envía el tramo abierto entero.
- **No** → se envía lo medido.

## Registrar después

«Estuve 40 min en una llamada con X» (ya pasó): se crea la tarea si no existe y un registro con esa
duración terminando ahora, o a la hora que diga el usuario. Es tiempo **declarado, no medido**: la
descripción del registro lo dice («declarado») y `balance` no lo usa para calibrar estimaciones.

## Imprevistos

Si `P resumen` del día muestra atención en un repo sin tarea abierta, se dice: «llevas 40 min en
este proyecto sin tarea abierta». Menos de `imprevisto_min` (30) y sin commit: un registro suelto en
Toggl (`create-taskless`), en el proyecto del repo, etiqueta `imprevisto`. Con commit o si pasa del
tope: es una tarea normal con esa etiqueta, y su `abrir` lleva `--hora` de cuando empezó de verdad.

## Si Toggl falla

La parte local y la de git se hacen igual, y se dice qué quedó sin enviar. Las marcas siguen en el
registro: el siguiente cierre, o `tarea-repo --toggl`, envía lo pendiente. **Con 402 por límite**, se
avisa y no se reintenta en bucle. Cada escritura del MCP pide un código de confirmación: lo resuelve
el skill, porque lo que dijo el usuario ya lo cubre.
