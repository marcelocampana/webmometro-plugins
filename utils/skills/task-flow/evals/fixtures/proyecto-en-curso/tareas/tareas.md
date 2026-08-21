# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Inicio | Nota |
| :--: | --- | --- | --- | --- | --- |
| 1 | Resolver el hardcodeo del tema antes de añadir el segundo cluster | General | Bloqueada | — | Espera el segundo cluster: sin un tema real no hay con qué probar el mapa. |
| 2 | Alinear el contenido bajo «Sigue leyendo» con el diseño original | Componentes | Pendiente | — | — |

---

## General

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| Bloqueada | Resolver el hardcodeo del tema antes de añadir el segundo cluster | — | — | — | Hace falta un mapa `cluster → clase de tema`; hoy la clase está fija en el `<div>` raíz de las dos páginas. |

**Cerradas en esta sección: ~1h 50m** · 1 archivada

---

## Componentes

Cambios que viven en los componentes compartidos y por tanto **alcanzan a todas las páginas a la vez**. Una fila aquí evita duplicar la tarea en cada página y contar su intervalo dos veces.

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| Pendiente | Alinear el contenido bajo «Sigue leyendo» con el diseño original | — | — | — | Afecta a dos páginas a la vez: el bloque vive en `RelatedCard`. Contrastar contra los mockups sección por sección. |

**Cerradas en esta sección: 35m** · 1 archivada

---

**Estados:**

- `Pendiente` — anotada.
- `🔵 En curso` — rama creada; una a la vez.
- `Pausada` — detenida por tiempo.
- `Bloqueada` — detenida por una dependencia; requiere Nota.
- `✅ Completada` — cerrada y archivada. Solo `🔵 En curso` y `✅ Completada` llevan icono, pegado al texto.

Al cerrarse, una tarea sale de este archivo hacia `historial/AAAA-MM.md`. El flujo completo —una
tarea/una rama/un commit, la confirmación de cierre en cadena y el cálculo de tiempos— lo gobierna
el skill `task-flow`.
