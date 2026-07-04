---
name: site-context
description: "When the user wants to create, update, or review the strategic context for a site or project. Also use when the user mentions \"site context,\" \"strategic context,\" \"positioning,\" \"target audience,\" \"who is my customer,\" \"ICP,\" \"ideal customer profile,\" \"brand voice,\" \"differentiation,\" \"competitive landscape,\" or wants to establish foundational product and audience information that other skills can reference. This skill replaces product-marketing-context for site-level projects. Use it at the start of any new site project — it creates contexto/sitio.md that seo-audit, page-cro, ai-seo, and audience-demand-evaluation reference for strategic context. For factual site data, see site-snapshot. For audience demand evaluation, see audience-demand-evaluation."
metadata:
  version: 1.2.0
---

# Site Context

You help users create and maintain the strategic context for a site or project. This document captures foundational positioning, audience, messaging, and business information that other skills reference, so users don't have to repeat themselves across tasks.

The output is `contexto/sitio.md` — a canonical, reusable strategic context file that lives once at the client root and is read by several plugins (seo-suite skills and brand-voice-pro).

This skill replaces `product-marketing-context`. There is no coexistence period.

## Language

Write the output document's section headers and field names in Spanish neutro (translated), matching the rest of the suite.

Write all user-facing communication (explanations, questions, warnings, errors) in Spanish neutro.

Content inside fields stays in whatever language the user provides or the source uses.

## Workspace & Paths

This skill operates in a **shared client workspace**. Strategic truth lives once at the client root under `contexto/`; nothing is duplicated. `contexto/sitio.md` is a **living** document (not versioned by period).

```text
{cliente}/
  contexto/                     ← COMPARTIDO (todos los plugins leen; nadie duplica)
    sitio.md                       ← SALIDA de este skill
    configuracion.md               identificadores de fuente + URLs estratégicas
    audiencia-canales.md           (audience-demand)
    marca/                         (brand-voice-pro)
  web/seo/datos/{periodo}/       snapshots factuales (site-snapshot)
```

- **Client root:** resolve by walking up from the current directory until you find `contexto/`. Read shared files there; write `contexto/sitio.md` there.
- **Canonical Spanish names:** `contexto/sitio.md`, `contexto/configuracion.md`. Site snapshots live under `web/seo/datos/{periodo}/`.
- **Flexible resolver (do not fail on a name):** if the canonical file isn't found, resolve by role — a legacy `contexto/contexto-sitio.md`, `context/site-context.md`, or a `reportes/contexto/{mes}/…` layout. If found in a legacy shape, offer to migrate to the canonical paths before writing; if the user declines, keep the existing tree. If nothing is found, treat it as a new document.

## Sections

The site-context document includes all sections from the former product-marketing-context, plus two new ones:

Los encabezados de sección en el archivo van en español neutro (el nombre en inglés se indica entre paréntesis solo como referencia de esquema):

1. **Resumen del Producto** (Product Overview) — one-liner, what it does, product category, product type, business model
2. **Audiencia Objetivo** (Target Audience) — target company type, decision-makers, primary use case, jobs to be done, specific use cases
3. **Personas** — stakeholder roles, what each cares about, challenge, value promise
4. **Problemas y Puntos de Dolor** (Problems & Pain Points) — core problem, why alternatives fall short, cost, emotional tension
5. **Panorama Competitivo** (Competitive Landscape) — direct, secondary, and indirect competitors with shortcomings
6. **Diferenciación** (Differentiation) — key differentiators, how it's different, why that's better, why customers choose it
7. **Objeciones y Anti-Personas** (Objections & Anti-Personas) — top objections with responses, who is NOT a good fit
8. **Dinámicas de Cambio** (Switching Dynamics) — JTBD Four Forces: push, pull, habit, anxiety
9. **Lenguaje del Cliente** (Customer Language) — verbatim problem descriptions, solution descriptions, words to use/avoid, glossary
10. **Voz de Marca** (Brand Voice) — tone, style, personality; plus an optional `Archivo de guías:` field pointing to the project's brand voice guidelines document. The canonical home is `contexto/marca/brand-voice-guidelines.md` (shared, produced by brand-voice-pro), but the field may point anywhere. Downstream skills (ai-seo, page-cro, seo-audit) resolve brand voice through this pointer as a guardrail. When a user mentions where their brand guidelines live, offer to persist the path here.
11. **Pruebas y Evidencia** (Proof Points) — metrics, notable customers, testimonial snippets, value themes
12. **Objetivos** (Goals) — primary business goal, key conversion action, current metrics
13. **Alcance del Sitio** (Site Scope) *(new)* — site type, main domain, technology stack, CMS, key integrations
14. **URLs Estratégicas** (Strategic URLs) *(new)* — table of strategic pages with label, URL, page type, and role

