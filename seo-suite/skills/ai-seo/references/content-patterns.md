# AEO and GEO Content Patterns

Reusable content block patterns optimized for answer engines and AI citation. The audit uses these patterns two ways: to detect which patterns the content already implements (feeding the extractability rubric) and to produce antes→después rewrites in the recommendations.

**Threshold alignment.** Length thresholds here are aligned with the drafting standard used in this ecosystem (the GEO/SEO web-content module of brand-voice-enforcement). Where the original source of these patterns differed, the drafting standard wins: quotable passages ~130–170 words, FAQ answers 40–80 words, answer-first lead ~40–60 words. If the drafting standard changes, update this file to match.

**Language.** Pattern scaffolds below are written in English; when auditing or rewriting content, produce questions and rewrites **in the content's language**. For Spanish content, phrase question headings the way users actually search: "Qué es…", "Cómo…", "Por qué…", "Cuándo…", "X vs Y", "mejores X para…", "cuánto cuesta…".

---

## Contents
- Answer Engine Optimization (AEO) Patterns (Definition Block, Step-by-Step Block, Comparison Table Block, Pros and Cons Block, FAQ Block, Listicle Block)
- Generative Engine Optimization (GEO) Patterns (Statistic Citation Block, Expert Quote Block, Authoritative Claim Block, Self-Contained Answer Block / Quotable Passage, Evidence Sandwich Block)
- Domain-Specific GEO Tactics
- Voice Search Optimization

## Answer Engine Optimization (AEO) Patterns

These patterns help content appear in featured snippets, AI Overviews, voice search results, and answer boxes.

### Definition Block

Use for "What is [X]?" / "Qué es [X]" queries.

```markdown
## What is [Term]?

[Term] is [concise 1-sentence definition]. [Expanded 1-2 sentence explanation with key characteristics]. [Brief context on why it matters or how it's used].
```

**Extractability criteria (rubric):** definition in the first sentence; 3-4 sentences total; self-contained (works without the rest of the page); heading phrased as the query.

**Ejemplo en español:**
```markdown
## Qué es la mamografía de tamizaje

La mamografía de tamizaje es una radiografía de las mamas que se realiza en mujeres sin síntomas para detectar el cáncer de mama en etapas tempranas. Se recomienda de forma periódica a partir de cierta edad, según las guías clínicas de cada país. Detectar el cáncer antes de que produzca síntomas aumenta significativamente las opciones de tratamiento.
```

### Step-by-Step Block

Use for "How to [X]" / "Cómo [X]" queries. Optimal for list snippets.

```markdown
## How to [Action/Goal]

[1-sentence overview of the process]

1. **[Step Name]**: [Clear action description in 1-2 sentences]
2. **[Step Name]**: [Clear action description in 1-2 sentences]
3. **[Step Name]**: [Clear action description in 1-2 sentences]
4. **[Step Name]**: [Clear action description in 1-2 sentences]
5. **[Step Name]**: [Clear action description in 1-2 sentences]

[Optional: Brief note on expected outcome or time estimate]
```

**Extractability criteria:** 1-sentence intro; numbered steps with bolded step names; max 2 sentences per step; ~5 steps standard.

### Comparison Table Block

Use for "[X] vs [Y]" queries. Optimal for table snippets.

```markdown
## [Option A] vs [Option B]: [Brief Descriptor]

| Feature | [Option A] | [Option B] |
|---------|------------|------------|
| [Criteria 1] | [Value/Description] | [Value/Description] |
| [Criteria 2] | [Value/Description] | [Value/Description] |
| [Criteria 3] | [Value/Description] | [Value/Description] |
| [Criteria 4] | [Value/Description] | [Value/Description] |
| Best For | [Use case] | [Use case] |

**Bottom line**: [1-2 sentence recommendation based on different needs]
```

**Extractability criteria:** actual table (not prose comparison); 4-5 criteria rows plus a "Best For" row; 1-2 sentence bottom-line conclusion; balanced (obviously biased comparisons are penalized by AI engines).

### Pros and Cons Block

Use for evaluation queries: "Is [X] worth it?" / "¿Vale la pena [X]?"

```markdown
## Advantages and Disadvantages of [Topic]

[1-sentence overview of the evaluation context]

### Pros

- **[Benefit category]**: [Specific explanation]
- **[Benefit category]**: [Specific explanation]
- **[Benefit category]**: [Specific explanation]

### Cons

- **[Drawback category]**: [Specific explanation]
- **[Drawback category]**: [Specific explanation]
- **[Drawback category]**: [Specific explanation]

**Verdict**: [1-2 sentence balanced conclusion with recommendation]
```

**Extractability criteria:** ≥3 pros and ≥3 cons in "Category: explanation" format; balanced verdict of 1-2 sentences.

### FAQ Block

Use for topic pages with multiple common questions. Essential for `FAQPage` schema.

```markdown
## Frequently Asked Questions

### [Question phrased exactly as users search]?

[Direct answer in first sentence]. [Supporting context in 1-3 additional sentences].
```

**Tips for FAQ questions:**
- Use natural question phrasing — in Spanish: "¿Cómo puedo…?", "¿Qué pasa si…?", "¿Cuándo debo…?"
- Include question words: qué, cómo, por qué, cuándo, dónde, quién, cuál
- Match "People Also Ask" / "Otras preguntas de los usuarios" queries from real search results — never invent questions
- Keep answers between **40-80 words** (drafting-standard threshold)
- Mark questions as `H3` under an `H2` such as "Preguntas frecuentes"
- Emit `FAQPage` schema

