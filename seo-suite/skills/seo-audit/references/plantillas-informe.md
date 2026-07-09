# Plantillas de Informe — seo-audit

Templates and conventions for the audit's output artifacts. SKILL.md defines the two-artifact model (executive + extended) and the executive template inline; this file holds the **extended-report template**, the **executive→extended anchor convention**, the **execution-layer field spec**, and the **single-topic expansion**. Read it when you write the extended technical report or a topical deep-dive.

All output is Spanish neutro with headers translated. Raw data values (queries, URLs, event names) stay in their source language.

## Contents
- [Extended report template](#extended-report-template)
- [Finding anchors (executive → extended)](#finding-anchors)
- [Execution-layer fields](#execution-layer-fields)
- [Single-topic expansion](#single-topic-expansion)

---

## Extended report template

File: `Auditoría SEO Informe Extendido.md` (or `Auditoría SEO Informe Extendido — {slug}.md` in URL-specific mode). This is the complete diagnosis — the executive report plus all evidence and reasoning. Same findings as the executive, fully worked. Section order:

### 1. Metadatos
Report name, mode (full-site / URL-specific), period, strategic context file + its `Fecha de extracción`, factual snapshot file + its `Fecha de extracción`, skill version. Repeat the >30-day freshness warning if it applies. Link back to the executive report (`[[Auditoría SEO Informe Ejecutivo]]` in Obsidian).

### 2. Contextualización
- Strategic context used and extraction date.
- Factual snapshot used and extraction date.
- Demand/channel-fit signals (if `contexto/audiencia-canales.md` exists).
- Prior-knowledge signals (if `contexto/antecedentes/` exists): already-agreed fixes, known strengths/weaknesses.
- Primary problem type: technical / on-page / content / coverage / demand. This framing prevents misdiagnosis — e.g. attributing low organic traffic to technical problems when the audience simply doesn't search actively.

### 3. Resumen Ejecutivo
Overall health assessment, top 3–5 priority issues, quick wins. (This mirrors the executive report's Veredicto + Lo que importa, in prose — it is the bridge for a reader who opened the full report directly.)

### 4. Hallazgos Técnicos SEO
One block per finding, each with these five fields and a stable anchor (see [Finding anchors](#finding-anchors)):
- **Problema** — what's wrong.
- **Impacto** — SEO/business impact (Alto / Medio / Bajo), tied where possible to the goal/conversion from `contexto/sitio.md`.
- **Evidencia** — how you found it (snapshot section + values, live verification, screenshots/exports). Be specific enough that someone can re-verify.
- **Solución** — the concrete fix. For the specific stack when known (e.g. Nuxt / Storyblok / Vercel), say *where* the change lives, not just what.
- **Prioridad** — 1–5 or Alta / Media / Baja.

Close each finding with its parseable action line: `slug: … · area: … · target_url: … · prioridad: …`.

### 5. Hallazgos On-Page
Same five-field format. When suggesting **title tag or meta description copy**, respect the brand voice guardrail (approved terminology, no prohibited terms) and note that final on-brand copy is produced by the **brand-voice-enforcement** skill — give only directional examples here.

### 6. Hallazgos de Contenido
Same five-field format.

### 7. Plan de Acción Priorizado
1. Critical fixes (blocking indexation/ranking).
2. High-impact improvements.
3. Quick wins (easy, immediate benefit).
4. Long-term recommendations.

Each item carries the execution-layer fields (owner / effort / done-criterion / what-to-measure — see below), so the full report's plan is executable, not just a list.

### 8. Nota metodológica (when relevant)
Which sources fed the report and any live verification done beyond the snapshot, with dates — so the reader can tell factual snapshot data from fresh checks.

---

## Finding anchors

The executive report links each finding to its expanded block in the full report. Make the anchor **stable and keyed to the action `slug`**, so links don't break when a heading is reworded.

**Obsidian vault** (detectable by a `.obsidian/` folder at the client root — the common case): use a block anchor placed on its **own line directly under the finding heading**. Obsidian renders `^id` literally if it's appended to a heading line, so keep it on a separate line — that line becomes a linkable block at the top of the section:

```markdown
### Home duplicado: `/` y `/home` sin consolidar
^home-duplicado

- **Problema**: …
```

and link from the executive finding:

```markdown
… · Prioridad: Alta · [[Auditoría SEO Informe Extendido#^home-duplicado|→ ver detalle]]
```

**Non-Obsidian**: fall back to a Markdown heading link — `[→ ver detalle](Auditoría SEO Informe Extendido.md#home-duplicado-y-home-sin-consolidar)` (GitHub-style slugified heading).

In URL-specific mode, target `Auditoría SEO Informe Extendido — {slug}` instead of `Auditoría SEO Informe Extendido`.

Use the **same `slug`** for: the block anchor, the parseable checklist line, and (later) the `accion_origen` handed to seo-change-tracker. One slug ties the whole chain together.

---

## Execution-layer fields

These make a plan executable instead of aspirational. They appear in the executive **Plan en secuencia** and in the full report's **Plan de Acción Priorizado**. For each action:

- **Responsable sugerido** — who acts: `dev` / `marketing` / `decisor` (or a named role). A recommendation, not an assignment.
- **Esfuerzo** — rough size: bajo (minutes) / medio (hours) / alto (days). Lets the reader plan a week of work.
- **Hecho =** — a verifiable done-criterion, ideally a check anyone can run. Examples: "`curl -I /home` devuelve 301 a `/`"; "GSC inspección de URL da 'Indexada' para las 6 URLs estratégicas"; "PSI mobile del home muestra LCP de campo < 2,5 s".
- **Qué medir** — the signal that tells you the fix worked, tied to the action `slug` for later reconciliation in seo-change-tracker (e.g. "impresiones GSC de las queries de la página X a 4 semanas"; "eventos `clic_whatsapp` de la landing Y").

**Decisiones que bloquean** are different from actions: they are choices the decision-maker must make *before* an action can proceed. Put them in their own executive section (up front), not inside a finding. Example: "¿`/endolifting` es solo landing de Ads (→ `noindex`) o debe rankear (→ title/meta/H1 propios + canónica)?" — the answer changes the action.

---

## Single-topic expansion

Secondary capability. With the executive→full links, "more detail" is usually just following a link. But sometimes a reader wants a **standalone document on one theme** — e.g. to hand a developer only the performance findings, or to send the client a focused note on indexation.

On request, produce `web/seo/informes/{periodo}/Auditoría SEO {tema}.md` (`{tema}` = a short topic label like `Rendimiento`, `Indexación`, `On-Page`). It reuses the **five-field finding template** above, scoped to only the findings for that theme, with a one-line note stating it is an extract of the extended report (link back to `[[Auditoría SEO Informe Extendido]]`). Do not re-diagnose — carry over the same findings, anchors, and action slugs so nothing diverges from the extended report.
