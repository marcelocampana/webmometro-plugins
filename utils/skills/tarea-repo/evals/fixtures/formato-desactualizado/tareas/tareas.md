<!-- task-flow: umbral 40000 chars · holgura 70% · última revisión 2026-06-10 -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Inicio | Nota |
| :--: | --- | --- | --- | --- | --- |
| 1 | Migrar el formulario de contacto a Nuxt UI | Formularios | Pendiente | — | — |

---

## General

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |

---

## Formularios

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| Pendiente | Migrar el formulario de contacto a Nuxt UI | — | — | — | Sustituye el formulario nativo por `UForm` con validación Zod. |

---

**Estados:** `Pendiente` (anotada) · `🔵 En curso` (rama creada, una a la vez) · `Pausada` (detenida por tiempo) · `Bloqueada` (detenida por una dependencia; requiere Nota) · `✅ Completada`. Solo `🔵 En curso` y `✅ Completada` llevan icono, y va pegado al texto. El comentario íntegro de cada tarea cerrada vive en `historial/AAAA-MM.md`; en la tabla queda su resumen y el enlace. El flujo completo lo gobierna el skill `task-flow`.
