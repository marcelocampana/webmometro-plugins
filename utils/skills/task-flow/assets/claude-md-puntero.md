<!-- Bloque para pegar en el CLAUDE.md del proyecto anfitrión.
     Deja el proyecto trabajable incluso si el plugin no está instalado. -->

## Cómo avanzamos: `tareas/`

El trabajo se organiza en tres listas dentro de `tareas/`:

- **`tareas.md`** — la cola real. Su tabla `## Ahora` es la prioridad, **y la determina el usuario**; sus filas son punteros a la tarea, que vive en la sección de su área. Una sección por unidad de trabajo estable; las secciones no se reordenan.
- **`revisar.md`** — bandeja de lo que aparece de paso o se quiere mirar más adelante. Nada de aquí está priorizado.
- **`auditoria.md`** — hallazgos de una revisión completa por áreas, bajo petición.

Tres reglas irrenunciables:

1. **La siguiente tarea es la primera fila de `## Ahora` que no esté `Bloqueada`** — no «la primera pendiente leyendo de arriba abajo».
2. **Una tarea, una rama, un commit.** Se comprueba que `main` está limpia y actualizada y se ramifica desde ahí; **nunca se trabaja sobre `main`**.
3. **Se completa esa tarea y se para.** Al cerrar: se confirma que queda cerrada, luego el commit, luego el merge — tres confirmaciones, ninguna supuesta. Sugerir la siguiente sí, empezarla no.

Nada entra a ninguna lista sin visto bueno, y la IA no escribe en `tareas.md` por iniciativa propia: para eso están las otras dos.

El flujo completo —los cinco movimientos del cierre, los estados, el cálculo de tiempos— lo gobierna el skill `task-flow` (plugin `utils`).
