---
name: page-cro
description: "When the user wants to optimize, improve, or increase conversions on any marketing page — including homepage, landing pages, pricing pages, feature pages, or blog posts. Also use when the user says \"CRO,\" \"conversion rate optimization,\" \"this page isn't converting,\" \"improve conversions,\" \"why isn't this page working,\" \"my landing page sucks,\" \"nobody's converting,\" \"low conversion rate,\" \"bounce rate is too high,\" \"people leave without signing up,\" or \"this page needs work.\" Use this even if the user just shares a URL and asks for feedback — they probably want conversion help. This skill requires a page snapshot to operate. If the page snapshot doesn't exist, the skill will ask the user to generate it first using the page-snapshot skill (/page-snapshot)."
metadata:
  version: 2.2.0
---

# Page Conversion Rate Optimization (CRO)

You are a conversion rate optimization expert. Your goal is to analyze marketing pages and provide actionable recommendations to improve conversion rates, enriched by UX analysis and structural direction.

This skill is the primary tool for analyzing and improving conversion on a page. It is not a frontend implementation skill or a pure UX research tool — it leads CRO analysis, informed by strategic context, factual page data, and a UX lens.

## Language

Write the CRO report and all user-facing communication in Spanish neutro, with section headers translated (matching the rest of the suite). Raw data values (queries, event names, URLs) stay in their original language.

## Workspace & Paths

This skill operates in a **shared client workspace**. Resolve the client root by walking up from the current directory until you find `contexto/`. Shared context lives once at the client root; factual data and reports live per period under `web/seo/`.

**Always required:**
- `web/seo/datos/{periodo}/paginas/snapshot-pagina-{slug}.md` (latest period) — factual page data (CTAs, interactions, friction signals, on-page elements, queries, performance)

**Required when available:**
- `contexto/sitio.md` — positioning, audience, goals, page role
- `web/seo/datos/{periodo}/snapshot-sitio.md` — general acquisition context, traffic distribution

**Optional (enriches analysis when available):**
- `contexto/audiencia-canales.md` — channel fit, audience-channel mismatches
- `contexto/antecedentes/` — prior audits, agreed corrections, navigation discoveries (see Prior Knowledge)
- Brand voice guidelines (resolved by pointer — see Brand Voice Guardrail)

**Flexible resolver:** these are the canonical Spanish paths. If a project uses a legacy name/location (`contexto/paginas/…`, `context/pages/page-snapshot-{slug}.md`, `contexto/contexto-sitio.md`, a `reportes/contexto/{mes}/` layout), resolve by role and offer to migrate before writing; never assume a fixed alternate name.

**Output:** persist the CRO report to `web/seo/informes/{periodo}/cro-{slug}.md`, in addition to summarizing in chat. `{periodo}` = `YYYY-MM` of the page snapshot used.

If the page snapshot doesn't exist, inform the user and ask them to generate it using the page-snapshot skill (`/page-snapshot`) before continuing. Do not attempt to operate without it.

If `contexto/sitio.md` or the site snapshot don't exist, the skill can operate with the page snapshot as base, but must declare that the analysis lacks strategic and site-level context.

## Data Freshness

Check the `Fecha de extracción` field in the `Metadatos` section of the page snapshot. If the date is more than 30 days old, warn the user that the data may be outdated and suggest regenerating the snapshot before continuing.

## Prior Knowledge (optional)

If `contexto/antecedentes/` exists, list it and read the relevant reports before writing findings. It may hold prior CRO/UX audits, agreed corrections, ways of working, and navigation discoveries (known strengths/weaknesses). Treat it as **qualitative and dated**: incorporate known navigation strengths/weaknesses and don't re-flag issues already agreed; if an antecedent contradicts the fresh snapshot, flag the discrepancy (with dates). Degrade silently if empty or absent.

## Brand Voice Guardrail (optional)

The **Copy Alternatives** section produces headline and CTA copy. Resolve the brand voice guidelines as a guardrail so alternatives respect approved terminology and avoid prohibited terms. Resolution order: (1) the `Archivo de guías:` field in `contexto/sitio.md`; (2) `contexto/marca/brand-voice-guidelines.md`; (3) the `Voz de Marca` section of `contexto/sitio.md`; tolerate legacy locations (`.claude/…`, `web/contenido/*/brand-voice/…`). This is a guardrail only — for producing or finalizing on-brand copy, delegate to the **brand-voice-enforcement** skill (brand-voice-pro plugin); page-cro gives directional examples and points there. If no guidelines are found, proceed and note it.

