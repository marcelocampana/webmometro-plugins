---
name: seo-audit
description: "When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions \"SEO audit,\" \"technical SEO,\" \"why am I not ranking,\" \"SEO issues,\" \"on-page SEO,\" \"meta tags review,\" \"SEO health check,\" \"my traffic dropped,\" \"lost rankings,\" \"not showing up in Google,\" \"site isn't ranking,\" \"Google update hit me,\" \"page speed,\" \"core web vitals,\" \"crawl errors,\" or \"indexing issues.\" Use this even if the user just says something vague like \"my SEO is bad\" or \"help with SEO\" — start with an audit. For AI search optimization, see ai-seo. This skill requires context files (site-context, site-snapshot) to operate. If they don't exist, the skill will ask the user to generate them first using the corresponding snapshot and context skills."
metadata:
  version: 2.2.0
---

# SEO Audit

You are an expert in search engine optimization. Your goal is to identify SEO issues and provide actionable recommendations to improve organic search performance.

This skill is a diagnostic tool — it reads context files produced by other skills in the ecosystem, it does not query MCPs directly.

## Language

Write the audit report and all user-facing communication in Spanish neutro, with section headers translated (matching the rest of the suite). The skill's internal reasoning may stay in English; the delivered report does not. Raw data values (queries, URLs, event names) stay in their original language.

## Workspace & Paths

This skill operates in a **shared client workspace**. Resolve the client root by walking up from the current directory until you find `contexto/`. Shared context lives once at the client root; factual data and reports live per period under `web/seo/`.

**Always required:**
- `contexto/sitio.md` — strategic context (audience, positioning, goals)
- `web/seo/datos/{periodo}/snapshot-sitio.md` (latest period) — factual site data (visibility, coverage, performance)

**Required in URL-specific mode:**
- `web/seo/datos/{periodo}/paginas/snapshot-pagina-{slug}.md` — factual page data

**Optional (enriches diagnosis when available):**
- `contexto/audiencia-canales.md` — demand and channel-fit data
- `contexto/antecedentes/` — prior audits, agreed corrections, team learnings (see Prior Knowledge)
- Brand voice guidelines (resolved by pointer — see Brand Voice Guardrail)

**Flexible resolver:** these are the canonical Spanish paths. If a project uses a legacy name/location (`contexto/contexto-sitio.md`, `context/site-context.md`, `context/pages/page-snapshot-{slug}.md`, a `reportes/contexto/{mes}/` layout), resolve by role and offer to migrate before writing; never assume a fixed alternate name.

**Output:** persist the audit report to `web/seo/informes/{periodo}/auditoria-seo.md` (full-site) or `web/seo/informes/{periodo}/auditoria-seo-{slug}.md` (URL-specific), in addition to summarizing in chat. `{periodo}` = `YYYY-MM` of the snapshot used.

If required files don't exist, inform the user which ones are missing and ask them to generate them using the corresponding skills (site-snapshot, `/page-snapshot`, site-context) before continuing. Do not attempt to operate without them.

## Data Freshness

Check the `Fecha de extracción` field in the `Metadatos` section of each snapshot you read. If the date is more than 30 days old, warn the user that the data may be outdated and suggest regenerating the snapshot before continuing.

## Prior Knowledge (optional)

If `contexto/antecedentes/` exists, list it and read the relevant reports before writing findings. It may hold prior audits, agreed corrections, ways of working, and navigation discoveries. Treat it as **qualitative and dated**: do not re-flag issues already marked resolved/agreed, respect agreed ways of working, and if an antecedent contradicts a fresh snapshot, flag the discrepancy (with dates) rather than trusting the older document. Degrade silently if empty or absent.

## Brand Voice Guardrail (optional)

When the audit proposes **title tag or meta description copy**, resolve the brand voice guidelines as a guardrail so suggestions respect approved terminology and avoid prohibited terms. Resolution order: (1) the `Archivo de guías:` field in `contexto/sitio.md`; (2) `contexto/marca/brand-voice-guidelines.md`; (3) the `Voz de Marca` section of `contexto/sitio.md`; tolerate legacy locations (`.claude/…`, `web/contenido/*/brand-voice/…`). This is a guardrail only — for producing or finalizing on-brand copy, delegate to the **brand-voice-enforcement** skill (brand-voice-pro plugin); this audit only gives directional examples and points there. If no guidelines are found, proceed and note it.

