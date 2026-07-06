# SEO Suite

Suite de SEO de 7 skills que trabajan de forma encadenada: primero extraen datos
factuales y contexto estratégico, y luego los usan para diagnosticar, evaluar demanda de
audiencia, optimizar conversión y optimizar para motores de búsqueda de IA (AEO/GEO).
Todo el output se genera en **español neutro**. Los skills operan dentro de un **workspace de
cliente compartido** con otros plugins: el contexto estratégico y de marca vive una sola vez
en la raíz del cliente (`contexto/`), y los datos e informes SEO viven por período bajo
`web/seo/` (ver "Workspace y estructura"). La convención de workspace está documentada en el
`CLAUDE.md` raíz del repositorio de plugins.

## Skills

| Skill | Qué hace |
|-------|----------|
| `site-context` | Crea y mantiene el contexto estratégico del sitio (positioning, audiencia, mensajes, info de negocio) → `contexto/sitio.md` |
| `site-snapshot` | Snapshot factual de datos de un dominio completo (GA4, GSC, PageSpeed, Clarity, DataForSEO) → `web/seo/datos/{periodo}/snapshot-sitio.md` |
| `page-snapshot` | Snapshot factual de datos de una URL específica → `web/seo/datos/{periodo}/paginas/snapshot-pagina-{slug}.md` |
| `seo-audit` | Audita y diagnostica problemas SEO (crawlability, indexación, performance técnica, on-page, calidad de contenido) → `web/seo/informes/{periodo}/auditoria-seo.md` |
| `audience-demand-evaluation` | Evalúa si una audiencia objetivo es alcanzable por búsqueda orgánica o necesita canales alternativos → `contexto/audiencia-canales.md` |
| `page-cro` | Optimiza la conversión de páginas de marketing (homepage, landing, pricing, feature pages, blog) → `web/seo/informes/{periodo}/cro-{slug}.md` |
| `ai-seo` | Audita contenido (publicado o borrador) para que motores de IA lo citen — AEO/GEO, AI Overviews, menciones en LLMs — y verifica visibilidad real → `web/seo/informes/{periodo}/auditoria-aeo-{slug}.md` |

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

### PageSpeed / Core Web Vitals de campo (opcional)

Los snapshots (`site-snapshot`, `page-snapshot`) extraen PageSpeed con el script compartido
`scripts/pagespeed_field.py` (PSI v5 + datos de campo CrUX, solo stdlib, sin `pip install`). Para
obtener **datos de campo reales (CrUX)** necesita una Google API key gratuita de PageSpeed
Insights. **La key nunca vive en el plugin** — se resuelve por convención desde fuera del repo,
en este orden:

1. `GOOGLE_API_KEY` — la key en crudo, como variable de entorno.
2. `CLAUDE_SEO_GOOGLE_API` — variable de entorno con la **ruta** a un archivo JSON (o a un
   directorio que contenga `google-api.json`). Es el override para guardar la credencial en otra
   ubicación sin tocar el código — útil al compartir el plugin.
3. `~/.config/claude-seo/google-api.json` — **ubicación por defecto**. Si guardas la key aquí, el
   script la encuentra sin ninguna configuración extra (ni env var ni dotfiles).

**Setup por defecto (recomendado, cero mantenimiento):**

1. Botón **"Get a Key"** en https://developers.google.com/speed/docs/insights/v5/get-started
   (crea el proyecto y habilita la PageSpeed Insights API en un paso). Copia la cadena `AIza…`.
2. Guárdala en la ubicación por defecto, con permisos restrictivos:
   ```bash
   mkdir -p ~/.config/claude-seo
   printf '{\n  "api_key": "TU_KEY"\n}\n' > ~/.config/claude-seo/google-api.json
   chmod 600 ~/.config/claude-seo/google-api.json
   ```
3. Verifica (una URL, sin costo) — debe devolver `field` (CrUX) además de `lab`:
   ```bash
   python3 seo-suite/scripts/pagespeed_field.py https://www.google.com --strategy mobile --json
   ```

