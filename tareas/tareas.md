<!-- tarea: umbral 40000 chars · holgura 70% · última revisión 2026-08-27 -->
<!-- tarea: toggl · proyecto 3968609 «Plugins de IA» · cliente 741361 «Webmómetro» -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Nota |
| :--: | --- | --- | --- | --- |

---

## General

Documentación raíz (`README.md`, `CLAUDE.md`, `docs/`), configuración y todo lo transversal a los cuatro plugins.

| Estado | Tarea | Comentarios |
| --- | --- | --- |
| Pendiente | Documentar `content-sync-check` en el `README.md` <!-- toggl:16505029 --> | El skill existe desde `b223d81` y está en `docs/skills.md`, pero el README no lo menciona. |
| Pendiente | Decidir el destino del skill `documentar-proceso` <!-- toggl:16505030 --> | Solo tiene `DESIGN.md` desde `ac6d7cc`: sin `SKILL.md`, sin entrada en manifests ni en `docs/skills.md`. Implementarlo o retirarlo. |

**Cerradas en esta sección: 3m** · 3 archivadas

---

## utils

Los skills del plugin `utils`: `agenda`, `balance`, `claude-activity-log`, `content-sync-check`, `documentar-proceso` y `tarea`.

| Estado | Tarea | Comentarios |
| --- | --- | --- |
| Pendiente | Registrar y planificar tareas sin repositorio (skill trabajo) <!-- toggl:16506476 --> | Segundo carril para tareas que no viven en un repo ni terminan en commit (p. ej. facturar, hoy manual). Solo en Toggl (cliente › proyecto, p. ej. Webmómetro › Administración; pueden ser recurrentes), sin fila en tareas.md. Se empiezan y terminan diciéndoselo a Claude en cualquier sesión: marcas locales y, al terminar, tramos a Toggl en bloque, sin rama ni commit; la presencia del Mac mide aunque el trabajo sea fuera de Claude. `plan-semanal` las propone como candidatas y `balance` marca las manuales que se repiten como candidatas a que las haga Claude. Skill aparte de `tarea`, que exige git; reusa `presencia.py` y el envío en bloque. |

**Cerradas en esta sección: ~2h 48m** · 11 archivadas

---

**Estados:**

- `Pendiente` — anotada.
- `🔵 En curso` — rama creada; una a la vez.
- `Pausada` — detenida por tiempo.
- `Bloqueada` — detenida por una dependencia; requiere Nota.
- `✅ Completada` — cerrada y archivada. Solo `🔵 En curso` y `✅ Completada` llevan icono, pegado al texto.

Al cerrarse, una tarea sale de este archivo hacia `historial/AAAA-MM.md` — no queda rastro en la
tabla de su sección. El flujo completo lo gobierna el skill `tarea`. **Repo conectado a Toggl:** el
tiempo (Coste, Vence, Inicio, Completada, Duración) vive en Toggl y en el registro de presencia; el
historial conserva todas las columnas.
