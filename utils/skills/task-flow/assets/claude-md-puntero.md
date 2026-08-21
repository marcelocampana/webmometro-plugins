<!-- Bloque para pegar en el CLAUDE.md del proyecto anfitrión.
     Deja el proyecto trabajable incluso si el plugin no está instalado. -->

## Cómo avanzamos: `tareas/`

El trabajo se organiza en cuatro piezas dentro de `tareas/`:

- **`tareas.md`** — la cola real, siempre limpia: `## Ahora` más solo las secciones con trabajo activo confirmado por el usuario. Su tabla `## Ahora` es la prioridad, **y la determina el usuario**; sus filas son punteros a la tarea, que vive en la sección de su área. Lo completado se archiva al cerrar, no vive aquí.
- **`revisar.md`** — bandeja de lo que aparece de paso o se quiere mirar más adelante. Nada de aquí está priorizado.
- **`auditoria.md`** — hallazgos de una revisión completa por áreas, bajo petición.
- **`secciones.md`** — catálogo de secciones (nombre y ámbito), sin tablas de tareas; persiste aunque una sección se quede sin trabajo activo. Es un catálogo abierto, no la lista cerrada de lo que puede existir.

Tres reglas irrenunciables:

1. **La siguiente tarea es la primera fila de `## Ahora` que no esté `Bloqueada`** — no «la primera pendiente leyendo de arriba abajo».
2. **Una tarea, una rama, un commit.** Se comprueba que `main` está limpia y actualizada y se ramifica desde ahí; **nunca se trabaja sobre `main`**.
3. **Se completa esa tarea y se para.** Al cerrar se pregunta una sola vez si queda terminada; con el visto bueno se encadenan el cierre de la fila, el commit y el merge a `main` sin pausas —salvo que `main` esté sucia/desactualizada, el merge tenga conflictos, o aparezcan cambios sin relación con la tarea, ahí sí se detiene y pregunta—. Sugerir la siguiente sí, empezarla no.

Nada entra a ninguna lista sin visto bueno, y la IA no escribe en `tareas.md` por iniciativa propia: para eso están las otras dos.

El flujo completo —los movimientos del cierre, los estados, el cálculo de tiempos— lo gobierna el skill `task-flow` (plugin `utils`).
