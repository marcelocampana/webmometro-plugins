# Fuentes de datos y herramientas MCP por paso

Mapeo de qué herramienta MCP usar en cada paso del skill. Idéntico en espíritu a
`seo-change-tracker/references/areas-seguimiento.md`: consultar antes de hacer llamadas para no
invocar fuentes irrelevantes ni omitir las que sí importan.

**Regla general:** si una herramienta no responde o el servidor MCP no está configurado, dejar el
campo en `null`, informarlo al usuario y continuar. Nunca bloquear el flujo por una fuente caída.

---

## Paso 1: Expansión de la semilla

| Datos | Herramienta MCP | Notas |
|---|---|---|
| Keywords relacionadas | `mcp__dataforseo__labs_google_related_keywords` | Punto de partida; devuelve keywords semánticamente relacionadas con volumen |
| Sugerencias long-tail | `mcp__dataforseo__labs_google_keyword_suggestions` | Variantes de la semilla con volumen y KD |
| Volumen + KD + CPC | `mcp__dataforseo__keywords_google_ads_search_volume` | Validar volumen de keywords ya identificadas |
| Preguntas PAA | `mcp__dataforseo__labs_google_keyword_ideas` | Con `include_serp_info=true` captura People Also Ask |
| Keywords reales del sitio | `mcp__gsc__search_analytics` | Filtrar por dominio del `config.md`; devuelve queries reales con impresiones y posición |

Orden sugerido: empezar con `related_keywords` + `keyword_suggestions` → enriquecer con `search_volume` → complementar con GSC.

---

## Paso 1a: Inventario de contenido del sitio

| Datos | Herramienta MCP | Notas |
|---|---|---|
| URLs indexadas del sitio | `mcp__gsc__list_sitemaps` + `mcp__gsc__get_sitemap` | Gratis; lista todas las URLs del sitemap. Filtrar luego por relevancia semántica con la semilla |
| Keywords completas del dominio | `mcp__dataforseo__labs_google_keywords_for_site` | Incluye posiciones 50+ que GSC quizá no muestre; ayuda a detectar páginas existentes con bajo rendimiento |
| Contenido real de cada URL relevante | `WebFetch` | Suficiente para sitios server-rendered (WordPress, Webflow, Shopify, la mayoría de CMS). Clasificar con `auditoria-intencion-url.md` |
| Render real (solo fallback) | `mcp__chrome-devtools__navigate_page` + `take_snapshot` | Solo si WebFetch devuelve contenido incompleto (SPAs JS-heavy). No usar por defecto |
| Crawl exhaustivo (opcional) | `mcp__dataforseo__onpage_task_post` + `onpage_pages` | Para sitios grandes donde el sitemap no basta; consume créditos. Ofrecerlo, no imponerlo |

Objetivo: saber qué subtemas del clúster **ya tienen página** (aunque no rankeen) antes de
declarar GAPs. El default es sitemap (gratis) + WebFetch (gratis); las fuentes de DataForSEO son
para profundizar cuando se justifica.

---

## Paso 2: Etiquetado de intención

| Datos | Herramienta MCP | Notas |
|---|---|---|
| Intención por keyword | `mcp__dataforseo__labs_google_search_intent` | Devuelve intención principal y secundaria por keyword; usar en lote para eficiencia |

Si `search_intent` no está disponible, etiquetar manualmente con heurísticas: keywords con "qué es",
"cómo", "por qué" → informacional; "mejor", "precio", "comparar" → comercial; "comprar", "reservar",
"agendar", nombre de servicio directo → transaccional; "[servicio] + [ciudad/comuna]" → local.

**Voz del buscador (cómo pregunta la gente):** además de la intención, capturar el lenguaje y las
preguntas reales. Fuentes y tabla completa en `references/voz-del-buscador.md`:

| Datos | Herramienta MCP | Notas |
|---|---|---|
| Queries reales del sitio | `mcp__gsc__search_analytics` | Dimensión `query`: lenguaje de 1ª mano |
| People Also Ask | `mcp__dataforseo__labs_google_keyword_ideas` (`include_serp_info=true`) | Sub-preguntas y sub-intenciones |
| Modificadores / variantes | `mcp__dataforseo__labs_google_keyword_suggestions` | precio, duele, opiniones, cerca de mí… |
| Lenguaje de comunidades (opcional) | `mcp__dataforseo__business_data_reddit_search`; `content_analysis_*` | Dolores y objeciones reales; consume créditos, ofrecer no imponer |

---

## Paso 3: Clustering por solapamiento de SERP + intención dominante

