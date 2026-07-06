---
name: site-snapshot
description: "When the user wants to generate a factual data snapshot for an entire site or domain. Also use when the user mentions \"site snapshot,\" \"site report,\" \"domain snapshot,\" \"site data extraction,\" \"pull site data,\" \"generate site baseline,\" \"extract site metrics,\" or wants to consolidate analytics, search, performance, behavior and SEO data for a domain into a single reference document. This skill extracts data only — it does not diagnose, recommend, or interpret. For page-level snapshots, see page-snapshot. For SEO diagnosis, see seo-audit. For conversion analysis, see page-cro."
metadata:
  version: 1.3.0
---

# Site Snapshot

You build a factual data snapshot for an entire site or domain, consolidating metrics from GA4, GSC, PageSpeed, Clarity and DataForSEO into a single Markdown reference document.

The output is `web/seo/datos/{periodo}/snapshot-sitio.md` (see Workspace & Paths) — a neutral, data-only file designed for human reading and downstream consumption by other skills (seo-audit, page-cro, ai-seo, site-context, audience-demand-evaluation).

## Editorial Principles

The snapshot is strictly factual. Include only: metrics, dimensions, tables, periods, extraction metadata, and metric definitions.

Do not include: recommendations, interpretations, insights, probable causes, priorities, or composite scores.

Use neutral titles for sections and tables (e.g., "Resumen por período," "Top páginas por clics"). Avoid evaluative titles (e.g., "Quick Wins," "Páginas con bajo rendimiento").

This matters because downstream skills rely on clean, unbiased data. If the snapshot contains opinions disguised as data, every skill that reads it inherits that bias.

## Language

**The entire output document must be written in Spanish neutro** — including all section headers, table headers, column names, field labels, period names, and technical terms. Do not use English headings or labels in the output file.

Examples of correct translation:
- "Overview by Period" → "Resumen por período"
- "Top Pages by Clicks" → "Top páginas por clics"
- "Acquisition by Channel" → "Adquisición por canal"
- "Device Mix" → "Mix de dispositivos"
- "Coverage Summary" → "Resumen de cobertura"
- "Extraction date" → "Fecha de extracción"
- "Reference date" → "Fecha de referencia"
- "Last 28 days" → "Últimos 28 días"
- "Last 90 days" → "Últimos 90 días"
- "Last 6 months" → "Últimos 6 meses"
- "Last 12 months" → "Últimos 12 meses"
- "Current state" → "Estado actual"
- "Latest snapshot" → "Snapshot más reciente"

Content inside tables stays in the original language of the source. If GA4 reports an event as `book_demo`, record it as-is. If a page title is in English, record it in English. Only the labels, headers, and structural elements of the document are translated — never the raw data values.

Write all user-facing communication (explanations, questions, warnings, errors) in Spanish neutro.

## Workspace & Paths

This skill operates inside a **shared client workspace** used by several plugins. The rule is: shared truth lives once at the client root under `contexto/`; each domain has its own work area; nothing is duplicated.

```text
{cliente}/
  contexto/                     ← COMPARTIDO (todos los plugins leen; nadie duplica)
    sitio.md                       (site-context)
    configuracion.md               ← este skill produce/lee aquí los identificadores de fuente
    audiencia-canales.md           (audience-demand)
    marca/                         (brand-voice-pro)
    antecedentes/                  (informes previos del equipo)
  web/seo/
    datos/{periodo}/            ← SALIDA de este skill (solo datos)
      snapshot-sitio.md
      paginas/snapshot-pagina-{slug}.md
    informes/{periodo}/         (auditoría / CRO / AI-SEO)
```

Rules:
- **Client root:** resolve the workspace root by walking up from the current directory until you find `contexto/`. Read shared files from there; write snapshots under `web/seo/datos/{periodo}/`.
- **Período (`{periodo}`) = `YYYY-MM`** derived from the reference date (e.g. `2026-07`). Each run writes into its period folder; older periods are preserved as history.
- **Canonical Spanish names:** `contexto/configuracion.md`, `web/seo/datos/{periodo}/snapshot-sitio.md`. Do not generate JSON versions.
- **Flexible resolver (do not fail on a name):** if the canonical file/location isn't found, resolve by role — search for the equivalent inside `contexto/` (source config) or the project's existing snapshot tree (e.g. a legacy `context/…`, an English `snapshot-config.md`, or a `reportes/contexto/{mes}/…` layout). If found in a legacy shape, **offer to migrate** (rename/relocate) to the canonical paths before writing; if the user declines, keep writing where the existing tree lives so files aren't split. If nothing is found, ask the user — never assume a fixed alternate name.
- The `Source Inventory` section inside the snapshot is the traceability record — no separate manifest files.

## Source Config

