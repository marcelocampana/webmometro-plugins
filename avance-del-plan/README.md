# Avance del plan

Mod de Claude Code (un plugin de *function hooks*) que muestra en qué paso va el plan de la rama en
curso.

- **Barra de estado:** `Plan 4/11 · sigue: <paso>`, o `listo para cerrar` con todo hecho.
- **`/plan`:** abre un panel con cada paso ✓ hecho (con su evidencia), ▸ en curso o · pendiente, y
  la línea «Espera de ti».
- **Se actualiza** al abrir la sesión, cada vez que Claude edita un plan y tras un `git switch`,
  `checkout`, `merge` o `commit`.

Lee el plan del modo plan, en `~/.claude/plans/`, cuya primera línea nombra el repo y la rama en
curso (`<!-- tarea: plan · repo <repo> · rama <rama> … -->`), y su tabla `## Pasos`, columna
«Hecho», que lleva el skill `tarea-repo` del plugin `utils`. Los planes anteriores a utils 6.1, en
`tareas/planes/` del repo, se siguen leyendo. Sin plan
para la rama, no muestra nada. Solo lee: no escribe en ningún archivo.

Usa `$.state.get/set` en vez de `atom`/`update`: el validador de algunas versiones del CLI rechaza
estos últimos aunque el motor los acepte.
