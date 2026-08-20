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

<!-- Al cerrar la primera tarea de la sección, añade bajo la tabla:
**Cerradas en esta sección: 1h 30m** -->

---

**Estados:** `Pendiente` (anotada) · `🔵 En curso` (rama creada, una a la vez) · `Pausada` (detenida por tiempo) · `Bloqueada` (detenida por una dependencia; requiere Nota) · `✅ Completada`. Solo `🔵 En curso` y `✅ Completada` llevan icono, y va pegado al texto. El comentario íntegro de cada tarea cerrada vive en `historial/AAAA-MM.md`; en la tabla queda su resumen y el enlace. El flujo completo lo gobierna el skill `task-flow`.
