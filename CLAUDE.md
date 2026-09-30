# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a **Claude Code plugin marketplace** (`webmometro-plugins`), not an application.
There is no build, test, or lint step — the "artifacts" are Markdown skills/agents/commands
and JSON manifests that Claude Code loads. Work here means authoring or editing those files
and keeping the manifests valid and consistent.

The marketplace currently ships four plugins, all authored in **Spanish neutro** for
user-facing output (skills instruct their output language explicitly):

- **brand-voice-pro** — full-stack plugin: skills + agents + commands + MCP servers.
- **design-system** — skills-only: design-system audit/docs + social carousel generation.
- **seo-suite** — skills-only: a 10-skill SEO suite (snapshots → audit/CRO/audience/AI-search, plus content clusters, landing blueprints and change tracking).
- **utils** — skills-only: general-purpose personal utilities (a task system). **Toggl 2.0 is the single task list for every project** (utils 4.0.0): `tarea` creates, opens (In Progress), pauses and closes tasks in Toggl; `tarea-repo` adds the repo ceremony — a branch per task cut from and merged back into the repo's **target branch** (`toggl.md` § Rama destino, `main` by default, e.g. `preview` for a test branch; promoting it to `main` is a separate, separately approved act), a one-confirmation close chain (Toggl, history, commit, merge) — **the merge always needs the user's approval given after seeing the result; no prior "finish it"/"don't ask me" nor the approved plan replaces it, and it is not configurable** (utils 4.8.0); commits on the task branch are save points and need nothing — for tasks whose Toggl project is linked from a repo's `tareas/toggl.md` (marker `<!-- tarea: toggl · proyecto … -->`, plus the repo's areas and rules). A repo keeps only its memory: `tareas/historial/AAAA-MM.md` (what was done and why, grouped by area — the context Claude reads), `auditoria.md` and `toggl.md`, plus two local lists that never reach Toggl (utils 5.0.0): `tareas/por-revisar.md` — **the inbox**: whatever is noted and not yet decided; it only stores, and reviewing is a separate step that turns an entry into a user task in Toggl, delegates it to Claude or drops it — and `tareas/para-claude.md`, what a review delegated to Claude (run on request as `pc-<slug>`, with its plan, branch and history; `modo-claude.md`). Changes to those two files outside a task are the one direct commit allowed on the target branch (`tareas: bandeja`). Projects without a repo keep both lists in `~/Obsidian/global/`. The user's pending list is never in the repo, and repos still on the old `tareas.md` / `revisar.md` / `secciones.md` format are moved with `tarea-repo --migrar` (`scripts/migrar_a_toggl.py`, read-only until the user approves). **A task's area is a Toggl tag** (utils 4.3.0 reverted the earlier "no sections" rule at the user's request), repeated as the first line of its description (`Área: …`) as a fallback for scripts; `cola.py` takes the area from the non-cross-cutting tag first. No subprojects. Cross-cutting tag: `imprevisto` (`por-revisar` and `claude` survive only on pre-5.0.0 items). **Toggl organizes the user; the plan organizes Claude** (utils 4.7.0): a task is the user's goal; only what the user must do himself goes as subtasks (one level, timed by the user with the Toggl app); Claude's steps never go to Toggl — they live in the task's plan, `tareas/planes/<id>-<slug>.md` (skill and context per step), approved once, chained without asking, marked done with evidence, and summarized in 2–3 lines when the task is resumed. The repo close chain ends with merge **and push**. **Tasks are read through `tarea/scripts/cola.py`**, never raw `tasks list`: each raw task is ~2,000 chars; `cola.py` calls the Focus API with the connector's OAuth session (`~/.toggl/focus-tools.json`; Toggl 2.0 accepts no API token) and **never refreshes it** (refreshing rotates the refresh token and would log the connector out), keeps only the useful fields plus full description and notes, and caches the copy (`cola.py invalidar` after any write). The shared infrastructure (`presencia.py`, `cola.py`, install assets) stays under `tarea/` so the launch agent and hook paths never move. **Toggl is only the user's work; nothing of Claude's goes there** (utils 5.0.0, reverting 4.4.0's Claude-time-in-Toggl). `tarea/scripts/presencia.py` reads Claude Code's local session transcripts and attributes each stretch of Claude's work to the repo whose files its tools touch — never to the folder the session was opened in — and `presencia.py asentar` writes it to a local ledger, `~/Obsidian/global/claude/registro-tiempo/<toggl-project-slug>-AAAA-MM.md` (one row per stretch: repo, the task open in that repo or `—`, minutes, minutes alone), idempotently, on every close and once a day from the launchd agent (Claude Code deletes transcripts after 30 days). `balance` reads it through `presencia.py claude`, which adds the not-yet-settled tail without writing. The user times his own work with the Toggl app, and `presencia.py verificar` checks those entries against his Mac activity (late start, timer left running, pauses, main apps) — read-only. The nightly routine is optional and paused. The user's own time stays local and is never summed with project time: the same stdlib script, run every minute by launchd and by a `UserPromptSubmit` hook, records keyboard/mouse idle time, the frontmost app and which session each message went to (attention follows the repo that session was working in), and raises the pause alert. `Coste` is estimated from closed-task history (matched by task *family* — verb + object — never by area mean). Project time (Toggl) and the user's own time (presence) are **never summed together**. `agenda` is the read-only daily view over all projects (the copy plus Toggl `capacities` for the working day; the `agenda.md` config keeps only the repo registry, which orders projects) — **it never writes to Toggl or any repo**, which is what lets it run unattended from a routine. `balance` is the read-only weekly review over both times, plus plan-versus-reality, estimation bias, automation candidates, health and app usage. `plan-semanal` is the only skill that writes a plan: it assigns each task a day in Toggl (`start_date` = `end_date`, plus `estimated_mins`) with the user's approval and snapshots the original version locally (`presencia.py plan guardar`), because Toggl keeps only the latest dates and plan-versus-reality must compare against Monday's plan. `tarea`, `tarea-repo`, `agenda`, `balance`, and `plan-semanal` all use a deliberately thin SKILL.md core that dispatches to one per-mode reference — keep the core under ~2.4k tokens and each reference under ~1.7k. **The core ceiling measures the body, not the frontmatter**: a skill's `description` is the activation trigger, is long and specific by design, and is loaded as listing metadata rather than as instructions, so it does not compete for the core's budget. Measure with `wc -c` on the text after the closing `---` (4 chars ≈ 1 token).

