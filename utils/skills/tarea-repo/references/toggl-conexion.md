# Conectar un repo con Toggl (`--toggl`)

Toggl 2.0 registra la realidad —cuánto duró cada tarea, de qué cliente— y `tareas/` la intención.
**La conexión es opcional por repo**: sin marcador, el skill funciona exactamente como siempre.

Se usa el MCP `toggl-focus` (`@togglhq/mcp`). Si sus herramientas no están en la sesión, se dice en
una línea y se sigue sin Toggl; nunca se bloquea una operación de tareas por eso.

## El marcador

Una línea al inicio de `tareas.md`, junto al del umbral:

```markdown
<!-- tarea: toggl · proyecto 3967672 «Webmómetro» · cliente 88123 «Webmómetro» -->
```

Es lo que dice que el repo está conectado, a qué proyecto van sus tareas y qué formato usan sus
tablas (`formato-tablas.md`, variante conectada). **Solo se escribe con visto bueno.**

## Descubrir cliente y proyecto, al vuelo

No se configura por adelantado. La primera vez que haga falta —crear o abrir una tarea en un repo
sin marcador, o `--toggl`—, se busca y se **propone en una línea**:

1. `projects list` con el nombre del repo. Si hay un proyecto que encaja:
   «Esta tarea parece del proyecto X (cliente Y). ¿Lo uso?»
2. Si no hay proyecto: «No hay proyecto para este repo. ¿Creo X? ¿De qué cliente?», con los clientes
   de `clients list`. **Si ningún cliente encaja, ofrece crear uno.**
3. O dejar el repo sin conectar: se respeta y no se vuelve a preguntar en la sesión.

Con la respuesta se crea lo que falte y se escribe el marcador. **Los proyectos se crean públicos**:
los privados son de pago en el plan gratuito (error 402).

**Una tarea de otro proyecto** que el del repo se dice al crearla («esta es de ODC, no de este
repo») y su `project_id` va solo en Toggl; el marcador no cambia.

## Configuración global

`~/Github/AI-kit/config/context/toggl.md` (o `TOGGL_CONFIG`), desde `tarea/assets/toggl.esqueleto.md`:
espacio de trabajo, etiqueta de imprevistos y umbrales. Si no existe, se ofrece crearla; hasta
entonces rigen los valores por defecto. **Se edita a mano**: el skill solo la lee.

## Migrar un repo al formato conectado

Al conectar un repo que ya tiene tareas, se pasa al formato sin columnas de tiempo
(`modo-actualizacion.md`, fila «Conexión con Toggl»). En una pasada y con un solo visto bueno:

1. Crear en Toggl **todas las filas abiertas en una llamada** (`tasks bulk-create`): nombre,
   `project_id`, etiqueta de su sección, `estimated_mins` desde `Coste` y, si hay `Vence`,
   `end_date` con `start_date` = hoy (**Toggl rechaza una sin la otra**).
2. Escribir `<!-- toggl:id -->` pegado al texto de cada celda `Tarea`, en `## Ahora` y en su sección.
3. Anotar `Coste` y `Vence` en el registro local (`presencia.py marca --evento crear`), que es de
   donde los lee el cierre.
4. Quitar las columnas de tiempo de `tareas.md`. **El historial no se toca**: conserva todas.
5. Escribir el marcador.

## Reconciliar

Si Toggl no respondía en un cierre, o una sesión se cortó, `presencia.py tramos` sigue teniendo lo
pendiente: `--toggl` en un repo ya conectado **envía lo que falte** (registros sin marca `enviado`,
estados que no coinciden) y lo dice en una línea. No reescribe lo ya enviado.

## Hallazgos de la API (prueba del 26-09-2026)

| Hecho | Consecuencia |
| --- | --- |
| Un solo cronómetro por persona: iniciar uno detiene el otro | No se usan cronómetros en vivo (`toggl.md`) |
| Registros superpuestos de la misma persona: se aceptan | Dos tareas en paralelo cuentan las dos |
| `time-entries stop` del MCP falla (422, formato de la hora) | No se usa |
| Las tareas no traen URL | El enlace es `<!-- toggl:id -->` |
| Cada cambio pide un código de confirmación (dos invocaciones) | Lo resuelve el skill: el visto bueno del usuario ya lo cubre |
| Límite: ~30 consultas por hora | Todo va en bloque; ninguna operación pasa de 2 |
