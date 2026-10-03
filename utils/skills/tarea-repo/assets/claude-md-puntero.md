<!-- Bloque para pegar en el CLAUDE.md del proyecto anfitrión. No copia reglas: la de ramas la
     impone la guardia de git del plugin utils, y el detalle vive en los skills. -->

## Tareas: `tareas/`

- **`tareas/historial/AAAA-MM.md`** — lo cerrado y lo descartado, con su porqué. **Es la mejor fuente
  de contexto sobre por qué el código está como está**: empieza por ahí antes de proponer cambios
  grandes.
- **`tareas/pendientes.md`** — lo decidido que Claude aún no hace. **`tareas/por-revisar.md`** — lo
  anotado sin decidir. El plan de cada trabajo es el del modo plan (`~/.claude/plans/`), con su tabla de pasos.
- **`tareas/config.md`** — la rama destino, las áreas y las reglas del repo.

Las tareas del usuario están en Toggl y las lleva él. Ramas, merge y cierre: los aplica la guardia de
git y los detalla el skill `tarea-repo` (plugin `utils`).