**Extractability criteria:** real user questions; direct answer in the first sentence; 40-80 words per answer; H3-under-H2 structure; FAQPage schema present or recommended.

### Listicle Block

Use for "Best [X]", "Top [X]", "[Number] ways to [X]" queries.

```markdown
## [Number] Best [Items] for [Goal/Purpose]

[1-2 sentence intro establishing context and selection criteria]

### 1. [Item Name]

[Why it's included in 2-3 sentences with specific benefits]
```

**Extractability criteria:** numbered H3 items; selection criteria stated in the intro; specific benefit per item (not generic praise).

---

## Generative Engine Optimization (GEO) Patterns

These patterns optimize content for citation by AI assistants (ChatGPT, Claude, Perplexity, Gemini).

### Statistic Citation Block

Statistics with named sources are among the strongest citation levers (see platform-ranking-factors.md for the dated study figures).

```markdown
[Claim statement]. According to [Source/Organization, year], [specific statistic with number and timeframe]. [Context for why this matters].
```

**Ejemplo en español:**
```markdown
El diagnóstico temprano cambia el pronóstico. Según cifras del Ministerio de Salud de Chile (2024), la sobrevida a cinco años supera el 90% cuando el cáncer de mama se detecta en etapa I. Por eso el control periódico importa más que cualquier síntoma visible.
```

**Extractability criteria:** specific number + timeframe; named source in the same sentence or passage ("según [organización, año]"), never "studies show" / "los estudios dicen"; dated.

### Expert Quote Block

Named expert attribution adds credibility and increases citation likelihood.

```markdown
"[Direct quote from expert]," says [Expert Name], [Title/Role] at [Organization]. [1 sentence of context or interpretation].
```

**Attribution without redundancy (three-level convention, aligned with the drafting standard):**
- **First mention:** full chain — name + role + affiliation + source (+ where/when). Only here.
- **Later mentions:** short proper-noun anchor — surname, institution, or source, whichever carries the signal for that data point. Never a pronoun or generic ("la especialista", "la institución").
- **Inside quotable passages:** intermediate form — name + source, the minimum for the fragment to stand alone.

Vary connectors ("según", "detalla", "explicó", "señala") so the short form doesn't read as a template.

### Authoritative Claim Block

Structure claims for easy AI extraction with clear attribution.

```markdown
[Topic] [verb: is/has/requires/involves] [clear, specific claim]. [Source] [confirms/reports/found] that [supporting evidence]. This [explains/means/suggests] [implication or action].
```

**Extractability criteria:** claim as a bare declarative sentence first; explicit source verb ("confirma", "reporta", "encontró"); implication closes the block.

### Self-Contained Answer Block / Quotable Passage

The single most important GEO lever. AI assistants quote self-contained fragments that answer a question without needing the rest of the article.

Two granularities, both audited:

1. **Liftable statement** (sentence-level): a bolded topic + a complete, standalone answer with specific details — the sentence an answer engine lifts verbatim.

```markdown
**[Topic/Question]**: [Complete, self-contained answer with specific numbers or examples, 2-3 sentences.]
```

2. **Quotable passage** (passage-level, drafting-standard threshold): a self-contained passage of **~130–170 words** that fully answers **one** concrete question, contains specifics, and names its source **within the same passage** (name + source, per the attribution convention). When geography matters to the topic, the passage states the relevant market explicitly. A well-formed article includes **at least 3** of these.

**Extractability criteria:** works without surrounding context; one question per passage; named source inside the passage; 130-170 words; market stated when relevant.

### Evidence Sandwich Block

Structure claims with evidence for maximum credibility.

```markdown
[Opening claim statement].

Evidence supporting this includes:
- [Data point 1 with source]
- [Data point 2 with source]
- [Data point 3 with source]

[Concluding statement connecting evidence to actionable insight].
```

**Extractability criteria:** ≥3 data points, each with its own source; conclusion connects evidence to action.

---

## Domain-Specific GEO Tactics

Different content domains benefit from different authority signals. For YMYL domains (health, finance, legal), these are **mandatory**, not optional — see the YMYL weighting in extractability-rubric.md.

### Technology Content
- Emphasize technical precision and correct terminology
- Include version numbers and dates for software/tools
- Reference official documentation
- Add code examples where relevant

### Health/Medical Content
- Cite peer-reviewed studies with publication details
- Include expert credentials (MD, especialidad, institución)
- Note study limitations and context
- Add "última revisión" dates; use `MedicalWebPage` schema

### Financial Content
- Reference regulatory bodies (in Chile: CMF, SII; elsewhere: SEC, FTC, etc.)
- Include specific numbers with timeframes
- Note that information is educational, not advice
- Cite recognized financial institutions

### Legal Content
- Cite specific laws, statutes, and regulations by full official name
- Reference jurisdiction clearly
- Include professional disclaimers
- Note when professional consultation is advised

### Business/Marketing Content
- Include case studies with measurable results
- Reference industry research and reports
- Add percentage changes and timeframes
- Quote recognized thought leaders

---

## Voice Search Optimization

Voice queries are conversational and question-based.

### Question Formats for Voice
English: "What is…", "How do I…", "Where can I find…", "Why does…", "When should I…", "Who is…"
Español: "Qué es…", "Cómo puedo…", "Dónde encuentro…", "Por qué…", "Cuándo debo…", "Quién es…", "Cuánto cuesta…"

### Voice-Optimized Answer Structure
- Lead with direct answer (under 30 words ideal)
- Use natural, conversational language
- Avoid jargon unless targeting expert audience
- Include local context where relevant (city, country, market)
- Structure for single spoken response
