<!-- tarea: umbral 40000 chars · holgura 70% · última revisión 2026-08-27 -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Vence | Coste | Nota |
| :--: | --- | --- | --- | --- | --- | --- |
| 1 | Añadir a `agenda` el modo semanal y la calibración de estimaciones | utils | Pendiente | — | — | El último, y solo si a esas alturas se echa de menos. |

---

## General

Documentación raíz (`README.md`, `CLAUDE.md`, `docs/`), configuración y todo lo transversal a los cuatro plugins.

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Documentar `content-sync-check` en el `README.md` | — | — | — | — | — | El skill existe desde `b223d81` y está en `docs/skills.md`, pero el README no lo menciona. |
| Pendiente | Decidir el destino del skill `documentar-proceso` | — | — | — | — | — | Solo tiene `DESIGN.md` desde `ac6d7cc`: sin `SKILL.md`, sin entrada en manifests ni en `docs/skills.md`. Implementarlo o retirarlo. |

**Cerradas en esta sección: 3m** · 3 archivadas

---

## utils

Los cuatro skills del plugin `utils`: `claude-activity-log`, `content-sync-check`, `documentar-proceso` y `tarea`.

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Añadir a `agenda` el modo semanal y la calibración de estimaciones | — | — | — | — | — | Dos errores que **no se corrigen con el mismo número**: esfuerzo (`Coste`→`Duración`, horas de trabajo, mediana de razones sobre duraciones sin `~`) y calendario (`Vence`→`Completada`, días de reloj, que en realidad mide capacidad). La salida útil es el sesgo enunciado, no solo el número corregido. |

**Cerradas en esta sección: ~2h 17m** · 8 archivadas

---

**Estados:**

- `Pendiente` — anotada.
- `🔵 En curso` — rama creada; una a la vez.
- `Pausada` — detenida por tiempo.
- `Bloqueada` — detenida por una dependencia; requiere Nota.
- `✅ Completada` — cerrada y archivada. Solo `🔵 En curso` y `✅ Completada` llevan icono, pegado al texto.

Al cerrarse, una tarea sale de este archivo hacia `historial/AAAA-MM.md` — no queda rastro en la
tabla de su sección. El flujo completo lo gobierna el skill `tarea`.
