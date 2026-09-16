<!-- task-flow: umbral 40000 chars · holgura 70% · última revisión 2026-08-27 -->

# Tareas

## Ahora

El orden de esta tabla **es** el orden de ejecución: se toma la primera fila que no esté `Bloqueada`, y se para al cerrarla. Sus filas son punteros — la tarea vive en la sección de su área, y aquí solo aparece mientras toca.

| # | Tarea | Sección | Estado | Vence | Coste | Nota |
| :--: | --- | --- | --- | --- | --- | --- |
| 1 | Crear el skill `agenda` con la vista diaria cross-repo | utils | Pendiente | — | — | Ya desbloqueada: las filas tienen `Coste` desde 1.7.0. |
| 2 | Montar la rutina diaria que dispara la agenda | utils | Pendiente | — | — | No toca este repo: es configuración de la máquina. Monday va aquí. |
| 3 | Añadir a `agenda` el modo semanal y la calibración de estimaciones | utils | Pendiente | — | — | El último, y solo si a esas alturas se echa de menos. |

---

## General

Documentación raíz (`README.md`, `CLAUDE.md`, `docs/`), configuración y todo lo transversal a los cuatro plugins.

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Documentar `content-sync-check` en el `README.md` | — | — | — | — | — | El skill existe desde `b223d81` y está en `docs/skills.md`, pero el README no lo menciona. |
| Pendiente | Decidir el destino del skill `documentar-proceso` | — | — | — | — | — | Solo tiene `DESIGN.md` desde `ac6d7cc`: sin `SKILL.md`, sin entrada en manifests ni en `docs/skills.md`. Implementarlo o retirarlo. |

---

## utils

Los cuatro skills del plugin `utils`: `claude-activity-log`, `content-sync-check`, `documentar-proceso` y `task-flow`.

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Crear el skill `agenda` con la vista diaria cross-repo | — | — | — | — | — | Skill aparte, **solo lectura**: la precondición de `task-flow` es resolver *este* repo con git y retirarse si no hay `tareas/`; la del consolidador es una lista de rutas sin git. Config en `Documents/config/claude/task-flow.md` (registro de repos + capacidad diaria, que es global). Debe caber en una pantalla. |
| Pendiente | Montar la rutina diaria que dispara la agenda | — | — | — | — | — | Fuera del repo: es configuración de la máquina, no código del marketplace. El conector de Monday vive aquí y no en el skill —precedente de `seo-suite`, que declara sus MCP como prerrequisito—. Corre sobre lo commiteado en `main`, así que no ve trabajo sin commitear. |
| Pendiente | Añadir a `agenda` el modo semanal y la calibración de estimaciones | — | — | — | — | — | Dos errores que **no se corrigen con el mismo número**: esfuerzo (`Coste`→`Duración`, horas de trabajo, mediana de razones sobre duraciones sin `~`) y calendario (`Vence`→`Completada`, días de reloj, que en realidad mide capacidad). La salida útil es el sesgo enunciado, no solo el número corregido. |
| Pendiente | Reducir `references/modo-gestion.md` al techo declarado de ~1.7k tokens | — | — | — | — | — | Está en 8.984 chars (~2.2k tokens) tras el impacto documental y la estimación al crear. `CLAUDE.md` fija ~1.7k por referencia. Candidato: extraer la cadena de cierre a su propia referencia. |

**Cerradas en esta sección: ~35m** · 1 archivada

---

**Estados:**

- `Pendiente` — anotada.
- `🔵 En curso` — rama creada; una a la vez.
- `Pausada` — detenida por tiempo.
- `Bloqueada` — detenida por una dependencia; requiere Nota.
- `✅ Completada` — cerrada y archivada. Solo `🔵 En curso` y `✅ Completada` llevan icono, pegado al texto.

Al cerrarse, una tarea sale de este archivo hacia `historial/AAAA-MM.md` — no queda rastro en la
tabla de su sección. El flujo completo lo gobierna el skill `task-flow`.