## SEO Change Tracking (optional)

Before writing findings, read the change log at `contexto/seo-tracking/cambios/` (produced by the **seo-change-tracker** skill; shared cross-plugin truth). Use it to:
- **Not re-propose** a change already registered as `implementado`/`midiendo`/`concluido` for the same `target_url`.
- **Verify before recommending**: if a proposed fix was already made, treat it as done and point to measuring its effect (its checkpoints) rather than recommending it again.
- **Treat unaccounted implemented changes as insight**: a registered change you didn't factor in may explain a movement in the data — fold it into the diagnosis, not as a new recommendation.

Emit your recommended actions as a **parseable checklist**: each action carries a short **slug** plus `area`, `target_url`, `prioridad`. This lets the reconciliation routine (see seo-change-tracker) cross proposals against the tracking. When the user confirms they implemented one of these actions, **offer to register it in seo-change-tracker, passing the action slug** so the note stores `accion_origen` (enables deterministic matching later). If `contexto/seo-tracking/` doesn't exist, proceed and note it (degrade explicitly).

## Context Reading Order

1. `contexto/sitio.md`
2. `web/seo/datos/{periodo}/snapshot-sitio.md`
3. `contexto/audiencia-canales.md` (when available)
4. `contexto/antecedentes/` (when available)
5. `web/seo/datos/{periodo}/paginas/snapshot-pagina-{slug}.md` (required in URL-specific mode)

## What to Take from Each Source

**`contexto/sitio.md`:** audience, positioning, goals, strategic pages, priorities. Use this to understand what the site is trying to achieve and for whom — so your audit findings are framed in terms of business impact, not just technical compliance.

**`snapshot-sitio.md` (latest period):** organic visibility, coverage, indexation, technical performance, competitors, channel distribution. This is your factual baseline for site-level diagnosis.

**`contexto/audiencia-canales.md`:** organic demand, capturability, channel limitations. Use this to distinguish SEO execution problems from demand or channel-fit problems. If this file shows `SEO-low-fit` for an audience, don't diagnose low traffic for that audience as an SEO failure.

**`snapshot-pagina-{slug}.md`:** on-page facts, behavior, queries, performance for a specific URL. Only for URL-specific audits.

## Operating Modes

### Full Site Mode

- Reads `contexto/sitio.md`, the latest `snapshot-sitio.md`, and `contexto/audiencia-canales.md`
- Diagnoses at site level: coverage, indexation, general technical performance, competition, channels
- Uses data already present in `snapshot-sitio.md` (top pages, top queries, coverage, PageSpeed for strategic URLs)
- Does NOT read individual page snapshots — the token cost would be excessive
- If it detects problems requiring page-level analysis, it recommends running `page-snapshot` + URL-specific audit for the affected pages

### URL-Specific Mode

- Also reads `web/seo/datos/{periodo}/paginas/snapshot-pagina-{slug}.md`
- If the page snapshot doesn't exist, asks the user to generate it first with `/page-snapshot`
- Diagnoses at page level: on-page elements, heading structure, images, CTAs, schema, performance, queries

## Initial Contextualization Layer

Before diving into findings, the audit output must include a brief contextualization section that states:

- Which strategic context was used (file and extraction date)
- Which factual snapshot was used (file and extraction date)
- Whether there are signals of low demand or low SEO fit for certain audiences
- Whether the main problem appears to be technical, on-page, content, coverage, or demand-related

This framing matters because it prevents misdiagnosis — for example, attributing low organic traffic to technical problems when the real issue is that the audience doesn't search actively.

## Schema Markup Detection Limitation

**`web_fetch` and `curl` cannot reliably detect structured data / schema markup.**

Many CMS plugins (AIOSEO, Yoast, RankMath) inject JSON-LD via client-side JavaScript — it won't appear in static HTML or `web_fetch` output (which strips `<script>` tags during conversion).

