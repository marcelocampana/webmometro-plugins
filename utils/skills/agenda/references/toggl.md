# Repos conectados a Toggl

Un repo está conectado si las primeras líneas de su `tareas.md` llevan el marcador
`<!-- tarea: toggl · proyecto <id> … -->` (`tarea/references/toggl-conexion.md`). Se mira con
`head -5`: no hace falta leer más para saberlo.

## Coste y Vence salen de Toggl

En un repo conectado, `## Ahora` no tiene esas columnas. Cada celda `Tarea` lleva el id pegado al
texto: `Corregir el menú <!-- toggl:16504199 -->`.

- **Una consulta por repo**, no por tarea: `tasks list` del proyecto del marcador, sin las `Done`.
  De cada tarea se toma `estimated_mins` (→ Coste) y `end_date` (→ Vence).
- Se cruza por el id del comentario. **El comentario se quita al mostrar la tarea.**
- Una fila con id que Toggl no devuelve se trata como sin Coste ni Vence, y se dice al pie: «2 filas
  de odc sin datos en Toggl: `tarea --toggl` allí lo reconcilia».
- `estimated_mins` se muestra con el formato de siempre (`45m`, `2h 30m`), sin `~`: en Toggl no queda
  quién lo estimó.

## Horas del día

Del registro de presencia, no de Toggl: `presencia.py resumen --desde HOY --hasta HOY` (el script vive
en `tarea/scripts/`). De ahí salen dos líneas de la vista:

- **«Llevas 2h 40m trabajadas de 4h»**, junto a la capacidad. Es el tiempo del usuario —un minuto
  cuenta una vez aunque haya dos sesiones en paralelo—, no la suma de las tareas.
- **Actividad sin tarea abierta**: si la atención del día en un repo registrado pasa de 15 min y ese
  repo no tiene ninguna `🔵 En curso`, un aviso al pie: «40 min en odc-clusters sin tarea abierta».

## Si Toggl no responde

**La agenda no se cae.** Se lista por orden con el tope de 5 filas y se dice al pie, una vez:
«sin datos de Toggl: no puedo sumar horas de los repos conectados». Lo mismo sin el MCP en la
sesión, que es lo normal en una rutina desatendida sin él. Sin registro de presencia, la línea de
horas del día simplemente no sale.

## Lo que no hace

**No escribe en Toggl**, igual que no escribe en ninguna lista: ni estados, ni registros, ni
reconciliaciones. Si algo no cuadra, lo dice y remite a `tarea --toggl` en ese repo.
