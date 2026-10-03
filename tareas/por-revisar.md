<!-- tarea: por-revisar · lo anotado sin decidir · lo escriben Claude (de paso) y el usuario (a mano) -->

# Por revisar

Lo que surgió y aún no se decide: aquí solo se guarda. **Revisar es otro paso** (a mano o con
Claude, `tarea-repo --revisar`), y cada entrada sale de aquí cuando se decide: tarea tuya en Toggl
(si te ocupa tiempo), delegada a Claude (`pendientes.md`) o descartada con su motivo en el historial.
Nada de este archivo está en Toggl.

Una entrada por línea: `- **Título** · Área · origen (tarea, commit o archivo) · AAAA-MM-DD — por qué`.
Sin repo (`~/Obsidian/Global/por-revisar.md`), una sección `## <Proyecto>` por proyecto de Toggl.

<!-- - **Corregir el desplegable del menú en móvil** · General · `AppHeader.vue:88` · 2026-09-29 — se corta en iPhone SE; visto al cerrar la tarea 16642210 -->
- **Obligar a decidir los pendientes antiguos** · utils · plan `completar-bien-el-trabajo` · 2026-10-02 — una entrada de `pendientes.md` con más de 3–4 semanas obliga a hacerla o descartarla con motivo; se dejó para después del congelamiento
- **La guardia revisa el commit antes de que corra el `git add` de la misma línea** · utils · `utils/hooks/guardia_git.py` · 2026-10-03 — `git add tareas/x.md && git commit` en una línea se bloquea aunque solo toque la bandeja; hoy basta separarlo en dos comandos
- **Migrar a utils 6 los cuatro repos de la agenda** · utils · revisión del plugin, sesión del 2026-10-03 · 2026-10-03 — CDZ, ODC y odc-clusters siguen con `tareas.md` y webmometro-web-reports con `toggl.md`; la captura se salta los tres primeros, y la rama `feat/revista-roc` de odc-clusters no figura en ningún sitio (`tarea-repo --migrar` en cada uno)
