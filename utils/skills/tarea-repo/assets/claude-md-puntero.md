<!-- Bloque para pegar en el CLAUDE.md del proyecto anfitrión.
     Deja el proyecto trabajable incluso si el plugin no está instalado. -->

## Cómo avanzamos: Toggl y `tareas/`

**Los pendientes viven en Toggl**, en el proyecto que enlaza `tareas/toggl.md`: una sola lista para
todos los proyectos, que también se edita a mano. En el repo queda la memoria:

- **`tareas/toggl.md`** — el proyecto de Toggl, las áreas del repo con su ámbito y las reglas propias.
- **`tareas/historial/AAAA-MM.md`** — lo cerrado, con el comentario íntegro de cada tarea. **Es la
  mejor fuente de contexto sobre por qué el código está como está**: empieza por ahí antes de proponer
  cambios grandes.
- **`tareas/auditoria.md`** — hallazgos de una revisión completa por áreas, bajo petición.

Reglas irrenunciables:

1. **Una tarea, una rama.** Se comprueba que `main` está limpia y actualizada y se ramifica desde ahí;
   **nunca se trabaja sobre `main`**.
2. **Un plan de varios pasos es una tarea principal con los pasos como subtareas.** Los pasos se
   encadenan sin pedir confirmación; se confirma solo el cierre de la principal.
3. **Se completa esa tarea y se para.** Al cerrar se pregunta una sola vez; con el visto bueno se
   encadenan el tiempo en Toggl, el historial, el commit y el merge a `main` sin pausas —salvo `main`
   sucia o desactualizada, un conflicto o cambios ajenos a la tarea—. Sugerir la siguiente sí,
   empezarla no.

Nada se crea en Toggl sin visto bueno, y la IA no reordena la cola del usuario. El flujo completo lo
gobiernan los skills `tarea` y `tarea-repo` (plugin `utils`).
