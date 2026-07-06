# Metodología de clústeres de contenido

Referencia de criterios y umbrales para el skill `content-cluster-builder`. Estos son defaults
razonados, no reglas rígidas — el modelo los aplica con criterio y puede apartarse cuando el caso
lo justifica. Los valores marcados como "(configurable)" pueden sobreescribirse en `contexto/configuracion.md`.

---

## Filtrado de keywords (Paso 2)

| Criterio | Valor por defecto | Configurable |
|---|---|---|
| Volumen mínimo mensual | 50 búsquedas/mes | Sí (`cluster_volumen_min`) |
| Dificultad máxima (KD) | 60 | Sí (`cluster_kd_max`) |
| Excluir marca | Sí | No |
| Excluir duplicados exactos | Sí | No |

Intenciones a etiquetar: `informacional`, `comercial`, `transaccional`, `local`.

---

## Agrupación por solapamiento de SERP (Paso 3)

La agrupación se basa en cuántas URLs del top-10 orgánico comparten dos keywords. No usar
similitud de texto — eso produce falsos positivos de canibalización.

| URLs compartidas en top-10 | Acción |
|---|---|
| 7–10 | Fusionar: son el mismo tema, una sola página los cubre |
| 4–6 | Mismo clúster: páginas distintas pero estrechamente relacionadas |
| 2–3 | Sólo interlinkar: temas vecinos, clústeres separados |
| 0–1 | Separar: temas independientes |

**Por eficiencia de créditos:** correr SERP en vivo para las ~20–30 keywords de mayor volumen e
intención relevante, no para todas las candidatas. Para las demás, usar agrupación semántica +
intención como primer filtro y validar con SERP solo las dudas.

---

## Matriz de asignación de rol pilar (Paso 5)

Cruzar la **intención dominante de la SERP** del término cabeza (Paso 3) con el **tipo de página
existente** en el sitio (Paso 4). La taxonomía completa de `tipo_pagina` y la heurística para leer
la intención de la SERP están en `references/auditoria-intencion-url.md`.

| Intención SERP → | SERP transaccional | SERP comercial | SERP informacional |
|---|---|---|---|
| **Página existente transaccional** | **Pilar transaccional** — conservar conversión, enlazar spokes. NO reconvertir a guía. | Revisar desajuste; posible spoke comercial separado. | Desajuste: la página vende donde Google informa. Informar al usuario antes de proponer. |
| **Página existente informacional** | Desajuste: la página informa donde Google vende. Informar al usuario; ¿crear landing transaccional? | Puede ser pilar comercial o informacional según volumen. | **Pilar informativo** — hub educativo que distribuye a spokes de profundidad. |
| **Sin página existente (GAP)** | Crear nueva landing transaccional como pilar. | Crear nueva página comercial. | Crear nuevo hub informativo. |

**Regla dura:** nunca recomendar reconvertir una página transaccional que ya convierte en pilar
informativo sin aprobación explícita del usuario (con análisis de riesgo de conversión).

---

## Pilar vs. spoke (Paso 5)

- **Pilar:** keyword de mayor volumen y amplitud del clúster. Cubre el tema de forma general
  (2.000–4.000 palabras). Objetivo: rankear el término cabeza y distribuir autoridad.
- **Spoke:** keyword más específica o long-tail. Profundiza un subtema (800–1.500 palabras).
  Objetivo: rankear la long-tail y reforzar la autoridad del pilar mediante enlazado.

El pilar **no** es un mega-artículo que cubre todo en profundidad. Es un hub que distribuye y
enlaza a los spokes.

Número de spokes por clúster: 3–7 (mínimo viable para competir; más de 10 sin producción paralela
es deuda que rara vez se paga).

---

## Score de oportunidad por pieza (Paso 6)

```
oportunidad = volumen_normalizado(40%) + kd_inverso_normalizado(30%) + intent_weight(30%)
```

`intent_weight`: transaccional = 1.0 · local = 0.9 · comercial = 0.7 · informacional = 0.4

Orden de producción: primero `gap` con mayor score, luego `parcial`, después `cubierto` que solo
necesita reenlazado.

---

## Scorecard de salud del clúster (Paso 7)

Métricas:

```
Cobertura (%)    = spokes cubiertos o parciales / total spokes × 100
Link Health (%)  = spokes con enlace bidireccional al pilar / total spokes × 100
Content Quality  = spokes con calidad ≥3 / total spokes × 100
```

| Estado del clúster | Cobertura | Link Health | Quality | Resultado esperado |
|---|---|---|---|---|
| Incompleto | <50% | <70% | — | El pilar difícilmente rankea página 1 |
| En desarrollo | 50–70% | 70–90% | 50–80% | Pilar puede aparecer en pág 2–3 |
| Competitivo | 70–90% | 100% | 80–90% | Pilar compite en página 1 |
| Dominante | >90% | 100% | >90% | Pilar sólido; clúster captura la mayoría de queries |

**Listo para competir:** Cobertura >70%, Link Health 100%, Quality >80%.

### Gates de tolerancia-cero

Si cualquiera de estos falla, marcar el mapa como "necesita revisión":

| Gate | Umbral | Descripción |
|---|---|---|
| Canibalización | 0 pares con >40% overlap | Dos clústeres no pueden compartir más del 40% de SERPs |
| Huérfanos | 0 tolerados | Todo spoke debe tener enlace desde el pilar |
| Cobertura mínima | ≥70% | El pilar debe cubrir al menos el 70% de las keywords del clúster |
| Anchor diversity | Ningún anchor >40% | No repetir el mismo anchor en más del 40% de los enlaces del clúster |
| Coherencia de intención | 0 desajustes sin resolver | El tipo de contenido de cada pieza coincide con la intención dominante de su SERP, y ninguna página transaccional que convierte se reconvierte en pilar informativo sin decisión explícita del usuario |

---

## Estándares de enlazado interno

| Tipo de enlace | Mínimo | Dirección |
|---|---|---|
| Pilar → cada spoke | 1 por spoke | Desde la sección relevante del pilar |
| Cada spoke → pilar | 1 por spoke | "guía completa sobre [tema]" u equivalente |
| Spoke ↔ spokes hermanos | 2–4 por spoke | Solo donde sea contextualmente natural |
| Puentes entre clústeres | 0–2 por clúster | Solo con relevancia temática genuina |

Usar anchor text variado — no siempre la keyword exacta. Alternar entre variantes semánticas y
frases de contexto.
