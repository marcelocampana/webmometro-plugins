<!-- task-flow: umbral 40000 chars · holgura 70% · última revisión 2026-08-20 -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Inicio | Nota |
| :--: | --- | --- | --- | --- | --- |
| 1 | Alinear el contenido bajo «Sigue leyendo» con el diseño original | Componentes | Pendiente | — | — |

---

## General

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| Pendiente | Separar las reglas de prosa editorial de la clase de tema | — | — | — | La prosa va a una clase neutra; en la de tema solo queda el acento. |

**Cerradas en esta sección: ~1h 50m** · 1 archivada en [historial](historial/2026-07.md)

---

## Componentes

Cambios que viven en los componentes compartidos y por tanto **alcanzan a todas las páginas a la vez**.

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| Pendiente | Alinear el contenido bajo «Sigue leyendo» con el diseño original | — | — | — | Afecta a dos páginas a la vez: el bloque vive en `RelatedCard`. |
| ✅ Completada | Convertir el índice móvil en un desplegable | 2026-07-19 18:27 | 2026-07-19 19:02 | 35m | Desplegable pegajoso con `UCollapsible` en vez de la tira con scroll. Trampa: el `class` del call site se pierde sin raíz única (`inheritAttrs: false`). [detalle](historial/2026-07.md#convertir-el-indice-movil-en-un-desplegable) |

**Cerradas en esta sección: 35m**

---

**Estados:** `Pendiente` (anotada) · `🔵 En curso` (rama creada, una a la vez) · `Pausada` (detenida por tiempo) · `Bloqueada` (detenida por una dependencia; requiere Nota) · `✅ Completada`. Solo `🔵 En curso` y `✅ Completada` llevan icono, y va pegado al texto. El comentario íntegro de cada tarea cerrada vive en `historial/AAAA-MM.md`; en la tabla queda su resumen y el enlace. El flujo completo lo gobierna el skill `task-flow`.
