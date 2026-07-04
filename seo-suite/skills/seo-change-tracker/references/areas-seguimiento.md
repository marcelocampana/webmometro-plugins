# Áreas de seguimiento y mapeo a herramientas MCP

Cada área de un cambio determina qué métricas capturar y con qué herramienta. Usa esta tabla para
decidir qué llamadas hacer al registrar un baseline o al medir un checkpoint — no llames todas las
fuentes para todos los cambios, solo las relevantes al `area` y `tipo` del cambio.

## on-page (title, meta description, headings, contenido de la página)

| Métrica | Herramienta MCP | Notas |
|---|---|---|
| Clics, impresiones, CTR, posición | `mcp__gsc__search_analytics` o `mcp__gsc__enhanced_search_analytics` | Filtrar por `page` = `target_url` y, si aplica, por las `keywords` del cambio |
| Sesiones, conversiones, conv. rate | `mcp__analytics-mcp__run_report` (GA4) | Dimensión `landingPage` = `target_url`, métricas `sessions`, `conversions`, `engagementRate` |
| Posición SERP | `mcp__dataforseo__serp_organic_live_advanced` | Una llamada por keyword principal; usar la misma ubicación/dispositivo en baseline y checkpoints para que sea comparable |

Es el área más común (cambios de title/meta/CTA) y la que más se beneficia de medir CTR — un
cambio de copy puede subir CTR sin mover el ranking, así que **siempre** captura `gsc` aquí.

## tecnico (indexación, canonicals, redirects, schema, Core Web Vitals, velocidad)

| Métrica | Herramienta MCP | Notas |
|---|---|---|
| Estado de indexación, canonical detectado | `mcp__gsc__index_inspect` | Usar la URL canónica completa (con protocolo y dominio) |
| Core Web Vitals, Performance score | Fuente PageSpeed configurada en el proyecto (ver `seo-suite/README.md`) | Correr para mobile y desktop si el cambio afecta rendimiento; si el MCP de PageSpeed no está disponible, deja el campo en `null` |
| Tráfico/conversión tras el cambio | `mcp__analytics-mcp__run_report` (GA4) | Solo si el cambio técnico puede afectar comportamiento de usuario (p.ej. velocidad, Core Web Vitals) |

Cambios puramente técnicos sin impacto esperado en comportamiento de usuario (p.ej. limpieza de
sitemap) pueden omitir `ga4` y `serp`.

## contenido (artículos nuevos, expansión de contenido existente, FAQ, etc.)

| Métrica | Herramienta MCP | Notas |
|---|---|---|
| Impresiones, clics, posición de las keywords objetivo | `mcp__gsc__search_analytics` | El contenido nuevo tarda en indexarse — el primer checkpoint puede mostrar `impressions: 0`, eso es normal, no un fallo |
| Posición SERP | `mcp__dataforseo__serp_organic_live_advanced` | |
| Sesiones, conversiones | `mcp__analytics-mcp__run_report` (GA4) | |

## backlinks (link building, outreach, menciones)

| Métrica | Herramienta MCP | Notas |
|---|---|---|
| Dominios de referencia, total de backlinks | `mcp__dataforseo__backlinks_summary` | Snapshot del dominio completo, no de una URL — los backlinks suelen apuntar al dominio o a páginas específicas, usar lo que corresponda |
| Nuevos/perdidos desde el baseline | `mcp__dataforseo__backlinks_bulk_new_lost_backlinks` o `backlinks_bulk_new_lost_referring_domains` | Útil en el checkpoint para ver el delta neto, no solo el total |

Los resultados de backlinks suelen tardar más en reflejarse (autoridad + indexación del enlace) —
usa el checkpoint de 28 días como mínimo, considera uno adicional a 60 días si el usuario lo pide.

## local (Google Business Profile, reseñas, NAP)

| Métrica | Herramienta MCP | Notas |
|---|---|---|
| Rating, cantidad de reseñas | `mcp__dataforseo__business_data_google_reviews` | |
| Datos de perfil (categorías, atributos, horario) | `mcp__dataforseo__business_data_google_my_business_info` | Útil para auditar consistencia tras un cambio de NAP/categoría |
| Visibilidad en Maps para keywords locales | `mcp__dataforseo__business_data_google_my_business_info`, o el MCP de SERP Google Maps que el proyecto tenga configurado si está disponible | Si ninguna fuente de Maps está disponible, deja el campo en `null` |

## Reglas generales

- **Nunca asumas que una fuente MCP está disponible.** Si una llamada falla o el servidor no está
  configurado en el proyecto, deja el campo como `null` en el frontmatter y pide al usuario el dato
  manualmente (o que confirme que se omite). No bloquees el registro del cambio por una fuente
  caída.
- **Usa la misma ventana de tiempo y el mismo filtro en baseline y en cada checkpoint.** Si el
  baseline de GSC es "últimos 28 días", el checkpoint debe pedir también 28 días — de lo contrario
  el delta no es comparable.
- **Un cambio puede tocar más de un área** (p.ej. una migración técnica que también reescribe
  contenido). En ese caso, usa el `area` predominante para clasificar el cambio, pero captura
  métricas de todas las áreas afectadas.