## Layout & manifest hierarchy

```
.claude-plugin/marketplace.json     ← registry: one entry per plugin (name, source, version, keywords)
<plugin>/.claude-plugin/plugin.json ← per-plugin metadata (name, displayName, version, author, keywords)
<plugin>/.mcp.json                  ← optional; only when the plugin needs MCP servers (brand-voice-pro only)
<plugin>/skills/<skill>/SKILL.md    ← the core unit; frontmatter drives auto-activation
<plugin>/skills/<skill>/references/ ← supporting docs a skill reads on demand
<plugin>/skills/<skill>/scripts/    ← executable helpers (stdlib-only, invoked from SKILL.md)
<plugin>/agents/<name>.md           ← optional autonomous subagents (brand-voice-pro only)
<plugin>/commands/<name>.md         ← optional slash-command entry points (brand-voice-pro only)
<plugin>/settings/*.local.md.example← optional per-project config template the user copies into .claude/
tareas/                             ← this repo's own task queue, managed by the `tarea` skill
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
    plantilla-landing.md           esqueleto de slots de landing    (produce: landing-blueprint)
    configuracion.md               IDs GA4/GSC/Clarity/DataForSEO + URLs, y los destinos de
                                     publicación: repo del sitio, proyecto de Claude Design y
                                     mapeo de páginas
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
- **La fuente de contenido manda sobre sus destinos.** Lo aprobado vive en `web/contenido/` y se
  copia a destinos externos al workspace (el repo del sitio, un proyecto de Claude Design, un
  espejo local de diseños). Esos destinos **se alimentan de la fuente y nunca la sustituyen**: una
  corrección se hace primero en `web/contenido/` y desde ahí se propaga. Las rutas de
  cada destino viven en `contexto/configuracion.md`.

Flujo de la suite SEO:

```
site-context + site-snapshot ─→ seo-audit / audience-demand-evaluation / landing-blueprint
page-snapshot ────────────────→ page-cro / ai-seo
landing-blueprint ────────────→ brand-voice-enforcement (copy, sub-modo landing)
contexto/seo-tracking/ ───────→ (leído por los skills analíticos antes de recomendar/reportar)
seo-change-tracker ───────────→ registra la ejecución de los cambios recomendados
```

`landing-blueprint` decide **qué secciones debe tener una landing y por qué**, cruzando la demanda
del visitante con la economía de conversión del negocio (cuándo conviene responder cada pregunta).
Se distingue de `page-cro`: el blueprint decide la arquitectura; page-cro optimiza una página que ya
existe y tiene comportamiento medido. En modo auditoría el blueprint **lee** `cro-{slug}.md` en vez
de re-derivar sus hallazgos UX. Produce además la sección *Economía de la Conversión* de
`contexto/sitio.md` (previa confirmación) y el esqueleto `contexto/plantilla-landing.md` cuando N
landings comparten patrón.

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
As a rule only snapshot skills query MCPs; the four bounded exceptions (with explicit execution
limits) are `audience-demand-evaluation` (demand validation), `ai-seo` (real AI-visibility
verification, gated behind a cost confirmation), `seo-change-tracker` (baseline/checkpoint
capture, bounded to the sources of the changed area within the configured time window), and
`landing-blueprint` (searcher-question mining, capped at 10 calls behind a cost gate — and subject
to a **prior condition: exhaust local sources first**; only a gap that both lacks local backing
*and* would change a section's classification qualifies as investigable).

Cross-plugin: the brand voice guidelines home is `contexto/marca/brand-voice-guidelines.md`
(produced by **brand-voice-pro**), and the SEO analytical skills read it only as a guardrail,
delegating on-brand copy production back to brand-voice-pro's `brand-voice-enforcement`.

The tightest cross-plugin coupling is `landing-blueprint` → `brand-voice-enforcement`: the blueprint
emits a **copy contract per section** (message, required proof, approximate length, CTA) and the
writer consumes it through its **landing sub-mode** (§15 of `web-content-geo-seo.md`), which
suspends the article-shaped criteria (answer-first lead, quotable passages, default FAQ, keyword
placement, woven internal links) and drafts section by section instead. If you change the contract's
fields on one side, update the other.

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
   together, **and** bump the `metadata.version` of **every skill whose content you changed**, in
   the same commit. These are separate version lines, not one number in three files: each skill
   versions independently of its siblings and of the plugin (`utils` 1.7.1 ships `tarea` 1.7.1
   alongside `agenda`, `balance` and `plan-semanal`). So a change touching one
   skill is two manifest bumps plus one skill bump; a change touching two skills is two plus two.
   **The trigger is changing content that ships, not editing a manifest** — a pure refactor that
   extracts a reference out of a `SKILL.md` and never opens a `.json` still needs all of them. Some
   skills carry no `metadata.version`; those have nothing to bump, and adding one is optional.

## Cómo avanzamos: Toggl y `tareas/`

**Los pendientes viven en Toggl**, en el proyecto «Plugins de IA» que enlaza `tareas/toggl.md`: una
sola lista para todos los proyectos, que también se edita a mano. En el repo queda la memoria:

- **`tareas/toggl.md`** — el proyecto de Toggl, las áreas del repo con su ámbito y las reglas propias.
- **`tareas/historial/AAAA-MM.md`** — lo cerrado, con el comentario íntegro de cada tarea. **Es la
  mejor fuente de contexto sobre por qué el código está como está**: empieza por ahí antes de proponer
  cambios grandes.
- **`tareas/auditoria.md`** — hallazgos de una revisión completa por áreas, bajo petición.
- **`tareas/por-revisar.md`** — la bandeja: lo anotado sin decidir. Solo guarda; revisar es otro
  paso, que puede crear una tarea tuya en Toggl, delegarla a Claude o descartarla.
- **`tareas/para-claude.md`** — lo que una revisión delegó a Claude. Nunca va a Toggl.

Reglas irrenunciables:

1. **Una tarea, una rama.** Se comprueba que `main` está limpia y actualizada y se ramifica desde ahí;
   **nunca se trabaja sobre `main`**.
2. **La tarea es el objetivo del usuario; el plan es de Claude.** Se planifica con el usuario: los pasos
   de Claude (con su skill y su contexto) van al plan, `tareas/planes/`, y no a Toggl; lo que le toca
   al usuario va como subtareas, que cronometra él. Aprobado el plan, los pasos se encadenan sin pedir
   confirmación. **Toggl es solo del usuario**: el tiempo de Claude va a su registro local
   (`~/Obsidian/global/claude/registro-tiempo/`), nunca a Toggl.
3. **Se completa esa tarea y se para.** Al cerrar se pregunta una sola vez; con el visto bueno se
   encadenan el estado en Toggl, el tiempo de Claude a su registro, el historial, el commit, el merge a `main` y el push sin pausas —salvo `main`
   sucia o desactualizada, un conflicto o cambios ajenos a la tarea—.

Nada se crea en Toggl sin visto bueno, y la IA no reordena la cola del usuario. El flujo completo lo
gobiernan los skills `tarea` y `tarea-repo` (plugin `utils`).

## Git

`main` is the default branch. Commit only when the user asks; if on `main`, branch first.
Note `.gitignore` only excludes `.DS_Store`, so avoid committing stray macOS metadata.
