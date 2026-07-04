# Extractability Rubric

Scoring rubric for the AEO/GEO audit. Two levels: a **dimension checklist** for the whole piece (mirrors the writer's coverage report) and **block-level criteria** for granular findings. Both feed the "Extractabilidad del Contenido" section of the report and the global score in the "Resumen Ejecutivo".

> **Maintenance note.** The dimensions and thresholds in this rubric derive from the drafting standard used in this ecosystem: the GEO/SEO web-content module of the brand-voice-enforcement skill (brand-voice-pro plugin), `references/web-content-geo-seo.md`. The two plugins install separately, so there is no live reference between them — **if one file changes its thresholds, the other must be updated by hand.** Canonical thresholds: lead answer-first ~40–60 words with keyword in first ~100; quotable passages ≥3 of ~130–170 words with named source in-passage; FAQ answers 40–80 words; three-level attribution.

## Scoring scale

Each criterion scores **0–2**:

- **0** — absent or contradicts the criterion
- **1** — partially present (exists but misses threshold, placement, or self-containment)
- **2** — fully meets the criterion

## Dimension checklist (piece level)

These 15 dimensions mirror the writer's self-reported coverage table, so a drafting self-report and this audit are directly comparable side by side.

| # | Dimension | Full-score criterion (2) |
|---|-----------|--------------------------|
| 1 | Answer-first opening | Lead block of ~40–60 words; first sentence directly answers the piece's main question; exact target keyword within the first ~100 words; placed before the narrative opening |
| 2 | Quotable passages | ≥3 self-contained passages of ~130–170 words, each answering one concrete question with a named source in the same passage; market stated when geography matters |
| 3 | Question → answer structure | H2/H3 phrased as real user questions where natural; direct answer in the first sentences of each section; no warm-up beyond 2-3 sentences |
| 4 | Fact-first, voice-after | Every section opens with a neutral, liftable factual claim; subjective/brand framing follows, never replaces it |
| 5 | Entity clarity | Brand/organization named in full at least once; people with title+credential on first mention; laws/programs/products by official name; proper-noun re-naming per section (never pronouns/generics) |
| 6 | Attribution without redundancy | Three-level convention: full chain on first mention → short proper-noun anchor after → name+source inside quotables; varied connectors |
| 7 | EEAT signals | Demonstrated experience; claims backed by named experts/primary sources; authorship note with credentials; dated data with acknowledged limits |
| 8 | FAQ (if the topic warrants it) | Real user questions (People Also Ask); direct self-contained answers of 40–80 words; H3 under an H2; FAQPage schema present/recommended |
| 9 | Title & meta | Primary keyword in first 3-5 words of title, ≤~60 chars; meta ≤~155 chars with keyword, value statement, reason to click |
| 10 | Keyword placement | Primary keyword in title, first ~100 words, ≥1 H2, main image alt, URL slug (~1-1.5% density); secondary keywords distributed |
| 11 | Heading hierarchy | Exactly one H1; descriptive H2/H3; no skipped levels |
| 12 | Internal links | ≥2 internal links woven into the body with descriptive anchors at the thematic point; 1 to the pillar/hub if one exists |
| 13 | Schema | Appropriate type(s) present or explicitly recommended (Article/BlogPosting, FAQPage, HowTo, Product, Organization, BreadcrumbList; MedicalWebPage for health); core fields (author, dates, publisher, url) |
| 14 | Readability / visual breaks | No prose runs beyond ~3-4 paragraphs without a list, table, or callout; 3+ parallel items as list; 2+ entities × 2+ dimensions as table; without fragmenting reflective brand prose |
| 15 | Bot access & crawlability signals | AI bots not blocked in robots.txt; main content in server-rendered HTML; key data in extractable form (from the Bot Access Check + snapshot; in Mode B, evaluate what is knowable and mark the rest N/A) |

Dimensions that don't apply (e.g., FAQ on a piece that doesn't warrant one, internal links in an isolated draft) are marked **N/A** and excluded from the denominator — never counted as 0.