**To accurately check for schema markup, use one of these methods:**
1. **Browser tool** — render the page and run: `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results
3. **Screaming Frog export** — if the client provides one, use it (SF renders JavaScript)

Reporting "no schema found" based solely on `web_fetch` or `curl` leads to false audit findings.

## Audit Framework

### Priority Order
1. **Crawlability & Indexation** (can Google find and index it?)
2. **Technical Foundations** (is the site fast and functional?)
3. **On-Page Optimization** (is content optimized?)
4. **Content Quality** (does it deserve to rank?)
5. **Authority & Links** (does it have credibility?)

---

## Technical SEO Audit

### Crawlability

**Robots.txt**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

**XML Sitemap**
- Exists and accessible
- Submitted to Search Console
- Contains only canonical, indexable URLs
- Updated regularly
- Proper formatting

**Site Architecture**
- Important pages within 3 clicks of homepage
- Logical hierarchy
- Internal linking structure
- No orphan pages

**Crawl Budget Issues** (for large sites)
- Parameterized URLs under control
- Faceted navigation handled properly
- Infinite scroll with pagination fallback
- Session IDs not in URLs

### Indexation

**Index Status**
- site:domain.com check
- Search Console coverage report
- Compare indexed vs. expected

**Indexation Issues**
- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization**
- All pages have canonical tags
- Self-referencing canonicals on unique pages
- HTTP → HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

### Site Speed & Core Web Vitals

Rate at the 75th percentile. **Field data (CrUX) is the verdict; lab data (Lighthouse) is
diagnostic only.** If the snapshot has only lab data (field marked unavailable because no Google
API key was configured), rate provisionally and say so — never present a lab number as real-user
performance.

**Core Web Vitals** (Good / Needs Improvement / Poor)
- LCP (Largest Contentful Paint): ≤ 2.5s / 2.5–4.0s / > 4.0s
- INP (Interaction to Next Paint): ≤ 200ms / 200–500ms / > 500ms
- CLS (Cumulative Layout Shift): ≤ 0.1 / 0.1–0.25 / > 0.25

A page passes CWV only when LCP, INP, and CLS are **all** in Good.

**Supporting metrics:** FCP (≤ 1.8s good), TTFB (≤ 0.8s good). **Speed factors:** server response
time, image optimization, JavaScript execution, CSS delivery, caching headers, CDN, font loading.

For the full threshold tables, the lab-vs-field reading rules, and diagnosis→fix guidance with
code examples (LCP element, INP, CLS, render-blocking, fonts, caching), see
[references/rendimiento-web.md](references/rendimiento-web.md). Performance fixes carry
`area: tecnico` in the recommended-actions checklist.

### Mobile-Friendliness

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Same content as desktop
- Mobile-first indexing readiness

### Security & HTTPS

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HTTP → HTTPS redirects
- HSTS header (bonus)

### URL Structure

- Readable, descriptive URLs
- Keywords in URLs where natural
- Consistent structure
- No unnecessary parameters
- Lowercase and hyphen-separated

---

## On-Page SEO Audit

### Title Tags

**Check for:**
- Unique titles for each page
- Primary keyword near beginning
- 50-60 characters (visible in SERP)
- Compelling and click-worthy
- Brand name placement (end, usually)

**Common issues:**
- Duplicate titles
- Too long (truncated)
- Too short (wasted opportunity)
- Keyword stuffing
- Missing entirely

### Meta Descriptions

**Check for:**
- Unique descriptions per page
- 150-160 characters
- Includes primary keyword
- Clear value proposition
- Call to action

**Common issues:**
- Duplicate descriptions
- Auto-generated garbage
- Too long/short
- No compelling reason to click

### Heading Structure

**Check for:**
- One H1 per page
- H1 contains primary keyword
- Logical hierarchy (H1 → H2 → H3)
- Headings describe content
- Not just for styling

**Common issues:**
- Multiple H1s
- Skip levels (H1 → H3)
- Headings used for styling only
- No H1 on page

### Content Optimization

**Primary Page Content**
- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth/length for topic
- Answers search intent
- Better than competitors

**Thin Content Issues**
- Pages with little unique content
- Tag/category pages with no value
- Doorway pages
- Duplicate or near-duplicate content

### Image Optimization

**Check for:**
- Descriptive file names
- Alt text on all images
- Alt text describes image
- Compressed file sizes
- Modern formats (WebP)
- Lazy loading implemented
- Responsive images

### Internal Linking

**Check for:**
- Important pages well-linked
- Descriptive anchor text
- Logical link relationships
- No broken internal links
- Reasonable link count per page

**Common issues:**
- Orphan pages (no internal links)
- Over-optimized anchor text
- Important pages buried
- Excessive footer/sidebar links

### Keyword Targeting

**Per Page**
- Clear primary keyword target
- Title, H1, URL aligned
- Content satisfies search intent
- Not competing with other pages (cannibalization)

**Site-Wide**
- Keyword mapping document
- No major gaps in coverage
- No keyword cannibalization
- Logical topical clusters

---

## Content Quality Assessment

### E-E-A-T Signals

**Experience** — First-hand experience demonstrated, original insights/data, real examples and case studies

**Expertise** — Author credentials visible, accurate detailed information, properly sourced claims

**Authoritativeness** — Recognized in the space, cited by others, industry credentials

**Trustworthiness** — Accurate information, transparent about business, contact info available, privacy policy, secure site

### Content Depth

- Comprehensive coverage of topic
- Answers follow-up questions
- Better than top-ranking competitors
- Updated and current

### User Engagement Signals

- Time on page
- Bounce rate in context
- Pages per session
- Return visits

---

## Common Issues by Site Type

### SaaS/Product Sites
- Product pages lack content depth
- Blog not integrated with product pages
- Missing comparison/alternative pages
- Feature pages thin on content
- No glossary/educational content

### E-commerce
- Thin category pages
- Duplicate product descriptions
- Missing product schema
- Faceted navigation creating duplicates
- Out-of-stock pages mishandled

### Content/Blog Sites
- Outdated content not refreshed
- Keyword cannibalization
- No topical clustering
- Poor internal linking
- Missing author pages

### Local Business
- Inconsistent NAP
- Missing local schema
- No Google Business Profile optimization
- Missing location pages
- No local content

---

## Output Format

The report is written in Spanish neutro (headers translated) and saved to `web/seo/informes/{periodo}/auditoria-seo.md` (or `auditoria-seo-{slug}.md` in URL-specific mode), plus a chat summary.

**Contextualización**
- Strategic context used and extraction date
- Factual snapshot used and extraction date
- Demand/channel-fit signals (if `contexto/audiencia-canales.md` exists)
- Prior-knowledge signals (if `contexto/antecedentes/` exists): already-agreed fixes, known strengths/weaknesses
- Primary problem type assessment: technical, on-page, content, coverage, or demand

**Resumen Ejecutivo**
- Overall health assessment
- Top 3-5 priority issues
- Quick wins identified

**Hallazgos Técnicos SEO**
For each issue:
- **Problema**: What's wrong
- **Impacto**: SEO impact (Alto/Medio/Bajo)
- **Evidencia**: How you found it
- **Solución**: Specific recommendation
- **Prioridad**: 1-5 or Alta/Media/Baja

**Hallazgos On-Page** — Same format. When suggesting **title tag or meta description copy**, respect the brand voice guardrail (approved terminology, no prohibited terms) and note that final on-brand copy is produced by the **brand-voice-enforcement** skill; give only directional examples here.

**Hallazgos de Contenido** — Same format

**Plan de Acción Priorizado**
1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

## Diagnostic Rules

- Do not repeat questions already answered by `site-context`
- Do not assume that every organic decline is a technical problem
- Do not diagnose as SEO failure something that is a demand or channel-fit limitation
- Verify snapshot freshness before using their data
- If required files are missing, request their creation before continuing

---

## References

- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid (em dashes, overused phrases, filler words)
- [Web Performance & Core Web Vitals](references/rendimiento-web.md): Canonical threshold tables, lab-vs-field reading rules, and diagnosis→fix guidance for PageSpeed/CWV data (this is the suite's owner for performance interpretation)
- For AI search optimization (AEO, GEO, LLMO, AI Overviews), see the **ai-seo** skill

---

## Tools Referenced

**Free Tools**
- Google Search Console (essential)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test (**use this for schema validation — it renders JavaScript**)
- Mobile-Friendly Test
- Schema Validator

> **Note on schema detection:** `web_fetch` strips `<script>` tags (including JSON-LD) and cannot detect JS-injected schema. Use the browser tool, Rich Results Test, or Screaming Frog instead.

**Paid Tools** (if available)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Related Skills

- **site-snapshot** — factual site data that this audit consumes
- **page-snapshot** — factual page data for URL-specific audits
- **site-context** — strategic context that frames the audit
- **audience-demand-evaluation** — demand and channel-fit context
- **ai-seo** — for optimizing content for AI search engines
- **page-cro** — for optimizing pages for conversion (not just ranking)
- **brand-voice-enforcement** (brand-voice-pro plugin) — for producing/finalizing on-brand title & meta copy
