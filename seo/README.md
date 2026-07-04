# SEO Suite

Suite de SEO de 7 skills que trabajan de forma encadenada: primero extraen datos
factuales y contexto estratégico, y luego los usan para diagnosticar, evaluar demanda de
audiencia, optimizar conversión y optimizar para motores de búsqueda de IA (AEO/GEO).
Todo el output se genera en **español neutro** y se guarda dentro de la carpeta
`contexto/` del proyecto activo, de modo que cada skill puede leer lo que produjeron los
anteriores.

## Skills

| Skill | Qué hace |
|-------|----------|
| `site-context` | Crea y mantiene el contexto estratégico del sitio (positioning, audiencia, mensajes, info de negocio) → `contexto/contexto-sitio.md` |
| `site-snapshot` | Snapshot factual de datos de un dominio completo (GA4, GSC, PageSpeed, Clarity, DataForSEO) → `contexto/snapshot-sitio.md` |
| `page-snapshot` | Snapshot factual de datos de una URL específica → `contexto/paginas/snapshot-pagina-{slug}.md` |
| `seo-audit` | Audita y diagnostica problemas SEO (crawlability, indexación, performance técnica, on-page, calidad de contenido) |
| `audience-demand-evaluation` | Evalúa si una audiencia objetivo es alcanzable por búsqueda orgánica o necesita canales alternativos → `contexto/contexto-adquisicion-audiencia.md` |
| `page-cro` | Optimiza la conversión de páginas de marketing (homepage, landing, pricing, feature pages, blog) |
| `ai-seo` | Audita contenido (publicado o borrador) para que motores de IA lo citen — AEO/GEO, AI Overviews, menciones en LLMs — y verifica visibilidad real → `contexto/paginas/auditoria-aeo-{slug}.md` |

## Orden de uso recomendado

Los skills dependen de los archivos de contexto que generan otros. El flujo típico:

```
site-context  ─┐
site-snapshot ─┼─→ seo-audit
               └─→ audience-demand-evaluation

page-snapshot ───→ page-cro / ai-seo
```

1. **`site-context`** + **`site-snapshot`** — sientan la base (estrategia + datos del dominio).
2. **`seo-audit`** y **`audience-demand-evaluation`** — consumen esa base para diagnosticar y evaluar demanda.
3. **`page-snapshot`** → **`page-cro`** / **`ai-seo`** — para trabajo a nivel de página, primero el snapshot de la URL y luego la optimización de conversión o la auditoría AEO/GEO.
4. **`ai-seo` en modo borrador** — audita contenido aún no publicado (gate pre-publicación) sin necesidad de snapshot.

Los skills de snapshot solo extraen datos (no interpretan); los de análisis (audit, cro,
audience, ai-seo) sí diagnostican y recomiendan, apoyándose en los snapshots para evitar sesgos.

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

Como regla, solo los skills de snapshot consultan MCPs. Hay **dos excepciones acotadas**,
ambas con límites de ejecución explícitos y datos que no existen en ningún snapshot:
`audience-demand-evaluation` (validación de demanda: volumen y competencia) y `ai-seo`
(verificación de visibilidad real en motores de IA vía los endpoints `ai_optimization` de
DataForSEO y SERP; incluye un gate de confirmación antes de gastar llamadas facturables).

## Output y estructura de contexto

Cada proyecto o dominio tiene su propia carpeta raíz con un subdirectorio `contexto/`:

```text
{dominio-o-proyecto}/
  contexto/
    contexto-sitio.md
    snapshot-sitio.md
    config-snapshot.md
    contexto-adquisicion-audiencia.md
    paginas/
      snapshot-pagina-{slug}.md
      auditoria-aeo-{slug}.md
      auditoria-aeo-borrador-{slug}.md
```

Los skills buscan primero en el `contexto/` local del proyecto activo. Todo el contenido
analítico canónico vive en Markdown y está escrito en español neutro (etiquetas y encabezados
traducidos; los valores de datos crudos se conservan en su idioma original).

**Retrocompatibilidad:** los nombres en inglés (`context/`, `site-context.md`,
`site-snapshot.md`, `snapshot-config.md`, `audience-acquisition-context.md`,
`pages/page-snapshot-{slug}.md`) son la convención anterior. Al leer, cada skill busca
primero la ruta en español y, si no existe, usa la equivalente en inglés sugiriendo
renombrar. Al escribir se usa siempre la ruta en español — salvo que el árbol del proyecto
siga en inglés, en cuyo caso el skill ofrece migrar antes de escribir.
