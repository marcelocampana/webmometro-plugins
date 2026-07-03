# SEO Suite

Suite de SEO de 6 skills que trabajan de forma encadenada: primero extraen datos
factuales y contexto estratégico, y luego los usan para diagnosticar, evaluar demanda de
audiencia y optimizar conversión. Todo el output se genera en **español neutro** y se
guarda dentro de la carpeta `context/` del proyecto activo, de modo que cada skill puede
leer lo que produjeron los anteriores.

## Skills

| Skill | Qué hace |
|-------|----------|
| `site-context` | Crea y mantiene el contexto estratégico del sitio (positioning, audiencia, mensajes, info de negocio) → `context/site-context.md` |
| `site-snapshot` | Snapshot factual de datos de un dominio completo (GA4, GSC, PageSpeed, Clarity, DataForSEO) → `context/site-snapshot.md` |
| `page-snapshot` | Snapshot factual de datos de una URL específica → `context/pages/page-snapshot-{slug}.md` |
| `seo-audit` | Audita y diagnostica problemas SEO (crawlability, indexación, performance técnica, on-page, calidad de contenido) |
| `audience-demand-evaluation` | Evalúa si una audiencia objetivo es alcanzable por búsqueda orgánica o necesita canales alternativos → `context/audience-acquisition-context.md` |
| `page-cro` | Optimiza la conversión de páginas de marketing (homepage, landing, pricing, feature pages, blog) |

## Orden de uso recomendado

Los skills dependen de los archivos de contexto que generan otros. El flujo típico:

```
site-context  ─┐
site-snapshot ─┼─→ seo-audit
               └─→ audience-demand-evaluation

page-snapshot ───→ page-cro
```

1. **`site-context`** + **`site-snapshot`** — sientan la base (estrategia + datos del dominio).
2. **`seo-audit`** y **`audience-demand-evaluation`** — consumen esa base para diagnosticar y evaluar demanda.
3. **`page-snapshot`** → **`page-cro`** — para trabajo a nivel de página, primero el snapshot de la URL y luego la optimización de conversión.

Los skills de snapshot solo extraen datos (no interpretan); los de análisis (audit, cro,
audience) sí diagnostican y recomiendan, apoyándose en los snapshots para evitar sesgos.

## Prerrequisitos (MCP)

Este plugin **no empaqueta un `.mcp.json`**. Los skills leen datos a través de servidores
MCP que debes tener configurados y autenticados por tu cuenta:

- **DataForSEO** (`dataforseo`) — datos de SERP, keywords, backlisks, on-page, Lighthouse.
- **Google Search Console** (`gsc`) — clics, impresiones, posiciones, cobertura de indexación.
- **Google Analytics 4** (`analytics-mcp`) — tráfico, adquisición por canal, comportamiento.
- **PageSpeed Insights / Microsoft Clarity** — métricas de performance y comportamiento; se
  consultan según disponibilidad (por MCP o extracción manual). Si no están disponibles, el
  skill lo indica y continúa con las fuentes que sí tenga.

Cada servidor requiere sus propias credenciales (API keys de DataForSEO, OAuth para
GSC/GA4). Configúralos vía `claude mcp` o `/mcp` en una sesión interactiva antes de usar la
suite. Si falta una fuente, los skills degradan de forma explícita en lugar de fallar.

## Output y estructura de contexto

Cada proyecto o dominio tiene su propia carpeta raíz con un subdirectorio `context/`:

```text
{dominio-o-proyecto}/
  context/
    site-context.md
    site-snapshot.md
    audience-acquisition-context.md
    pages/
      page-snapshot-{slug}.md
```

Los skills buscan primero en el `context/` local del proyecto activo. Todo el contenido
analítico canónico vive en Markdown y está escrito en español neutro (etiquetas y encabezados
traducidos; los valores de datos crudos se conservan en su idioma original).