`contexto/configuracion.md` stores non-sensitive identifiers: domain, market, language, property IDs, project IDs, strategic URL list. It is shared (other plugins read the same domain/URLs) and lives once at the client root — do not copy it into `web/seo/`.

Auto-detection rules:
- The system can auto-detect: main domain, market, language
- Source identifiers (GA4 property, GSC site URL, Clarity project, DataForSEO target domain) must be asked from the user the first time
- Do not guess property IDs or project IDs

Do not store secrets. Secrets are resolved by MCP, environment variables, or secret manager.

Example:

```md
# Configuración

## General

| Campo | Valor |
|---|---|
| Dominio | `www.example-saas.com` |
| Mercado | `CL` |
| Idioma | `es` |
| Fecha de referencia | `2025-03-31` |

## Identificadores de fuente

| Fuente | Campo | Valor |
|---|---|---|
| GA4 | Property ID | `123456789` |
| GSC | Site URL | `sc-domain:example-saas.com` |
| Clarity | Project ID | `abc123xyz` |
| DataForSEO | Dominio objetivo | `example-saas.com` |

## URLs estratégicas

| Etiqueta | URL |
|---|---|
| Home | `https://www.example-saas.com/` |
| Pricing | `https://www.example-saas.com/pricing` |
| Product | `https://www.example-saas.com/product` |
| Demo | `https://www.example-saas.com/demo` |
```

## Reference Date

All relative time windows are calculated backwards from a **reference date** provided by the user — not from today's system date.

Ask the user for the reference date before starting any data extraction. If the user does not specify one, ask explicitly:

> "¿Desde qué fecha quieres que se calculen los períodos del snapshot? Por ejemplo: si indicas el 31 de marzo de 2025, 'últimos 28 días' irá del 2 al 31 de marzo."

Accept any unambiguous format (ISO, written date, "fin del mes pasado", etc.) and confirm the resolved date before proceeding.

Record the reference date in the snapshot's `Metadatos` as `Fecha de referencia` (it is per-period, so it is stamped in each period's snapshot). You may also keep the last-used value in `contexto/configuracion.md` under `General` as a convenience default.

## Sources and Time Windows

All windows below are calculated backwards from the reference date provided by the user.

| Fuente | Ventanas |
|---|---|
| GA4 | Últimos 28 días, Últimos 90 días, Últimos 6 meses, Últimos 12 meses |
| GSC | Últimos 28 días, Últimos 90 días, Últimos 6 meses, Últimos 12 meses, Estado actual (cobertura) |
| PageSpeed | Estado actual |
| Clarity | Últimos 28 días, Últimos 90 días |
| DataForSEO | Snapshot más reciente |

## Minimum Datasets per Source

**GA4:** resumen por período, adquisición por canal, mix de dispositivos, top landing pages, eventos de conversión, tendencia mensual (12 meses).

**GSC:** resumen por período, top queries por clics, queries con posición promedio 4-20, top páginas por clics, **top 20 páginas por clics (últimos 90 días) con clics, CTR e impresiones**, tendencia mensual (12 meses), resumen de cobertura, detalle de cobertura.

**PageSpeed:** snapshots por URL estratégica y dispositivo, field data cuando esté disponible. Extraer con el script compartido del plugin, una vez por URL estratégica:

```bash
python3 "<ruta-del-plugin>/scripts/pagespeed_field.py" <url> --strategy both --json
```

El script (PSI v5 + CrUX) resuelve la Google API key desde `GOOGLE_API_KEY` o `~/.config/claude-seo/google-api.json` y devuelve números crudos (lab + field), sin ratings. **Degradación explícita:** si sale con `error: no_api_key` (código 3) o falla la cuota, usar el fallback `mcp__dataforseo__on_page_lighthouse` (lab-only, sin CrUX) y registrar en el Inventario de fuentes que PageSpeed quedó lab-only. No abortar el snapshot.

**Clarity:** resumen por período, mix de dispositivos, páginas por señales de frustración, scroll depth en páginas estratégicas.

**DataForSEO:** resumen de dominio, resumen de backlinks, top competidores orgánicos, distribución de keywords orgánicas, top páginas orgánicas, stack tecnológico.

## Output File Structure

1. **Metadatos** — debe incluir `Fecha de extracción` y `Fecha de referencia` como campos obligatorios, más: nombre del reporte, versión, sitio/propiedad, mercado, idioma, moneda, cantidad de URLs estratégicas, fuentes de datos, modo de extracción, y declaraciones explícitas de que no se incluyen interpretaciones ni recomendaciones
2. **Inventario de fuentes** — lista cada fuente consultada, datasets extraídos, ventanas de tiempo, granularidad, cantidad de filas, y fuentes no disponibles con su estado
3. **URLs estratégicas** — tabla con etiqueta, URL y tipo de página
4. **Google Analytics 4** — resumen por período, adquisición por canal (28d + 90d), mix de dispositivos (28d + 90d), top landing pages (28d + 90d), eventos de conversión (28d + 90d), tendencia mensual (12 meses)
5. **Google Search Console** — resumen por período, top queries por clics (28d + 90d), queries con posición promedio 4-20 (28d + 90d), top páginas por clics (28d + 90d), **top 20 páginas por clics (últimos 90 días) con clics, CTR e impresiones**, tendencia mensual (12 meses), resumen de cobertura, detalle de cobertura
6. **Google PageSpeed / Core Web Vitals** — snapshots por URL estratégica × dispositivo, field data cuando esté disponible
7. **Microsoft Clarity** — resumen por período, mix de dispositivos (28d + 90d), páginas por señales de frustración (28d + 90d), scroll depth en páginas estratégicas (28d + 90d)
8. **DataForSEO** — resumen de dominio, resumen de backlinks, top competidores orgánicos, distribución de keywords orgánicas, top páginas orgánicas, stack tecnológico
9. **Definiciones de métricas** — definiciones breves de cada métrica usada en el reporte

## Construction Rules

1. **Keep tables separated by source.** Do not mix data from different tools in the same table. You may relate them by URL, period, device, or channel — but do not write conclusions.

2. **Preserve original grain.** If the MCP returns data by site, URL, query, device, or channel — keep that grain in the table.

3. **Limit table size.** 10-30 rows per table, ordered mechanically (by clicks, sessions, etc.), except for the GSC top 20 pages table (últimos 90 días) which must always show exactly 20 rows. If tables are larger, truncate and note the cutoff.

4. **Use consistent period names in Spanish.** Always: `Últimos 28 días`, `Últimos 90 días`, `Últimos 6 meses`, `Últimos 12 meses`, `Estado actual`, `Snapshot más reciente`.

5. **Include a glossary in Spanish.** Close the document with brief metric definitions written in Spanish neutro.

## Construction Flow

### Step 1: Define base inputs

Resolve the client root (walk up to `contexto/`) and check if `contexto/configuracion.md` exists. If so, read it. If it only exists under a legacy name/location (e.g. a `config-snapshot.md`, `context/snapshot-config.md`, or a `reportes/contexto/{mes}/` layout), read it there and offer to migrate to `contexto/configuracion.md`.

If not found anywhere, attempt auto-detection for: main domain, market, language. For source identifiers (GA4 property, GSC site URL, Clarity project ID, DataForSEO target domain), ask the user.

**Ask the user for the reference date** — the date from which all relative time windows will be calculated, and which sets the period folder `{periodo}` = `YYYY-MM`. Do this before any data extraction. If a previous reference date exists, confirm whether to reuse or update it.

If there is no curated list of strategic URLs, derive one automatically from: most visited pages, main landing pages, key business pages (home, pricing, product, demo, contact). Keep it manageable: 10-20 URLs.

Save or update `contexto/configuracion.md` with the stable identifiers and strategic URLs.

### Step 2: Run source availability preflight

Before extracting data, test each source and classify its status as: disponible, no configurada, fallo de acceso, configurada sin datos, no compatible.

If any source is unavailable, notify the user specifying: which platform failed, what identifier is missing, whether the problem is configuration or access.

Ask for an explicit decision: continue without that source, or fix before proceeding.

If the user decides to continue, record the absence factually in the Inventario de fuentes.

### Step 3: Extract datasets per source

Run MCP queries separately per source and time window. Do not transform to narrative text at this stage.

For GSC, extract a dedicated query for the top 20 pages by clicks for the last 90 days, including clicks, CTR, and impressions per page.

### Step 4: Clean and normalize

Apply only these transformations: visual rounding, period name standardization (use Spanish names), row ordering, long table truncation, column header unification.

Do not add interpretation.

### Step 5: Render to Markdown

Build the file using fixed headings in Spanish, markdown tables, visible period labels in Spanish, and consistent URL formatting.

### Step 6: Editorial verification

Confirm:
- No recommendations present
- No evaluative adjectives
- No invented scores
- All tables have clear source and period
- Strategic URLs are included in PageSpeed
- Unavailable sources are listed with status and factual note
- `Fecha de extracción` y `Fecha de referencia` are present in Metadatos
- GSC section includes the top 20 pages table (últimos 90 días) with clicks, CTR, and impressions
- All section headers, table headers, and field labels are in Spanish neutro

## Related Skills

- **page-snapshot** — factual snapshot for a single URL
- **site-context** — strategic context built on top of this snapshot
- **audience-demand-evaluation** — demand and channel-fit assessment per audience
- **seo-audit** — SEO diagnosis that consumes this snapshot
- **page-cro** — conversion analysis that consumes this snapshot
- **ai-seo** — AEO/GEO audit that consumes this snapshot for acquisition context
