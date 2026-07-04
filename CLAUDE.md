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
- **seo** — skills-only: a 7-skill SEO suite (snapshots → audit/CRO/audience/AI-search).

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

## Skills chain through shared context files

Skills are not standalone — within a plugin they pass data via Markdown files under a
project's `contexto/` directory (the skill looks in the *active project's* local `contexto/`
first, not this repo). Context file names are Spanish-first with an English legacy fallback
(`contexto/contexto-sitio.md` ← `context/site-context.md`, `contexto/snapshot-sitio.md` ←
`context/site-snapshot.md`, `contexto/paginas/snapshot-pagina-{slug}.md` ←
`context/pages/page-snapshot-{slug}.md`, etc.): skills read Spanish first, fall back to
English suggesting a rename, and always write Spanish. In the **seo** plugin specifically:

```
site-context + site-snapshot ─→ seo-audit / audience-demand-evaluation
page-snapshot ────────────────→ page-cro / ai-seo
```

Snapshot skills (`site-snapshot`, `page-snapshot`) are strictly **data-only** — no
interpretation, recommendations, or composite scores — because downstream analytical skills
(`seo-audit`, `page-cro`, `audience-demand-evaluation`, `ai-seo`) read them and would inherit
any bias. Preserve that separation when editing SEO skills. As a rule only snapshot skills
query MCPs; the two bounded exceptions (with explicit execution limits) are
`audience-demand-evaluation` (demand validation) and `ai-seo` (real AI-visibility
verification, gated behind a cost confirmation).

## MCP dependencies

MCP servers are **not** bundled except in brand-voice-pro (`brand-voice-pro/.mcp.json`, HTTP
endpoints for Notion/Atlassian/Box/Figma/Gong/Granola). The **seo** plugin deliberately ships
no `.mcp.json`: it relies on servers the user configures globally (DataForSEO, GSC/`gsc`,
GA4/`analytics-mcp`, plus PageSpeed/Clarity), documented as prerequisites in `seo/README.md`.
When a data source is missing, SEO skills degrade explicitly rather than fail.

## Adding or editing a plugin

1. Create `<plugin>/.claude-plugin/plugin.json` and add the matching entry to
   `.claude-plugin/marketplace.json` (respect the two sync invariants above).
2. Validate every manifest you touch:
   `python3 -m json.tool .claude-plugin/marketplace.json` and the plugin's `plugin.json`.
3. Match the closest existing plugin's shape: skills-only plugins (design-system, seo) have
   no `agents/`, `commands/`, or `.mcp.json` — skills auto-activate via their `description`.
4. Bump `version` in **both** the plugin's `plugin.json` and its `marketplace.json` entry
   together.

## Git

`main` is the default branch. Commit only when the user asks; if on `main`, branch first.
Note `.gitignore` only excludes `.DS_Store`, so avoid committing stray macOS metadata.