## Block-level criteria

For each content block (identified by its heading), score these five criteria and record which of the 11 patterns from [content-patterns.md](content-patterns.md) the block implements or should implement:

| Criterion | 2 | 1 | 0 |
|---|---|---|---|
| Direct answer first | First sentence answers the block's question | Answer present but buried mid-block | No direct answer |
| Self-containment | Block works verbatim without surrounding context | Needs minor context | Meaningless out of context |
| Query-phrased heading | Heading matches how users search | Descriptive but not query-shaped | Generic ("Introducción") |
| Sourced specificity | Specific number/fact + named, dated source in-block | Specifics without source, or source without specifics | Vague claims |
| Format fits intent | Table for comparison, list for steps/enumeration, prose for narrative | Suboptimal format | Format fights the intent (prose comparison, fragmented narrative) |

## YMYL weighting

When `contexto-sitio.md` indicates a YMYL domain (health, finance, legal — e.g., health clients), apply **double weight** to dimensions 5, 6, and 7 (entity clarity, attribution, EEAT) and to the "Sourced specificity" block criterion, and treat these as **mandatory**:

- Expert credentials on every clinical/financial/legal claim (name + specialty/title + institution)
- "Última revisión" date visible
- Domain-specific schema (`MedicalWebPage` for health)
- Study limitations acknowledged where studies are cited

A YMYL piece missing any mandatory item **cannot score above "Base"** regardless of its numeric total, and in Mode B the publication gate must mark it "no apto".

## Global score and named levels

Global score = points obtained / points possible (after N/A exclusions and YMYL weighting), as a percentage:

| Level | Range | Meaning |
|---|---|---|
| **No citable** | 0–39% | AI engines have little to extract or trust; structural rework needed |
| **Base** | 40–64% | Foundations exist; key levers (quotables, sources, schema) missing |
| **Extraíble** | 65–84% | AI engines can lift answers; authority/presence gaps remain |
| **Optimizado** | 85–100% | Meets the drafting standard; focus shifts to authority and measured visibility |

## Score → pattern mapping

For every dimension or block scoring 0-1, the recommendation names the pattern that fixes it:

| Gap | Apply pattern |
|---|---|
| No answer-first lead | Definition Block / Self-Contained Answer at the top |
| Missing quotable passages | Quotable Passage (130-170 words, source in-passage) |
| Unsourced claims | Statistic Citation Block / Evidence Sandwich |
| No expert voice | Expert Quote Block (three-level attribution) |
| Comparison in prose | Comparison Table Block |
| Process in prose | Step-by-Step Block |
| Evaluation without balance | Pros and Cons Block |
| Common questions unanswered | FAQ Block (40-80 word answers + FAQPage schema) |
| Generic headings | Question-phrased headings (see language guidance in content-patterns.md) |

## Report table format

The "Extractabilidad del Contenido" section of the report uses exactly this structure (headers in Spanish):

```markdown
### Checklist de dimensiones

| # | Dimensión | Puntaje | Evidencia | Patrón recomendado |
|---|-----------|---------|-----------|--------------------|
| 1 | Apertura answer-first | 0/1/2/N-A | [cita o hecho observado] | [patrón o —] |
| … | … | … | … | … |

**Score global: NN% — [Nivel]** (ponderación YMYL aplicada: sí/no)

### Detalle por bloque

| Bloque (encabezado) | Respuesta directa | Autocontención | Encabezado-query | Especificidad con fuente | Formato | Patrones presentes |
|---------------------|-------------------|----------------|------------------|--------------------------|---------|--------------------|
| [H2 del bloque] | 0-2 | 0-2 | 0-2 | 0-2 | 0-2 | [lista] |
```

Every score of 0 or 1 must carry evidence (a quote or an observed fact), never a bare number.
