# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a **Claude Code plugin marketplace** (`webmometro-plugins`), not an application.
There is no build, test, or lint step — the "artifacts" are Markdown skills/agents/commands
and JSON manifests that Claude Code loads. Work here means authoring or editing those files
and keeping the manifests valid and consistent.

The marketplace currently ships three plugins, all authored in **Spanish neutro** for
user-facing output (skills instruct their output language explicitly):

- **brand-voice-pro** — full-stack plugin: skills + agents + commands + MCP servers.
- **design-system** — skills-only: design-system audit/docs + social carousel generation.
- **seo-suite** — skills-only: an 8-skill SEO suite (snapshots → audit/CRO/audience/AI-search, plus change tracking).

## Layout & manifest hierarchy

```
.claude-plugin/marketplace.json     ← registry: one entry per plugin (name, source, version, keywords)
<plugin>/.claude-plugin/plugin.json ← per-plugin metadata (name, displayName, version, author, keywords)
<plugin>/.mcp.json                  ← optional; only when the plugin needs MCP servers (brand-voice-pro only)
<plugin>/skills/<skill>/SKILL.md    ← the core unit; frontmatter drives auto-activation
<plugin>/skills/<skill>/references/ ← supporting docs a skill reads on demand
<plugin>/agents/<name>.md           ← optional autonomous subagents (brand-voice-pro only)
<plugin>/commands/<name>.md         ← optional slash-command entry points (brand-voice-pro only)
<plugin>/settings/*.local.md.example← optional per-project config template the user copies into .claude/
```

Two invariants tie the manifests together — **always keep them in sync**:
1. A plugin's `name` must be identical in `marketplace.json` and its `plugin.json`.
2. `marketplace.json` `source: "./<plugin>"` must point at an existing folder, and `version`
   should match the plugin's own `plugin.json` `version`.

## Frontmatter conventions

- **SKILL.md**: YAML frontmatter with `name` and `description`. The `description` is the
  activation trigger — it enumerates the phrases/intents that should invoke the skill, so it
  is long and specific by design. Optional: `argument-hint` (for command-invoked skills) and
  `metadata.version` (semver, e.g. `metadata: { version: 2.0.0 }`).