**Guardar la key en otra ubicación** (p. ej. una carpeta de credenciales propia): deja el JSON
donde quieras y exporta la ruta en tu perfil de shell (`~/.zshenv`, `~/.zshrc`…):
```bash
export CLAUDE_SEO_GOOGLE_API="/ruta/a/tu/carpeta-de-credenciales"   # dir con google-api.json
# o directo al archivo:
export CLAUDE_SEO_GOOGLE_API="/ruta/a/tu/google-api.json"
```

**Mantenimiento:** ninguno en la práctica. Las API keys de Google **no caducan** y el tier
gratuito (25.000 solicitudes/día) sobra para snapshots. Solo la reemplazas si decides **rotarla**
por seguridad (generas otra y sobrescribes el archivo).

**Sin key**, el script degrada y los snapshots caen al fallback
`mcp__dataforseo__on_page_lighthouse` (Lighthouse **lab-only**, sin CrUX), registrándolo en el
Inventario de fuentes. La interpretación de estos datos (umbrales, rating bueno/malo) vive en la
capa analítica: `seo-audit/references/rendimiento-web.md`.

**Detalle de la API a tener en cuenta:** CrUX entrega el CLS de campo **multiplicado por 100**
(un `5` crudo en la respuesta = un CLS de 0.05). El umbral se evalúa contra 0.1 en la capa
analítica; el script reporta el valor crudo de Google sin transformarlo.

Como regla, solo los skills de snapshot consultan MCPs. Hay **dos excepciones acotadas**,
ambas con límites de ejecución explícitos y datos que no existen en ningún snapshot:
`audience-demand-evaluation` (validación de demanda: volumen y competencia) y `ai-seo`
(verificación de visibilidad real en motores de IA vía los endpoints `ai_optimization` de
DataForSEO y SERP; incluye un gate de confirmación antes de gastar llamadas facturables).

## Workspace y estructura

Los skills operan en un **workspace de cliente compartido** por varios plugins. Regla: lo
compartido vive una sola vez en la raíz del cliente bajo `contexto/`; cada dominio tiene su área;
nada se duplica.

```text
{cliente}/
  contexto/                     ← COMPARTIDO (todos los plugins leen; nadie duplica)
    sitio.md                       estrategia, audiencia, objetivos            (site-context)
    configuracion.md               IDs GA4/GSC/Clarity/DataForSEO + URLs        (snapshots)
    audiencia-canales.md           demanda y channel-fit                       (audience-demand)
    marca/                         voz de marca, guidelines                    (brand-voice-pro)
    antecedentes/                  informes previos / conocimiento del equipo  (aporta: equipo)
  recursos/                     ← COMPARTIDO (logos, fuentes, iconos, imágenes)
  conocimiento/                 ← COMPARTIDO (bibliotecas de fuentes para citar/redactar; p. ej. revista-roc/)
  web/seo/                      ← DOMINIO SEO
    datos/{periodo}/               solo datos: snapshot-sitio.md, paginas/snapshot-pagina-{slug}.md
    informes/{periodo}/            interpretación: auditoria-seo.md, cro-{slug}.md, auditoria-aeo-{slug}.md
    tracking/                      registro de cambios SEO (seo-change-tracker)
```

- **`{periodo}` = `YYYY-MM`**, derivado de la fecha de referencia. Cada ciclo de trabajo escribe
  su propia carpeta de período; los períodos anteriores quedan como histórico.
- **`contexto/` es vivo** (no versionado); los datos e informes se versionan por período.
- Todo el contenido analítico vive en Markdown, en español neutro (etiquetas y encabezados
  traducidos; los valores de datos crudos se conservan en su idioma original).
- **Sin duplicación:** la voz de marca vive solo en `contexto/marca/`; el contexto del sitio solo
  en `contexto/sitio.md`. Los demás plugins leen por puntero, no copian.
- **Resolver flexible / migración:** los nombres canónicos son español bajo las rutas de arriba.
  Si un proyecto usa una estructura o nombres antiguos (p. ej. `contexto/contexto-sitio.md`, un
  legado `context/…`, o un `reportes/contexto/{mes}/…`), cada skill los resuelve por rol y ofrece
  migrar a las rutas canónicas antes de escribir; nunca asume un nombre alterno fijo.
