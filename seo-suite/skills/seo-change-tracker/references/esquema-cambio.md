# Esquema de una nota de cambio

Cada cambio SEO es un archivo `.md` en `contexto/seo-tracking/cambios/`, nombrado `AAAA-MM-DD-slug.md`
(fecha del cambio + slug corto del target/acción, p.ej. `2026-06-16-meta-laser-co2.md`).

El slug se deriva de `target_url` o `descripcion`: minúsculas, sin tildes, espacios → guiones,
máximo ~5 palabras.

## Frontmatter completo

```yaml
---
id: 2026-06-16-meta-laser-co2
fecha: 2026-06-16
area: on-page
tipo: meta-tags
target_url: https://www.clinicadrazaror.cl/laser-co2-fraccionado
keywords: [laser co2 fraccionado, co2 fraccionado]
accion_origen: null
descripcion: Reescritura de title y meta description para subir CTR en page 1
hipotesis: Subir CTR de 1.08% a ~3-5% sin mover ranking, ~65 clics/mes adicionales
estado: midiendo
resultado: pendiente
checkpoint_dias: [14, 28]
baseline:
  fecha: 2026-06-16
  gsc: {clicks: 18, impressions: 1665, ctr: 1.08, position: 6.2}
  ga4: {sessions: 536, conversions: 30, conv_rate: 5.6}
  serp: {posicion: 10, fuente: dataforseo}
  tecnico: null
  backlinks: null
  local: null
checkpoints:
  - fecha: 2026-06-30
    dias: 14
    gsc: {clicks: 31, impressions: 1700, ctr: 1.82, position: 5.9}
    ga4: {sessions: 560, conversions: 34, conv_rate: 6.1}
    serp: {posicion: 8, fuente: dataforseo}
    nota: ""
---
```

## Campos y vocabularios controlados

| Campo | Tipo | Valores / formato |
|---|---|---|
| `id` | string | igual al nombre de archivo sin `.md` |
| `fecha` | date | `AAAA-MM-DD`, fecha de implementación del cambio |
| `area` | enum | `on-page` \| `tecnico` \| `contenido` \| `backlinks` \| `local` \| `otro` |
| `tipo` | string libre | p.ej. `meta-tags`, `redirect`, `schema-markup`, `link-building`, `gbp-post` — usa lo que mejor describa la acción, no hay lista cerrada |
| `target_url` | string o null | URL afectada; `null` si el cambio es a nivel de sitio o de perfil (p.ej. GBP) |
| `keywords` | lista de strings | keywords relacionadas, para cruzar con SERP/GSC |
| `accion_origen` | string o null | slug de la acción del informe (`seo-audit`/`page-cro`/`ai-seo`) que originó el cambio, cuando llega por hand-off desde ese skill. Es la clave del **match determinista** de la rutina de reconciliación (`references/rutina-reconciliacion.md`). `null` para cambios ad-hoc registrados directamente |
| `descripcion` | string | qué se hizo, en una frase |
| `hipotesis` | string | **obligatorio** — qué resultado se espera y por qué. Sin esto el cambio no es medible: no hay forma de juzgar "funcionó" sin saber qué se esperaba |
| `estado` | enum | `planificado` (aún no implementado) → `implementado` (recién hecho, baseline capturado) → `midiendo` (esperando checkpoints) → `concluido` (con veredicto final) |
| `resultado` | enum | `pendiente` \| `positivo` \| `neutral` \| `negativo` \| `inconcluso` (datos insuficientes o contradictorios) |
| `checkpoint_dias` | lista de int | días desde `fecha` en que se debe re-medir. Default `[14, 28]` si no se especifica `checkpoint_dias_default` en `contexto/configuracion.md` |
| `baseline` | objeto | snapshot de métricas al momento del cambio, una clave por área relevante (las no aplicables quedan `null`) |
| `checkpoints` | lista de objetos | un objeto por medición de seguimiento, mismo shape que `baseline` más `dias` y `nota` |

### Sub-objetos de métricas (mismo shape en baseline y checkpoints)

- `gsc`: `{clicks, impressions, ctr, position}` — de `mcp__gsc__search_analytics` filtrado por `target_url` y/o `keywords`.
- `ga4`: `{sessions, conversions, conv_rate}` — de `mcp__analytics-mcp__run_report`, filtrado por landing page si aplica.
- `serp`: `{posicion, fuente}` — de `mcp__dataforseo__serp_organic_live_advanced`, una posición por keyword principal (si hay varias keywords, usa la de mayor volumen o registra un objeto por keyword).
- `tecnico`: `{indexado, core_web_vitals, ...}` — indexación/canonical de `mcp__gsc__index_inspect`; Core Web Vitals / performance de la fuente PageSpeed que el proyecto tenga configurada (ver `seo-suite/README.md`; si no está disponible, deja `core_web_vitals` en `null`), según lo que aplique al cambio.
- `backlinks`: `{referring_domains, backlinks_total}` — de `mcp__dataforseo__backlinks_summary`.
- `local`: `{rating, reviews_count}` — de `mcp__dataforseo__business_data_google_reviews` o `business_data_google_my_business_info`.

No completes sub-objetos que no apliquen al área del cambio — déjalos `null`. Esto evita llamadas
MCP innecesarias y mantiene el frontmatter legible.

## Cuerpo de la nota (debajo del frontmatter)

Texto libre: contexto adicional, capturas o enlaces de evidencia, decisiones tomadas en checkpoints
intermedios. No structurado — el frontmatter es la fuente de verdad para el reporte.
