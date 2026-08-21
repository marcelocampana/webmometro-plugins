<!-- task-flow: umbral 40000 chars · holgura 70% · última revisión {{AAAA-MM-DD}} -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Inicio | Nota |
| :--: | --- | --- | --- | --- | --- |

---

## {{Sección}}

{{Una línea opcional: qué abarca esta sección y qué queda fuera. Se omite si el título ya lo dice.}}

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |

<!-- Al cerrar la primera tarea de la sección, añade bajo la tabla (el total real vive en
     secciones.md; esto es el reflejo mientras la sección siga activa aquí):
**Cerradas en esta sección: 1h 30m** · 1 archivada -->

---

**Estados:**

- `Pendiente` — anotada.
- `🔵 En curso` — rama creada; una a la vez.
- `Pausada` — detenida por tiempo.
- `Bloqueada` — detenida por una dependencia; requiere Nota.
- `✅ Completada` — cerrada y archivada. Solo `🔵 En curso` y `✅ Completada` llevan icono, pegado al texto.

Al cerrarse, una tarea sale de este archivo hacia `historial/AAAA-MM.md` — no queda rastro en la
tabla de su sección. El flujo completo lo gobierna el skill `task-flow`.
