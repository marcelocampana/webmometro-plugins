# Web Content: GEO/AEO + On-Page SEO

Criteria for writing web content (articles, blog posts, landing pages, guides) so it is
discoverable by search engines **and** quotable by AI assistants — applied **while drafting**,
not as a later cleanup. This file is business-agnostic: it names no brand, audience, or topic.
Read targets (keywords, audience, internal-link candidates, named entities) from the request,
the editorial brief, or the brand guidelines. Never invent them.

Voice always wins. These criteria shape structure and phrasing; they never override the brand's
voice, terminology, or tone.

> **GEO** (Generative Engine Optimization): get AI engines (ChatGPT, Perplexity, Gemini, Claude)
> to cite or recommend the content.
> **AEO** (Answer Engine Optimization): structure content so search assistants extract a direct
> answer.

---

## 0. SEO change tracking (read before drafting; register after)

In a shared client workspace (a `contexto/` directory at or above the working folder), the SEO
change log lives at `contexto/seo-tracking/cambios/`, produced by the **seo-change-tracker** skill
(seo-suite). It is shared cross-plugin truth — read it here **by pointer**, don't duplicate it.

- **Read before drafting web content for a page:** skim recent changes on that page/keywords so you
  don't undo or contradict a deliberate SEO change (e.g. a just-rewritten title, a new schema, a
  changed internal-link target), and so the copy builds on what was already done.
- **Register after, on hand-off:** if the user applies a copy rewrite that affects SEO/AEO (title,
  meta, headings, on-page content, internal links), **offer to register it in seo-change-tracker**
  so its impact can be measured later. That skill owns the registration and always asks for
  confirmation before writing.

Degrade silently if `contexto/seo-tracking/` doesn't exist — it's optional context, not a blocker.

---

## 1. Answer-first opening — the lead block

The very first block of the piece is the highest-leverage real estate for AEO: search engines
and AI Overviews extract the first clear answer they find, so the lead must *be* that answer.

- Open with a **self-contained block of ~40–60 words** whose **first sentence directly answers
  the main question** the piece exists to answer.
- Work the **exact target keyword** in naturally within the **first ~100 words**.
- The block must read as a **complete answer on its own** — it is what a featured snippet or AI
  Overview lifts — and still sound like the brand (persona, tone, and terminology from the
  guidelines; never its prohibited terms).
- Place it **before** the usual narrative/brand opening. You are not replacing the narrative
  lead — you are putting a direct answer in front of it. Burying the keyword inside a long
  warm-up intro cedes the snippet position. Voice and answer-first do not compete; they stack.

**Example** (generic brand "Lumen", a budgeting app; target keyword *emergency fund*):

> *Buried opening (avoid):* "Everyone hits the moment when an unexpected expense lands at the
> worst possible time. We've spent years watching people wrestle with that stress, and it's why
> we built what we built. In this guide we'll walk through the mindset shift that changes how you
> think about saving…" — the keyword and the actual answer arrive far too late.
>
> *Answer-first opening (preferred):* "**An emergency fund is three to six months of essential
> expenses set aside in a separate, easy-to-reach account.** At Lumen we help you build that fund
> automatically — a small amount tucked away each payday — so a surprise bill never turns into
> debt. Here's how to start, and the mindset shift that makes it stick." — answers in sentence
> one, exact keyword early, brand named and brand voice intact, then it hands off into the same
> narrative lead.


## 2. Quotable passages — the single most important GEO lever

AI assistants quote self-contained fragments that answer a question without needing the rest of
the article.

- Include at least **3 self-contained passages of ~130–170 words**.
- Each passage fully answers **one** concrete question the reader (or the brief) is asking.
- Each passage contains specifics with a **named source in the same passage** — not "studies
  show" but "according to [organization/publication, year]".
- When location matters to the topic, state the relevant geography/market explicitly (AI engines
  prioritize geographically relevant context).
- The named source in a quotable passage is the **condensed form** (name + source), not the full
  credential chain — see the attribution-without-redundancy convention in §4.

