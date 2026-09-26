<!-- tarea: umbral 40000 chars · holgura 70% · última revisión 2026-08-27 -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Vence | Coste | Nota |
| :--: | --- | --- | --- | --- | --- | --- |
| 1 | Instalar y activar Toggl en el Mac y en los repos | utils | Pendiente | — | — | Necesita al usuario presente. |

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

Los skills del plugin `utils`: `agenda`, `balance`, `claude-activity-log`, `content-sync-check`, `documentar-proceso` y `tarea`.

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Instalar y activar Toggl en el Mac y en los repos | — | — | — | — | — | Activar el gancho `UserPromptSubmit` en `~/.claude/settings.json` y el arranque de `presencia.py` al encender el Mac; crear clientes y proyectos en Toggl y `~/Github/AI-kit/config/context/toggl.md`; migrar el primer repo (el de plugins) al formato sin columnas de tiempo. Cada cambio fuera del repo, con visto bueno en el momento. |

**Cerradas en esta sección: ~2h 26m** · 9 archivadas

---

**Estados:**

- `Pendiente` — anotada.
- `🔵 En curso` — rama creada; una a la vez.
- `Pausada` — detenida por tiempo.
- `Bloqueada` — detenida por una dependencia; requiere Nota.
- `✅ Completada` — cerrada y archivada. Solo `🔵 En curso` y `✅ Completada` llevan icono, pegado al texto.

Al cerrarse, una tarea sale de este archivo hacia `historial/AAAA-MM.md` — no queda rastro en la
tabla de su sección. El flujo completo lo gobierna el skill `tarea`.