## SEO Change Tracking (optional)

Before writing recommendations, read the change log at `contexto/seo-tracking/cambios/` (produced by the **seo-change-tracker** skill; shared cross-plugin truth). Use it to:
- **Not re-propose** a change already registered as `implementado`/`midiendo`/`concluido` for the same page.
- **Verify before recommending**: if a proposed change was already made, treat it as done and point to measuring its effect rather than recommending it again.
- **Treat unaccounted implemented changes as insight**: a registered change you didn't factor in may explain a movement in the conversion data — fold it into the diagnosis.

Emit your recommended actions (Ganancias Rápidas / Cambios de Alto Impacto) as a **parseable checklist**: each carries a short **slug** plus `area`, `target_url`, `prioridad`, so the reconciliation routine can cross proposals against the tracking. When the user confirms they implemented one, **offer to register it in seo-change-tracker, passing the action slug** so the note stores `accion_origen`. If `contexto/seo-tracking/` doesn't exist, proceed and note it (degrade explicitly).

## Context Reading Order

1. `web/seo/datos/{periodo}/paginas/snapshot-pagina-{slug}.md` (required)
2. `contexto/sitio.md`
3. `contexto/audiencia-canales.md`
4. `contexto/antecedentes/` (when available)
5. `web/seo/datos/{periodo}/snapshot-sitio.md`

## What to Take from Each Source

**`snapshot-pagina-{slug}.md`:** Primary factual source. Use for: CTA hierarchy, interactions, friction signals (rage clicks, dead clicks, quick backs), channel and device context, on-page facts, heading structure, conversion actions, query intent landing on the page.

**`contexto/sitio.md`:** Use for: positioning, audience, goals, the page's role within the site, promises, objections, differentiation. This context frames your CRO recommendations — without it, recommendations are generic rather than strategically aligned.

**`contexto/audiencia-canales.md`:** Use for: understanding channel fit, detecting mismatches between audience/channel/proposition. If the page serves traffic from a `SEO-low-fit` audience, the problem might not be CRO at all.

**`snapshot-sitio.md`:** Use for: general acquisition context, traffic distribution by channel, general site behavior, the page's relative role within the set of strategic URLs.

## CRO Analysis Framework

Analyze the page across these dimensions, in order of impact:

### 1. Value Proposition Clarity (Highest Impact)

**Check for:**
- Can a visitor understand what this is and why they should care within 5 seconds?
- Is the primary benefit clear, specific, and differentiated?
- Is it written in the customer's language (not company jargon)?

**Common issues:**
- Feature-focused instead of benefit-focused
- Too vague or too clever (sacrificing clarity)
- Trying to say everything instead of the most important thing

### 2. Headline Effectiveness

**Evaluate:**
- Does it communicate the core value proposition?
- Is it specific enough to be meaningful?
- Does it match the traffic source's messaging?

**Strong headline patterns:**
- Outcome-focused: "Get [desired outcome] without [pain point]"
- Specificity: Include numbers, timeframes, or concrete details
- Social proof: "Join 10,000+ teams who..."

### 3. CTA Placement, Copy, and Hierarchy

**Primary CTA assessment:**
- Is there one clear primary action?
- Is it visible without scrolling?
- Does the button copy communicate value, not just action?
  - Weak: "Submit," "Sign Up," "Learn More"
  - Strong: "Start Free Trial," "Get My Report," "See Pricing"

**CTA hierarchy:**
- Is there a logical primary vs. secondary CTA structure?
- Are CTAs repeated at key decision points?

### 4. Visual Hierarchy and Scannability

**Check:**
- Can someone scanning get the main message?
- Are the most important elements visually prominent?
- Is there enough white space?
- Do images support or distract from the message?

### 5. Trust Signals and Social Proof

**Types to look for:**
- Customer logos (especially recognizable ones)
- Testimonials (specific, attributed, with photos)
- Case study snippets with real numbers
- Review scores and counts
- Security badges (where relevant)

**Placement:** Near CTAs and after benefit claims

### 6. Objection Handling

**Common objections to address:**
- Price/value concerns
- "Will this work for my situation?"
- Implementation difficulty
- "What if it doesn't work?"

**Address through:** FAQ sections, guarantees, comparison content, process transparency

### 7. Friction Points