## 3. Question → answer structure

- Phrase section headings (H2/H3) as the **real questions users ask**, where natural.
- The **first sentences** under each heading give the direct answer — don't make the reader wait
  until the end of the section.
- No "warm-up" paragraphs that delay the answer more than 2–3 sentences.
- **Fact-first, voice-after (per section).** Open every section with a **neutral, self-contained
  factual claim** — the sentence an answer engine can lift verbatim without the surrounding
  paragraph. Place the brand's personal/relational framing (first person, anecdote, direct
  address) **immediately after**, never before. This applies the §1 answer-first principle not
  just to the lead block but to *every* section.
  - **AEO** rewards a neutral, autonomous answer; a claim wrapped in subjective framing
    ("we tell our clients that…") is weaker to lift than the bare fact.
  - **GEO** rewards the opposite — a named, credentialed, first-person voice is a trust/EEAT
    signal engines prefer to cite, especially on YMYL topics. So do **not** strip the brand voice
    to sound neutral.
  - **Resolution:** lead each section with the liftable fact; let the brand voice follow and wrap
    it. Subjective framing may **surround** the neutral answer, never **replace** it. Voice and
    answer-first **stack, they don't compete** — the same move as the lead block in §1, applied
    to each section.

## 4. Entity clarity

LLMs need precisely named entities to attribute information correctly.

- Name the **organization/brand** in full at least once.
- Name **people** with their title and credential the first time they appear.
- Name **laws, programs, products, and bodies** by their full official name.
- **Define** technical or proprietary terms the first time they are used.
- Re-name relevant entities **in each section** — don't fall back to "the institution" / "it".

**Attribution without redundancy.** Re-naming an entity is necessary; repeating its *full
credential* every time is not — it adds no new signal after the first mention and reads as heavy
and redundant. Use a three-level convention by mention position:

- **First mention — full introduction (once):** name + role + affiliation + source + (where/when).
  This is the only place the full chain appears; EEAT (§5) and entity clarity are satisfied here in
  one go.
- **Later mentions — short anchor:** an abbreviated form that keeps only the identifier relevant to
  that data point — surname when the expert's authority matters, institution when the figure/study
  matters, source when the origin of the testimony matters. Don't drag all four elements along each
  time.
- **Self-contained quotable passage (§2) — intermediate form:** name + source, the minimum for the
  fragment to stand on its own when an AI lifts it.

Anti-opposite-error rule: the short form is **still a proper noun** (surname or institution),
never a pronoun or generic ("the specialist", "the institution", "the same one") — that is exactly
what this section forbids. Vary the connectors ("according to", "details", "stated", "explained")
so the short form doesn't read like a template.

This convention **reinforces** §2/§4/§5 rather than contradicting them: every passage keeps a
named, traceable source; only the repeated credential — which carries no new signal after the
first mention — is dropped.

## 5. EEAT signals (Expertise, Experience, Authoritativeness, Trustworthiness)

Especially important for YMYL (Your Money or Your Life) topics — health, finance, legal, safety.