| Datos | Herramienta MCP | Notas |
|---|---|---|
| Top-10 orgánico por keyword | `mcp__dataforseo__serp_google_organic_live` | Usar `location_code` y `language_code` de `config.md`; correr para las 20–30 keywords de mayor potencial, no todas |
| Intención por keyword (confirmación) | `mcp__dataforseo__labs_google_search_intent` | Opcional: corroborar la intención inferida manualmente con el modelo |

Parámetros que deben ser consistentes entre llamadas (mismos que el `seo-change-tracker` usa):
`location_code` desde `config.md` → `ubicacion_serp.ciudad`; `language_code` desde `config.md` → `ubicacion_serp.idioma`.

Para ahorrar créditos: agrupar primero por intención (Paso 2) y correr SERP solo para las dudas de
si dos keywords deben ir juntas o separadas.

**Clasificar la intención dominante de la SERP** para cada keyword cabeza usando los resultados de
`serp_google_organic_live`: observar el tipo de dominio (clínica/tienda vs. blog/medio), el patrón
de URL (`/servicios/…` vs. `/blog/…`), el título del resultado y los `item_types` presentes
(local_pack, featured_snippet, etc.). Ver heurística completa en
`references/auditoria-intencion-url.md`.

---

## Paso 4: Cobertura + auditoría de contenido e intención de URLs propias

**4a. Coverage en el vault** — no usa MCP:
- Usar Grep/Glob sobre el vault del proyecto.
- Buscar notas `.md` que mencionen la keyword o el subtema en el título o en el frontmatter.
- Clasificar: cubierto / parcial / gap según existencia y calidad percibida del contenido.

**4b. Auditoría de URLs propias** — para cada URL del propio dominio identificada en GSC o en la
SERP del Paso 3:

| Datos | Herramienta | Notas |
|---|---|---|
| Contenido real de la página | `WebFetch` sobre la URL | Opción por defecto: rápida y sin créditos |
| Render real (JS-heavy) | `mcp__chrome-devtools__navigate_page` + `take_snapshot` | Usar solo si WebFetch devuelve contenido incompleto |
| Análisis on-page estructurado | `mcp__dataforseo__onpage_pages` | Útil si ya se tiene una tarea onpage activa del dominio |
| Intención a nivel keyword | `mcp__dataforseo__labs_google_search_intent` | Para corroborar; no reemplaza abrir la página |

Seguir el procedimiento de `references/auditoria-intencion-url.md` para clasificar
`tipo_pagina_actual`, `intencion_satisfecha` y `coincide_con_serp`.

**4c. Chequeo de canibalización contra URLs propias** — para cada pieza nueva (gap), comparar su
SERP objetivo contra la SERP de las URLs propias que ya rankean:

| Datos | Herramienta | Notas |
|---|---|---|
| Top-10 de la keyword de la pieza nueva | `mcp__dataforseo__serp_google_organic_live` | Mismos `location_code`/`language_code` del `config.md`; reutilizar las SERPs ya traídas en el Paso 3 si están disponibles |
| Top-10 de la keyword de la URL propia existente | `mcp__dataforseo__serp_google_organic_live` | Igual; comparar los dos conjuntos de URLs |

Calcular el overlap = (URLs compartidas en el top-10) / 10. Si supera el 40%, marcar
canibalización (ver umbral en `metodologia-cluster.md`). Para ahorrar créditos, comparar solo las
keywords cuya intención y subtema se solapen — no todos los pares.

---

## Paso 5 y 6: Arquitectura y priorización

No requieren llamadas MCP adicionales. Los datos ya están de los pasos anteriores.

Si el proyecto tiene una guía de brand voice, leerla con Read. Descubrirla, no asumir una ruta
fija: buscar con Glob/Grep archivos cuyo nombre o ruta contenga "brand", "voice", "tono" o "voz"
(p. ej. en un directorio `editorial/`, `brand/` o similar). Tomar la coincidencia más específica.
Si no aparece ninguna, continuar sin guía de marca — es un enriquecedor opcional, no un requisito.

---

## Paso 7: Scorecard de salud

Ejecutar `scripts/salud_cluster.py` si ya hay notas en el vault. Si no hay notas aún (plan puro),
calcular las métricas manualmente con las tablas de `metodologia-cluster.md`.

No requiere llamadas MCP — trabaja sobre archivos locales del proyecto.

---

## Créditos DataForSEO: estimación previa

Antes de correr búsquedas masivas de SERP, estimar el costo:
```
créditos ≈ n_keywords × 3  (modo standard)
créditos ≈ n_keywords × 10 (modo advanced)
```
Si la estimación supera ~500 créditos, informar al usuario y ofrecer dos caminos: reducir el número
de keywords a revisar con SERP, o proceder con la estimación completa.