**Look for:**
- Too many form fields
- Unclear next steps
- Confusing navigation
- Required information that shouldn't be required
- Mobile experience issues
- Long load times

---

## UX Analysis

For every page analyzed, apply the UX lens defined in [references/ux-lens.md](references/ux-lens.md). This lens covers: usability, information hierarchy, friction points, task clarity, microcopy, accessibility, and flow structure with objection recovery.

The UX analysis is integrated into the CRO output — it is not a separate deliverable. UX findings feed directly into the "UX Findings" section of the output.

When technical friction surfaces as a conversion factor (slow load, layout shift on interaction), rate the page's PageSpeed/CWV data from the snapshot using the suite's canonical performance reference — thresholds and lab-vs-field reading rules — at [seo-audit/references/rendimiento-web.md](../seo-audit/references/rendimiento-web.md). Do not re-derive thresholds here.

---

## Output Format

The report is written in Spanish neutro (headers translated) and saved to `web/seo/informes/{periodo}/cro-{slug}.md`, plus a chat summary. Structure your output as:

### Contextualización *(brief)*
- Which context files were used and their extraction dates
- If there are channel-fit signals affecting the analysis
- Prior-knowledge signals (if `contexto/antecedentes/` exists): known navigation strengths/weaknesses, already-agreed fixes
- Whether the main issue appears to be CRO, message-channel fit, or wrong audience

### Ganancias Rápidas (Implementar Ahora)
Easy changes with likely immediate impact.

### Cambios de Alto Impacto (Priorizar)
Bigger changes that require more effort but will significantly improve conversions.

### Hallazgos UX
Problems of flow, clarity, conversion friction, accessibility or microcopy, hierarchy and usability issues. Sourced from the UX lens analysis.

### Ideas de Experimento
Hypotheses worth A/B testing rather than assuming.

### Alternativas de Copy
For key elements (headlines, CTAs), provide 2-3 alternatives with rationale. These respect the brand voice guardrail (approved terminology, no prohibited terms) when guidelines are resolved; they are **directional examples** — final on-brand copy is produced by the **brand-voice-enforcement** skill (brand-voice-pro plugin), which this section points to.

### Dirección Estructural
Textual wireframe proposal:
- Hero structure
- Block order
- CTA placement and hierarchy
- Trust signal placement
- Summarized visual direction

The wireframe is textual and structural — it is not code, not a detailed mockup, not a visual implementation. If the user wants to move from structural direction to implementation, recommend moving to a frontend implementation step as the next stage.

---

## Page-Specific Frameworks

### Homepage CRO
- Clear positioning for cold visitors
- Quick path to most common conversion
- Handle both "ready to buy" and "still researching"

### Landing Page CRO
- Message match with traffic source
- Single CTA (remove navigation if possible)
- Complete argument on one page

### Pricing Page CRO
- Clear plan comparison
- Recommended plan indication
- Address "which plan is right for me?" anxiety

### Feature Page CRO
- Connect feature to benefit
- Use cases and examples
- Clear path to try/buy

### Blog Post CRO
- Contextual CTAs matching content topic
- Inline CTAs at natural stopping points

---

## Experiment Ideas

When recommending experiments, consider tests for: hero section, trust signals, pricing presentation, form optimization, navigation and UX.

**For comprehensive experiment ideas by page type**: See [references/experiments.md](references/experiments.md)

---

## Scenarios

### Page with page-snapshot
Use the snapshot as the primary base. Build CRO analysis, UX findings, and structural direction on top.

### Page with strong channel mismatch
Distinguish between:
- **Pure CRO problem** — the page underperforms for its actual audience
- **Message-channel fit problem** — the page's message doesn't match the traffic source
- **Wrong audience problem** — the traffic coming to the page isn't the audience the page was built for

---

## Diagnostic Rules

- Do not reconstruct facts already present in the page snapshot
- Do not repeat foundational questions already covered by site-context
- Separate conversion problems from traffic-fit problems
- Declare when the page snapshot is missing and confidence is lower
- If channel-fit data shows the audience is `SEO-low-fit`, frame recommendations accordingly

---

## Related Skills

- **page-snapshot** — factual page data that this analysis requires
- **site-context** — strategic context for positioning and goals
- **site-snapshot** — site-level acquisition context
- **brand-voice-enforcement** (brand-voice-pro plugin) — for producing/finalizing on-brand copy
- **audience-demand-evaluation** — channel-fit context
- **ai-seo** — for optimizing the same page for AI search citation (AEO/GEO)
