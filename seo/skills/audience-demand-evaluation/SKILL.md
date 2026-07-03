---
name: audience-demand-evaluation
description: "When the user wants to evaluate whether a target audience is reachable through organic search or needs alternative acquisition channels. Also use when the user mentions \"demand evaluation,\" \"audience demand,\" \"is there search demand,\" \"can we reach this audience with SEO,\" \"channel fit,\" \"acquisition channel,\" \"organic feasibility,\" \"is SEO the right channel,\" or wants to understand if low organic performance is due to execution problems or lack of demand. This skill uses MCPs for targeted demand validation queries — it is not a data extraction skill. For factual site data, see site-snapshot. For SEO diagnosis, see seo-audit."
metadata:
  version: 1.0.0
---

# Audience Demand Evaluation

You evaluate, per audience, the potential organic demand, real SEO feasibility, and the most suitable acquisition channel or motion.

The output is `context/audience-acquisition-context.md` — a reference document that seo-audit and page-cro can read to distinguish execution problems from demand limitations.

## Why This Skill Exists

Many sites assume that all their audiences are reachable through SEO. When organic traffic is low, the default diagnosis is "we have an SEO problem." But sometimes the real issue is that the audience doesn't search for what the site offers — they discover solutions through LinkedIn, outbound sales, events, or referrals. This skill exists to separate demand from capturability, so downstream diagnosis (seo-audit) and conversion analysis (page-cro) start from accurate premises.

## Language

Write section headers and field names in English.

Write all user-facing communication in Spanish neutro.

Content inside tables stays in the language of the source or query.

## Context Prerequisites

**Required (read):**
- `context/site-context.md` — audiences, JTBD, pains, use cases
- `context/site-snapshot.md` — GSC signals, organic visibility

If these files don't exist, ask the user to generate them first using site-context and site-snapshot.

**Not used:**
- Page snapshots — demand evaluation is audience-level, not page-level

## Use of MCPs

This skill is an exception to the general rule that only snapshots query MCPs. audience-demand-evaluation needs to validate demand hypotheses with data that is not in the snapshots:

- Search volume for keywords the site doesn't yet rank for (not in the snapshot's GSC data)
- SERP competition and difficulty for hypothetical query families
- Aggregated volume by query family

These queries are targeted and bounded (see execution limits), not full dataset extractions.

**MCPs used:**
- **DataForSEO** — search volume by keyword, SERP competition
- **GSC** — queries with real traffic to the site (cross-reference with snapshot data)

## Methodology

For each audience:

1. **Take definition from `site-context.md`** — audience, JTBD, pains, use cases
2. **Build query family hypotheses** — generate seed keywords for applicable families
3. **Validate with DataForSEO** (volume, competition) and **GSC** (existing real traffic)
4. **Separate existing demand from current capturability** — high volume doesn't mean the site can capture it; low GSC traffic might mean poor execution or no demand
5. **Classify channel fit**

## Query Families

- **problem-aware** — searches describing the problem without naming solutions
- **solution-aware** — searches naming solution categories
- **category** — searches for the product category
- **role-based** — searches tied to a job role or function
- **use-case** — searches describing specific scenarios
- **comparison** — "X vs Y" searches
- **alternative-to** — "alternative to X" searches
- **industry-specific** — searches tied to a vertical or industry

Not all families apply to every audience. Evaluate relevance before querying — in practice, 4-5 families per audience is typical. If a family clearly doesn't apply (e.g., "alternative-to" for a category creator with no known alternatives), skip it.

## Channel Fit Classification

| Classification | Meaning |
|---|---|
| `SEO-primary` | High and capturable organic demand |
| `SEO-secondary / mixed` | Organic demand exists but the channel needs support |
| `Channel-mixed` | Audience responds better to combined channels |
| `SEO-low-fit` | Audience doesn't actively search; LinkedIn, outbound, or paid are more realistic |
| `Insufficient evidence` | Not enough signals to classify |

## Execution Limits

| Dimension | Limit |
|---|---|
| Audiences per execution | Max 5. If site-context defines more, ask the user to prioritize. |
| Query families per audience | Max 8 (the defined ones). Evaluate relevance first; in practice, 4-5. |
| Seed keywords per family | Max 10 terms. |
| Keyword ceiling per audience | ~50 in worst case. |
| Total keyword ceiling | ~250 if 5 audiences at maximum. |
| Volume validation | Batch keywords for DataForSEO volume queries. |
| Detailed SERP queries | Limit to 3-5 highest-volume keywords per audience. |
| Total MCP calls ceiling | 15-25 per full execution. |

## Early Stopping Criterion

If an audience produces no signals in GSC and no relevant volume in DataForSEO after evaluating the first 3 query families, classify it as `Insufficient evidence` and stop further investigation. This prevents wasting MCP calls on audiences with no detectable search behavior.

## Output Structure

`context/audience-acquisition-context.md` must include:

1. **Metadata** — extraction date, site, audiences evaluated, sources used
2. **Audience Definitions** — summary of each audience from site-context
3. **Methodology** — brief description of approach and limits applied
4. **Audience Reachability Assessment** — per audience: hypothesized query families, observed signals, external demand validation, organic feasibility, recommended acquisition motion, confidence, caveats
5. **Search Demand Signals** — supporting tables with volume, competition, and existing traffic data
6. **Channel Fit Summary** — table with all audiences and their classification
7. **Confidence and Caveats** — limitations, data gaps, assumptions

Minimum fields per audience:
- Audience / Segment
- Hypothesized query families
- Observed signals (from GSC/snapshot)
- External demand validation (from DataForSEO)
- Organic feasibility
- Recommended acquisition motion
- Confidence
- Caveats

## Validation Rules

- Do not conclude "no demand" solely from low GSC visibility — the site might just not be ranking
- Always separate demand (does the search volume exist?) from capturability (can this site realistically capture it?)
- Do not use page snapshots as source
- Can classify B2B audiences with motion `LinkedIn/outbound` when SEO is not the primary channel

## Related Skills

- **site-context** — provides audience definitions and strategic context
- **site-snapshot** — provides GSC signals and organic visibility baseline
- **seo-audit** — reads this output to distinguish execution vs. demand problems
- **page-cro** — reads this output to understand channel-fit mismatches
