<!-- Bloque para pegar en el CLAUDE.md del proyecto anfitrión.
     Deja el proyecto trabajable incluso si el plugin no está instalado. -->

## Cómo avanzamos: Toggl y `tareas/`

**Los pendientes viven en Toggl**, en el proyecto que enlaza `tareas/toggl.md`: una sola lista para
todos los proyectos, que también se edita a mano. En el repo queda la memoria:

- **`tareas/toggl.md`** — el proyecto de Toggl, la **rama destino** (a la que vuelve cada tarea;
  `main` si no se declara), las áreas del repo con su ámbito y las reglas propias.
- **`tareas/historial/AAAA-MM.md`** — lo cerrado, con el comentario íntegro de cada tarea. **Es la
  mejor fuente de contexto sobre por qué el código está como está**: empieza por ahí antes de proponer
  cambios grandes.
- **`tareas/auditoria.md`** — hallazgos de una revisión completa por áreas, bajo petición.
- **`tareas/por-revisar.md`** — la bandeja: lo anotado sin decidir. Solo guarda; revisar es otro
  paso, que puede crear una tarea tuya en Toggl, delegarla a Claude o descartarla.
- **`tareas/para-claude.md`** — lo que una revisión delegó a Claude. Nunca va a Toggl.

Reglas irrenunciables:

1. **Una tarea, una rama.** Se comprueba que la rama destino está limpia y actualizada y se ramifica
   desde ahí; **nunca se trabaja sobre la destino ni sobre `main`**.
2. **La tarea es el objetivo del usuario; el plan es de Claude.** Se planifica con el usuario: los pasos
   de Claude (con su skill y su contexto) van al plan, `tareas/planes/`, y no a Toggl; lo que le toca
   al usuario va como subtareas, que cronometra él. Aprobado el plan, los pasos se encadenan sin pedir
   confirmación. **Toggl es solo del usuario**: el tiempo de Claude va a su registro local
   (`~/Obsidian/global/claude/registro-tiempo/`), nunca a Toggl.
3. **Se completa esa tarea y se para.** Los commits en la rama de la tarea son puntos de guardado y no
   piden confirmación; **el merge a la rama destino sí, siempre, una vez y después de ver el
   resultado** —ni «complétala» ni el plan aprobado la sustituyen—. Con ese visto bueno se encadenan
   el estado en Toggl, el tiempo de Claude a su registro, el historial, el commit, el merge y el push sin pausas —salvo la destino sucia
   o desactualizada, un conflicto o cambios ajenos a la tarea—. Si la destino no es `main`, pasar a
   `main` es otro acto con su propia aprobación. Sugerir la siguiente tarea sí, empezarla no.

Nada se crea en Toggl sin visto bueno, y la IA no reordena la cola del usuario. El flujo completo lo
gobiernan los skills `tarea` y `tarea-repo` (plugin `utils`).
