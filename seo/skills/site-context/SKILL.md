---
name: site-context
description: "When the user wants to create, update, or review the strategic context for a site or project. Also use when the user mentions \"site context,\" \"strategic context,\" \"positioning,\" \"target audience,\" \"who is my customer,\" \"ICP,\" \"ideal customer profile,\" \"brand voice,\" \"differentiation,\" \"competitive landscape,\" or wants to establish foundational product and audience information that other skills can reference. This skill replaces product-marketing-context for site-level projects. Use it at the start of any new site project — it creates context/site-context.md that seo-audit, page-cro, and audience-demand-evaluation reference for strategic context. For factual site data, see site-snapshot. For audience demand evaluation, see audience-demand-evaluation."
metadata:
  version: 1.0.0
---

# Site Context

You help users create and maintain the strategic context for a site or project. This document captures foundational positioning, audience, messaging, and business information that other skills reference, so users don't have to repeat themselves across tasks.

The output is `context/site-context.md` — a canonical, reusable strategic context file.

This skill replaces `product-marketing-context`. There is no coexistence period.

## Language

Write section headers and field names in English.

Write all user-facing communication (explanations, questions, warnings, errors) in Spanish neutro.

Content inside fields stays in whatever language the user provides or the source uses.

## File Architecture

```text
{domain-or-project}/
  context/
    site-context.md
    site-snapshot.md
    snapshot-config.md
```

## Sections

The site-context document includes all sections from the former product-marketing-context, plus two new ones:

1. **Product Overview** — one-liner, what it does, product category, product type, business model
2. **Target Audience** — target company type, decision-makers, primary use case, jobs to be done, specific use cases
3. **Personas** — stakeholder roles, what each cares about, challenge, value promise
4. **Problems & Pain Points** — core problem, why alternatives fall short, cost, emotional tension
5. **Competitive Landscape** — direct, secondary, and indirect competitors with shortcomings
6. **Differentiation** — key differentiators, how it's different, why that's better, why customers choose it
7. **Objections & Anti-Personas** — top objections with responses, who is NOT a good fit
8. **Switching Dynamics** — JTBD Four Forces: push, pull, habit, anxiety
9. **Customer Language** — verbatim problem descriptions, solution descriptions, words to use/avoid, glossary
10. **Brand Voice** — tone, style, personality
11. **Proof Points** — metrics, notable customers, testimonial snippets, value themes
12. **Goals** — primary business goal, key conversion action, current metrics
13. **Site Scope** *(new)* — site type, main domain, technology stack, CMS, key integrations
14. **Strategic URLs** *(new)* — table of strategic pages with label, URL, page type, and role

## Auto-Draftable vs. User-Input Sections

When generating site-context for the first time from `site-snapshot.md`, not all sections can be completed automatically.

**Inferable from snapshot and visible site** (the skill can draft a V1):
- Product Overview (partial: from title, meta description, visible content)
- Target Audience (partial: from organic queries and traffic patterns)
- Competitive Landscape (partial: from DataForSEO top organic competitors)
- Site Scope
- Strategic URLs
- Goals (partial: from conversion events and site structure)

**Require user input** (the skill can attempt inference, but must mark it as `[inferred — review required]`):
- Personas
- Problems & Pain Points
- Differentiation
- Objections & Anti-Personas
- Switching Dynamics
- Customer Language
- Brand Voice
- Proof Points

When the skill infers content for these sections, it must add a visible note indicating the content was inferred and needs user review. This distinction matters because downstream skills (seo-audit, page-cro) trust site-context as validated strategic truth — if inferred content goes unreviewed, it can lead to misaligned diagnoses.

## Drafting Sources

Priority order:
1. `context/site-context.md` (existing — if it exists, summarize and update)
2. `context/site-snapshot.md` (primary source for auto-drafting)
3. `context/snapshot-config.md`
4. Project docs with explicit strategic context

Exclude:
- Page snapshots
- Technical audits
- UX/CRO reports

## Workflow

### Step 1: Check for existing context

Check if `context/site-context.md` exists.

**If it exists:**
- Read it and summarize what's captured
- Ask which sections the user wants to update
- Only gather info for those sections

**If it doesn't exist, offer two paths:**

1. **Auto-draft from site-snapshot** (recommended when `context/site-snapshot.md` exists): Read the snapshot, draft inferable sections, mark inferred sections that need review, present to user for corrections and gap-filling.

2. **Start from scratch**: Walk through each section conversationally, one at a time, gathering info progressively.

### Step 2: Gather information

**If auto-drafting:**
1. Read `context/site-snapshot.md` and `context/snapshot-config.md`
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

Save to `context/site-context.md`.

Tell the user: "Los skills de diagnóstico (seo-audit, page-cro) y el skill de evaluación de demanda (audience-demand-evaluation) van a usar este contexto automáticamente. Puedes actualizarlo cuando quieras."

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
