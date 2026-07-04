# Rutina de reconciliación (recordatorio de ejecución SEO)

Esta referencia documenta una **rutina reutilizable** que cierra el bucle entre lo que los skills de
SEO *recomiendan* y lo que efectivamente se *registró* en el tracking. No es un archivo que corra
solo: la **instancia** se crea por cliente con la skill `schedule` (agente programado), apuntando al
workspace de ese cliente. Aquí queda la plantilla para que crearla sea copiar/pegar.

## Por qué existe

El registro de un cambio depende de que alguien se acuerde de pedirlo. Las capas 1 (auto-activación
por descripción) y 2 (hand-off desde `seo-audit`/`page-cro`/`ai-seo`/`brand-voice-enforcement`)
cubren la mayoría de los casos, pero no todos. Esta rutina es la **red de seguridad temporal**:
encaja mejor que un hook porque el modelo del tracker es intrínsecamente diferido (checkpoints a
14/28 días). **Respalda**, no reemplaza, las capas 1 y 2.

## Qué hace el agente (lógica)

1. **Lee las acciones propuestas** en los informes más recientes de `web/seo/informes/{periodo}/`
   (`seo-audit`, `page-cro`, `ai-seo`). Estas vienen como checklist con un **slug** por acción
   (+ `area`, `target_url`, `prioridad`).
2. **Lee los cambios registrados** en `contexto/seo-tracking/cambios/`.
3. **Cruza propuesta ↔ registro**, en dos pasadas:
   - **Match determinista por `accion_origen`:** una nota de cambio cuyo `accion_origen` == slug de
     la acción es un match exacto.
   - **Match semántico de respaldo:** para acciones sin match exacto, empareja por `target_url` +
     `area` + similitud de la descripción. Es aproximado; úsalo solo para recordar, nunca para
     afirmar con certeza que algo se hizo o no.
4. **Clasifica y arma el digest** (ver abajo), **sin escribir nada sin confirmación** — el principio
   de confirmación obligatoria del skill aplica también aquí. La rutina *propone*, el usuario decide.

## Reglas de clasificación

| Situación | Salida en el digest |
|---|---|
| Acción con cambio `implementado`/`midiendo`/`concluido` | **Hecho.** Si está en `midiendo` y el checkpoint ya venció (`fecha` + `checkpoint_dias`), pásalo a **A medir** y propone correr el Modo 2 |
| Acción **sin** ningún cambio asociado | **Pendiente.** Recuerda hacerla, o registrarla si ya se hizo sin anotar |
| Cambio en `estado: planificado` que nunca pasó a `implementado` | **Pendiente.** Recuerda implementarlo o descartarlo |
| Cambio registrado sin acción de origen (`accion_origen: null`) que no matchea ninguna propuesta | Informativo: cambio ad-hoc, ya trackeado. No requiere acción |

## Formato del digest ("estado de ejecución SEO")

```markdown
# Estado de ejecución SEO — {cliente} — {fecha}

## A medir ahora ({n})
- {descripcion} — checkpoint {dias}d vencido el {fecha} → correr Modo 2

## Pendientes ({n})
- {slug/descripcion} — recomendado en {informe} el {fecha}, sin registrar

## Hechos y en curso ({n})
- {descripcion} — {estado} ({resultado si concluido})
```

Manténlo corto y accionable: es un recordatorio semanal, no un reporte ejecutivo (ese lo genera el
Modo 3 con `scripts/generar_reporte.py`).

## Crear la instancia por cliente (skill `schedule`)

Cadencia sugerida: **semanal**. Prompt plantilla para la rutina:

```
Eres la rutina de reconciliación SEO de {cliente}. Trabajando en {ruta-del-workspace-del-cliente}:
1. Lee las acciones propuestas en web/seo/informes/{periodo más reciente}/ (checklist con slug).
2. Lee los cambios en contexto/seo-tracking/cambios/.
3. Cruza por accion_origen (exacto) y luego semántico (target_url + area + descripción).
4. Entrega el digest "estado de ejecución SEO" (A medir / Pendientes / Hechos), siguiendo
   references/rutina-reconciliacion.md del skill seo-change-tracker.
No escribas ni modifiques ninguna nota ni informe sin confirmación explícita: solo reporta.
```

Requisitos: la rutina necesita **acceso al workspace del cliente** (para leer `web/seo/informes/` y
`contexto/seo-tracking/`). Si el proyecto usa ubicaciones legadas, aplica el resolver flexible del
skill antes de cruzar.
