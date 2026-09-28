<!-- tarea: umbral 40000 chars · holgura 70% · última revisión 2026-08-27 -->
<!-- tarea: toggl · proyecto 3968609 «Plugins de IA» · cliente 741361 «Webmómetro» -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Nota |
| :--: | --- | --- | --- | --- |
| 1 | Llevar a `tarea` el ciclo común en Toggl y fundir `tarea-suelta` <!-- toggl:16580515 --> | utils | Pendiente | — |
| 2 | Quitar `tareas.md`, `revisar.md` y `secciones.md` de `tarea-repo` <!-- toggl:16580516 --> | utils | Pendiente | — |
| 3 | Leer `agenda` y `plan-semanal` desde la copia de Toggl <!-- toggl:16580517 --> | utils | Pendiente | — |
| 4 | Crear el script que migra un repo a Toggl <!-- toggl:16580518 --> | utils | Pendiente | — |
| 5 | Subir `utils` a 4.0.0 y actualizar `docs/skills.md` y el README <!-- toggl:16580519 --> | Manifests | Pendiente | Al final |

---

## General

Documentación raíz (`README.md`, `CLAUDE.md`, `docs/`), configuración y todo lo transversal a los cuatro plugins.

| Estado | Tarea | Comentarios |
| --- | --- | --- |
| Pendiente | Documentar `content-sync-check` en el `README.md` <!-- toggl:16505029 --> | El skill existe desde `b223d81` y está en `docs/skills.md`, pero el README no lo menciona. |
| Pendiente | Decidir el destino del skill `documentar-proceso` <!-- toggl:16505030 --> | Solo tiene `DESIGN.md` desde `ac6d7cc`: sin `SKILL.md`, sin entrada en manifests ni en `docs/skills.md`. Implementarlo o retirarlo. |

**Cerradas en esta sección: 3m** · 3 archivadas

---

## Manifests

`.claude-plugin/marketplace.json` y los cuatro `plugin.json`.

| Estado | Tarea | Comentarios |
| --- | --- | --- |
| Pendiente | Subir `utils` a 4.0.0 y actualizar `docs/skills.md` y el README <!-- toggl:16580519 --> | Cierra el cambio a Toggl como única lista. Plan: `~/.claude/plans/s-haz-las-consultas-zesty-beaver.md`. |

**Cerradas en esta sección: 1m** · 1 archivada

---

## utils

Los skills del plugin: `agenda`, `balance`, `claude-activity-log`, `content-sync-check`, `documentar-proceso`, `plan-semanal`, `tarea` (entrada), `tarea-repo` y `tarea-suelta`.

| Estado | Tarea | Comentarios |
| --- | --- | --- |
| Pendiente | Llevar a `tarea` el ciclo común en Toggl y fundir `tarea-suelta` <!-- toggl:16580515 --> | Crear, abrir, pausar y cerrar en Toggl para todas; `tarea-repo` solo añade git e historial. Desaparece el nombre «suelta»: lo que no tiene repo lo dice su proyecto. Abrir tiene que pasar el estado a In Progress en Toggl (hoy se queda en Todo). |
| Pendiente | Quitar `tareas.md`, `revisar.md` y `secciones.md` de `tarea-repo` <!-- toggl:16580516 --> | En el repo quedan `historial/`, `auditoria.md` y `toggl.md` (enlace, áreas, reglas y comentarios). El área va en la primera línea de la descripción en Toggl. |
| Pendiente | Leer `agenda` y `plan-semanal` desde la copia de Toggl <!-- toggl:16580517 --> | Capacidad desde `capacities` de Toggl; `agenda.md` queda solo con `## Repos`. Las madres de tareas con pasos toman la fecha del último paso. |
| Pendiente | Crear el script que migra un repo a Toggl <!-- toggl:16580518 --> | Arma el `bulk-create` desde `tareas.md`, `revisar.md` y `secciones.md`, lo muestra, y con visto bueno lo envía y limpia el repo. Reutiliza `emparejar_ahora.py`. |

**Cerradas en esta sección: ~3h 4m** · 14 archivadas

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