- **agents/*.md**: `name` + a `description` that embeds `<example>`/`<commentary>` blocks
  showing when to delegate to the agent.
- **commands/*.md**: `description` + `argument-hint`; body references `$ARGUMENTS` and tells
  Claude to follow a named skill's workflow, then delegate to agents. Commands are thin entry
  points — the real logic lives in the skill.

The pattern in brand-voice-pro is **command → skill → agent(s)**: a slash command orients the
user and invokes a skill, and the skill delegates heavy/autonomous work to subagents.

## Shared client workspace (convention for all plugins)

Skills are not standalone — they pass data via Markdown files inside a **shared client
workspace** that several plugins (seo-suite, brand-voice-pro, content, RRSS/design) read and
write. The governing rule: **shared truth lives once at the client root; each domain has its own
work area; nothing is duplicated.** Skills resolve the client root by walking up from the active
directory until they find `contexto/` (they operate in the *active project*, not this repo).

```text
{cliente}/
  contexto/                     ← COMPARTIDO (todos los plugins leen; nadie duplica)
    sitio.md                       estrategia/audiencia/objetivos   (produce: site-context)
    marca/                         voz de marca, guidelines         (produce: brand-voice-pro)
    audiencia-canales.md           demanda y channel-fit            (produce: audience-demand)
    configuracion.md               IDs GA4/GSC/Clarity/DataForSEO + URLs
    antecedentes/                  informes previos del equipo (solo lectura; input cualitativo)
    seo-tracking/                  cambios SEO — continuo, sin período (produce: seo-change-tracker;
                                     leen: skills SEO + brand-voice-pro)
  recursos/                     ← COMPARTIDO (logos, fuentes, iconos, imágenes)
  conocimiento/                 ← COMPARTIDO (bibliotecas de fuentes para citar/redactar; p. ej. revista-roc/)
  web/seo/                      ← DOMINIO SEO
    datos/{periodo}/               datos factuales (snapshots)      versionado por período YYYY-MM
    informes/{periodo}/            interpretación (auditoría/CRO/AI-SEO)
  web/contenido/                ← DOMINIO CONTENIDO   ·   rrss/  ← DOMINIO RRSS/diseño
```

Reglas clave para editar skills:
- **Nombres canónicos en español**; los archivos compartidos viven una sola vez en `contexto/` y
  los demás plugins los leen **por puntero** (p. ej. la voz de marca vía el campo `Archivo de
  guías:` en `contexto/sitio.md`), nunca copiando.
- **Resolver flexible:** si un proyecto usa nombres/ubicaciones antiguas (`contexto/contexto-sitio.md`,
  un legado `context/…`, o un `reportes/contexto/{mes}/…`), resolver por rol y ofrecer migrar; no
  asumir un nombre alterno fijo.
- **`contexto/` es vivo** (no versionado); datos e informes se versionan por período `YYYY-MM`.

Flujo de la suite SEO:

```
site-context + site-snapshot ─→ seo-audit / audience-demand-evaluation
page-snapshot ────────────────→ page-cro / ai-seo
contexto/seo-tracking/ ───────→ (leído por los skills analíticos antes de recomendar/reportar)
seo-change-tracker ───────────→ registra la ejecución de los cambios recomendados
```

The analytical skills (`seo-audit`, `page-cro`, `ai-seo`, `audience-demand-evaluation`) read
`contexto/seo-tracking/` **before** producing recommendations: to avoid re-proposing a change already
made, to verify whether a proposed fix was implemented, and to fold implemented-but-unaccounted
changes into the diagnosis as insight. `seo-change-tracker` registers the execution of those changes
(with `accion_origen` linking a change back to the audit action that proposed it). Generar un reporte
del tracker es una **lectura agregada**, no un registro.

Snapshot skills (`site-snapshot`, `page-snapshot`) are strictly **data-only** — no
interpretation, recommendations, or composite scores — because downstream analytical skills
(`seo-audit`, `page-cro`, `audience-demand-evaluation`, `ai-seo`) read them and would inherit
any bias. Snapshots and site-context never read `contexto/antecedentes/` nor
`contexto/seo-tracking/` (both are interpretive). Preserve that separation when editing SEO skills.
As a rule only snapshot skills query MCPs; the three bounded exceptions (with explicit execution
limits) are `audience-demand-evaluation` (demand validation), `ai-seo` (real AI-visibility
verification, gated behind a cost confirmation), and `seo-change-tracker` (baseline/checkpoint
capture, bounded to the sources of the changed area within the configured time window).

Cross-plugin: the brand voice guidelines home is `contexto/marca/brand-voice-guidelines.md`
(produced by **brand-voice-pro**), and the SEO analytical skills read it only as a guardrail,
delegating on-brand copy production back to brand-voice-pro's `brand-voice-enforcement`.

## MCP dependencies

MCP servers are **not** bundled except in brand-voice-pro (`brand-voice-pro/.mcp.json`, HTTP
endpoints for Notion/Atlassian/Box/Figma/Gong/Granola). The **seo-suite** plugin deliberately ships
no `.mcp.json`: it relies on servers the user configures globally (DataForSEO, GSC/`gsc`,
GA4/`analytics-mcp`, plus PageSpeed/Clarity), documented as prerequisites in `seo-suite/README.md`.
When a data source is missing, SEO skills degrade explicitly rather than fail.

## Adding or editing a plugin

1. Create `<plugin>/.claude-plugin/plugin.json` and add the matching entry to
   `.claude-plugin/marketplace.json` (respect the two sync invariants above).
2. Validate every manifest you touch:
   `python3 -m json.tool .claude-plugin/marketplace.json` and the plugin's `plugin.json`.
3. Match the closest existing plugin's shape: skills-only plugins (design-system, seo-suite) have
   no `agents/`, `commands/`, or `.mcp.json` — skills auto-activate via their `description`.
4. Bump `version` in **both** the plugin's `plugin.json` and its `marketplace.json` entry
   together.

## Git

`main` is the default branch. Commit only when the user asks; if on `main`, branch first.
Note `.gitignore` only excludes `.DS_Store`, so avoid committing stray macOS metadata.