- Show direct **experience** with the topic where applicable.
- Back significant claims with **named experts or primary sources** (not "a study").
- **Cite the primary source, not a relaying medium.** When a claim reaches you through an outlet
  that is merely *relaying* it — a magazine, newsletter, aggregator, or news site (including the
  brand's own publication) — attribute it to the **original source**: the issuing body, the study
  with year, or the named person who said it. The relaying outlet may be added as a
  **complementary link** for verification and traffic, never as the attribution of origin. If the
  primary-source link isn't available while drafting, mark it (e.g. `[PENDIENTE-enlace-…]`) rather
  than defaulting the attribution to the outlet.
- Include an **authorship note** (name, role, credential) when the format allows.
- State the **dates** of data in the text itself, and acknowledge limits when relevant
  ("data available is from [year]; more recent figures may exist").
- Carry no prohibited terminology or tone from the brand guidelines.

## 6. FAQ section (when the topic warrants it)

- Questions are **real user questions** (e.g. from "People Also Ask"), not invented.
- Each answer is **direct and self-contained**, 40–80 words max.
- Mark questions as `H3` under an `H2` such as "Frequently asked questions".
- Emit `FAQPage` schema.

## 7. On-page SEO — title & meta

- **Title:** primary keyword in the first 3–5 words; ≤ ~60 characters; brand suffix at the end
  if the project uses one (e.g. "… | Brand").
- **Meta description:** includes the primary keyword naturally; ≤ ~155 characters; states what
  the reader will find; carries a clear benefit or reason to click.

## 8. On-page SEO — keyword placement

- **Primary keyword** appears in: the title, the **first ~100 words**, at least one **H2**, the
  **main image alt text**, and the **URL slug**. Natural density ~1–1.5% — no stuffing.
- **Secondary keywords** each appear at least once (H3, body, or FAQ); semantic variants woven
  in naturally.

## 9. Heading hierarchy

- Exactly **one H1** (the title).
- **H2** for main sections (at least one carries a secondary keyword); **H3** for subsections.
  Never skip a level (no H2 → H4).
- Headings are **descriptive**, not generic ("Why X costs more than Y", not "Introduction").

## 10. Internal links

- At least **2 internal links** to related content; **1 to the pillar/hub page** if one exists.
- Links are **woven into the body** — placed with descriptive anchor text at the thematic point
  where they apply, not only grouped in a "Related articles" block at the foot. When the project
  has an internal-linking map with suggested anchors, use those anchors.
- Anchor text is **descriptive** (not "click here").
- **Invite deeper reading with woven links, not meta-phrases.** Place the link on the natural
  anchor; do **not** announce the cross-reference with phrases like "this is covered in detail in
  the guide on…" / "see our article about…". A pointer that doesn't fit naturally in the body
  belongs in the related-articles list at the foot, not as a narrated aside.
- **Never expose internal content-architecture labels in reader-facing text.** Taxonomy or CMS
  terms (pillar/spoke/hub/cluster, internal IDs, file names) must not appear in the visible text —
  including the related-articles list. Use natural display text / link aliases.
- Note any already-published pages that should be updated to link back to this new piece.

## 11. Images & media

- Main image alt text contains the primary keyword; other images have descriptive alt text.
- Descriptive file names (`topic-keyword.jpg`, not `IMG_001.jpg`); compressed (< ~200 KB).

## 12. Schema markup

Emit the schema type(s) that fit the page, e.g.:
- `Article` (general articles); a domain-specific type when applicable (e.g. `MedicalWebPage`
  for health content).
- `FAQPage` when there is a FAQ section.
- `BreadcrumbList` for the navigation path.
- Core fields: `author`, `datePublished`, `dateModified`, `publisher`, `url`.

## 13. Crawlability & technical (verify when tooling is available)

- Main content is in **server-rendered HTML**, not JS-only.
- Not blocked in `robots.txt` for known AI/search bots (GPTBot, PerplexityBot, ClaudeBot,
  Googlebot); included in `llms.txt` if the domain uses one.
- Key data (figures, percentages, comparisons) is in extractable form: lists, tables, or short
  paragraphs with the data point + source in the same sentence.
- Core Web Vitals within targets (LCP < 2.5s, CLS < 0.1, INP < 200ms) — check with a PageSpeed /
  Lighthouse tool when one is connected.

## 14. Readability & visual breaks (scannability)

Purpose, in priority order: (1) give the reader **visual breaks** while reading (avoid walls of
prose), (2) make the content **scannable** (the eye can skim it), (3) make the **key data quick to
look up**.

**Structure is earned, not presumed.** A list or table is never added because you *believe* it
helps, to fill space, or out of SEO habit — only when it adds **real value to the reader**: there
is a genuine enumeration or a genuine contrast of comparable data underneath. When there is, use
structure; when there isn't, prose.

- No stretch runs more than ~3–4 paragraphs of continuous prose without a visual break: a list, a
  comparison table, a callout/blockquote, or a highlighted data point.
- Turn any enumeration of **3+ parallel items** (options, steps, requirements, signals) into a
  list.
- Turn any contrast of **2+ entities across 2+ dimensions** (e.g. option A/B/C, before/after, two
  opposing approaches) into a **comparison table**. Run this as an explicit test **per section**,
  not as a vibe over the whole piece: if a section lays out N options against M criteria (e.g. "what
  determines the price": factors × how each affects it), it has earned a table — render it as one.
- **Voice wins — but that is not a blanket license for prose.** Lists and tables give rhythm; they
  never replace the brand's *reflective* prose — philosophy, positioning, first-person narrative,
  emotional or judgment-bearing content — which must not be chopped into bullets. But a brand's
  stylistic preference for flowing prose does **not** exempt genuinely comparable data (a 2+×2+
  contrast, a set of parallel items) from becoming a table or list. Prose is the home of narrative
  and judgment; structure is the home of comparable data. Keep each in its own home — don't let a
  brand's prose voice annex data that the reader needs to scan, and don't let a table fragment a
  reflective passage. When two brand/format signals conflict, surface the trade-off explicitly
  rather than resolving it silently toward prose.
- **Anti-overuse:** no more than ~1 table per 2–3 sections; too many tables tire the reader as much
  as too much prose.
- **Why structure also helps discovery (GEO) — a by-product, never the justification:** a well-formed
  comparison table makes the data *extractable*. AI answer engines (Google AI Overviews, ChatGPT,
  Perplexity, Claude) and Google featured snippets lift structured data more readily than prose, and
  tables map directly onto comparative queries ("X vs Y", "how much does it cost", "which is
  better"). This visibility gain is a **consequence** of a table that already earned its place on
  reader value — it is never a reason to add one. A filler table helps no one: not the reader, not
  the engine. The value rule and the visibility gain point the same way.

---

## Coverage report (include in "Validate and Explain" for web content)

After drafting, report briefly:

| Dimension | Status | Notes / pending |
|-----------|--------|-----------------|
| Answer-first opening (lead, keyword in 1st sentence) | ✅ / ⚠️ / ⛔ | |
| Quotable passages (≥3, self-contained) | ✅ / ⚠️ / ⛔ | |
| Question → answer structure | ✅ / ⚠️ / ⛔ | |
| Entity clarity | ✅ / ⚠️ / ⛔ | |
| EEAT signals | ✅ / ⚠️ / ⛔ | |
| FAQ (if applicable) | ✅ / N/A | |
| Title & meta | ✅ / ⚠️ / ⛔ | |
| Keyword placement | ✅ / ⚠️ / ⛔ | |
| Heading hierarchy | ✅ / ⚠️ / ⛔ | |
| Internal links | ✅ / ⚠️ / ⛔ | |
| Schema noted | ✅ / ⚠️ / ⛔ | |
| Fact-first, voice-after (neutral claim opens each section) | ✅ / ⚠️ / ⛔ | |
| Readability / visual breaks (lists, tables, no walls of prose) | ✅ / ⚠️ / ⛔ | |
| Internal links woven into the body (not only at the foot) | ✅ / ⚠️ / ⛔ | |
| Internal links without meta-phrases ("covered in the guide on…") | ✅ / ⚠️ / ⛔ | |
| No internal-architecture labels in visible text (pillar/spoke/hub) | ✅ / ⚠️ / ⛔ | |
| Attribution without redundancy (1st full, then short form) | ✅ / ⚠️ / ⛔ | |
| Primary source cited (not a relaying medium; outlet = complementary link) | ✅ / ⚠️ / ⛔ | |

> Sources/claims are governed by the citation rule in the brand guidelines (e.g. "every figure
> carries a named source"). This module adds **no** separate claim-validation mechanism — rigorous
> validation (ledgers, source gates) is a separate downstream step.
