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
| ✅ Completada | Corregir el enlace del logo a la página de inicio | 2026-08-17 17:55 | 2026-08-18 09:55 | ~1h 50m | El logo se movió a `public/images/` y pasó a `NuxtImg`. Ningún asset debe quedar en la raíz de `public/`: no cae bajo ningún prefijo del proxy. |

**Cerradas en esta sección: ~1h 50m**

---

## Componentes

Cambios que viven en los componentes compartidos y por tanto **alcanzan a todas las páginas a la vez**. Una fila aquí evita duplicar la tarea en cada página y contar su intervalo dos veces.

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| Pendiente | Alinear el contenido bajo «Sigue leyendo» con el diseño original | — | — | — | Afecta a dos páginas a la vez: el bloque vive en `RelatedCard`. Contrastar contra los mockups sección por sección. |
| ✅ Completada | Convertir el índice móvil en un desplegable | 2026-08-19 18:27 | 2026-08-19 19:02 | 35m | Sustituye la tira con scroll lateral por un desplegable pegajoso. Se retiró la tira porque lo que queda fuera de pantalla no se descubre. El `class="lg:hidden"` del call site **se pierde** si el componente no tiene raíz única: se arregla con `inheritAttrs: false` + `v-bind="$attrs"`. |

**Cerradas en esta sección: 35m**

---

**Estados:** `Pendiente` (anotada) · `🔵 En curso` (rama creada, una a la vez) · `Pausada` (detenida por tiempo) · `Bloqueada` (detenida por una dependencia; requiere Nota) · `✅ Completada`. Solo esos dos llevan icono. El flujo completo —una tarea/una rama/un commit, las tres confirmaciones de cierre y el cálculo de tiempos— lo gobierna el skill `task-flow`.
