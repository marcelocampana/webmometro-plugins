# Lo de Claude: `para-claude.md`

Lo que una revisión delegó a Claude vive en **`tareas/para-claude.md`** (sin repo,
`~/Obsidian/global/para-claude.md`). **No está en Toggl ni va a estar**: Toggl es solo del usuario.
Si no existe, se crea desde `assets/para-claude.esqueleto.md` al delegar la primera entrada.

## Ejecutar

Cuando el usuario lo pide —«haz lo de Claude», «haz lo del menú»—, nunca por iniciativa propia:

1. **Id y plan.** El id es `pc-<slug>` (el título en minúsculas y con guiones). El plan va a
   `tareas/planes/pc-<slug>.md` desde `assets/plan.esqueleto.md` (marcador `toggl:—`), con los pasos,
   su skill y su contexto. **Se aprueba una vez**, como cualquier plan; si el usuario lo pidió ya
   concreto («hazlo»), esa orden lo cubre.
2. **Abrir.** `presencia.py marca --repo R --tarea pc-<slug> --evento abrir` y la ceremonia de
   `modo-gestion.md` (rama destino limpia, rama nueva). En Toggl, nada.
3. **Ejecutar** el plan de corrido, sin preguntar por el siguiente paso.
4. **Cerrar** con la misma cadena de `modo-gestion.md` y la misma regla: **el merge espera la
   aprobación del usuario, dada tras ver el resultado.** Cambia solo la parte de Toggl: en vez del
   estado Done, `marca --evento cerrar`, `tramos` (para el historial) y `presencia.py asentar`. La
   entrada sale de `para-claude.md` en el mismo commit y queda en el historial, con `pc-<slug>` como
   id.

**Sin repo** no hay rama ni historial: se marca con `--repo sin-repo`, y al cerrar la entrada pasa a
`## Hechas` del archivo global, con la fecha.

## Consultar

«Qué tiene Claude pendiente»: la lista de `para-claude.md`, tal cual, más las globales si se pide
todo. `agenda` la cuenta en una línea y no la suma a la capacidad del usuario.