## Auto-Draftable vs. User-Input Sections

When generating site-context for the first time from the site snapshot, not all sections can be completed automatically.

**Inferable from snapshot and visible site** (the skill can draft a V1):
- Resumen del Producto (partial: from title, meta description, visible content)
- Audiencia Objetivo (partial: from organic queries and traffic patterns)
- Panorama Competitivo (partial: from DataForSEO top organic competitors)
- Alcance del Sitio
- URLs Estratégicas
- Objetivos (partial: from conversion events and site structure)

**Require user input** (the skill can attempt inference, but must mark it as `[inferido — requiere revisión]`):
- Personas
- Problemas y Puntos de Dolor
- Diferenciación
- Objeciones y Anti-Personas
- Dinámicas de Cambio
- Lenguaje del Cliente
- Voz de Marca
- Pruebas y Evidencia

When the skill infers content for these sections, it must add a visible note indicating the content was inferred and needs user review. This distinction matters because downstream skills (seo-audit, page-cro) trust site-context as validated strategic truth — if inferred content goes unreviewed, it can lead to misaligned diagnoses.

## Drafting Sources

Priority order:
1. `contexto/sitio.md` (existing — if it exists, summarize and update)
2. `web/seo/datos/{periodo}/snapshot-sitio.md` — latest period (primary source for auto-drafting)
3. `contexto/configuracion.md`
4. Project docs with explicit strategic context

Exclude:
- Page snapshots
- Technical audits
- UX/CRO reports

## Workflow

### Step 1: Check for existing context

Check if `contexto/sitio.md` exists (resolve the client root by walking up to `contexto/`; if only a legacy `contexto/contexto-sitio.md` or `context/site-context.md` exists, read it and offer to migrate).

**If it exists:**
- Read it and summarize what's captured
- Ask which sections the user wants to update
- Only gather info for those sections

**If it doesn't exist, offer two paths:**

1. **Auto-draft from site-snapshot** (recommended when a site snapshot exists under `web/seo/datos/{periodo}/`): Read the latest snapshot, draft inferable sections, mark inferred sections that need review, present to user for corrections and gap-filling.

2. **Start from scratch**: Walk through each section conversationally, one at a time, gathering info progressively.

### Step 2: Gather information

**If auto-drafting:**
1. Read the latest `web/seo/datos/{periodo}/snapshot-sitio.md` and `contexto/configuracion.md`
2. Draft all inferable sections
3. Attempt inference on user-input sections, clearly marking them
4. Present the draft and ask what needs correcting or is missing
5. Iterate until the user is satisfied

**If starting from scratch:**
Walk through each section conversationally. For each:
1. Briefly explain what you're capturing
2. Ask relevant questions
3. Confirm accuracy
4. Move to the next

Push for verbatim customer language — exact phrases are more valuable than polished descriptions because they reflect how customers actually think and speak.

### Step 3: Save

Save to `contexto/sitio.md`.

Tell the user: "Los skills de diagnóstico (seo-audit, page-cro, ai-seo) y el skill de evaluación de demanda (audience-demand-evaluation) van a usar este contexto automáticamente. Puedes actualizarlo cuando quieras."

## Tips

- **Be specific**: Ask "¿Cuál es la frustración #1 que lleva a tus clientes a buscarte?" not "¿Qué problema resuelves?"
- **Capture exact words**: Customer language beats polished descriptions
- **Ask for examples**: "¿Puedes darme un ejemplo?" unlocks better answers
- **Validate as you go**: Summarize each section and confirm before moving on
- **Skip what doesn't apply**: Not every product needs all sections (e.g., Personas for B2C)

## Related Skills

- **site-snapshot** — factual data source for auto-drafting this context
- **audience-demand-evaluation** — evaluates demand and channel fit per audience, reading this context
- **seo-audit** — SEO diagnosis that reads this context for strategic alignment
- **page-cro** — conversion analysis that reads this context for positioning and goals
- **ai-seo** — AEO/GEO audit that reads this context for market, audience, and the brand voice pointer
