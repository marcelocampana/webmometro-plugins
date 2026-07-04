---
name: brand-voice-enforcement
description: >
  This skill applies brand guidelines to content creation. It should be used when
  the user asks to "write an email", "draft a proposal", "create a pitch deck",
  "write a LinkedIn post", "draft a presentation", "write a Slack message",
  "draft sales content", or any content creation request where brand voice should
  be applied. Also triggers on "on-brand", "brand voice", "enforce voice",
  "apply brand guidelines", "brand-aligned content", "write in our voice",
  "use our brand tone", "make this sound like us", "rewrite this in our tone",
  or "this doesn't sound on-brand". Not for generating guidelines from scratch
  (use guideline-generation) or discovering brand materials (use discover-brand).
---

# Brand Voice Enforcement

Apply existing brand guidelines to all sales and marketing content generation. Load the user's brand guidelines, apply voice constants and tone flexes to the content request, validate output, and explain brand choices.

## Loading Brand Guidelines

Find the user's brand guidelines using this sequence. Stop as soon as you find them:

1. **Session context** — Check if brand guidelines were generated earlier in this session (via `/brand-voice-pro:generate-guidelines`). If so, they are already in the conversation. Use them directly. Session-generated guidelines are the freshest and reflect the user's most recent intent.

2. **Local guidelines file (workspace-aware)** — Check, in order: (a) `contexto/marca/brand-voice-guidelines.md` when a `contexto/` directory exists at or above the working folder (the shared client workspace convention — this is the canonical home); (b) `.claude/brand-voice-guidelines.md` in the working folder; (c) the legacy `.claude/brand-voice-pro-guidelines.md`. Do NOT use a relative path from the agent's current working directory — in Cowork, the agent runs from a plugin cache directory, not the user's project. Resolve the path relative to the user's working folder. If no working folder is set, skip this step.

   In a shared client workspace, also read `contexto/sitio.md` if present — its strategic context (audience, positioning, goals) frames on-brand content the same way it frames the seo-suite skills.

3. **Ask the user** — If none of the above found guidelines, tell the user:
   "I couldn't find your brand guidelines. You can:
   - Run `/brand-voice-pro:discover-brand` to find brand materials across your platforms
   - Run `/brand-voice-pro:generate-guidelines` to create guidelines from documents or transcripts
   - Paste guidelines directly into this chat or point me to a file"

   Wait for the user to provide guidelines before proceeding.

Also read `.claude/brand-voice-pro.local.md` for enforcement settings (even if guidelines came from another source):
- `strictness`: strict | balanced | flexible
- `always-explain`: whether to always explain brand choices

## Enforcement Workflow

### 1. Analyze the Content Request

Before writing, identify:
- **Content type**: email, presentation, proposal, social post, message, etc.
- **Target audience**: role, seniority, industry, company stage
- **Key messages needed**: which message pillars apply
- **Specific requirements**: length, format, tone overrides

**Web content detection.** If the content type is a piece that will live on the web and be
found by search engines or AI assistants — a **blog post, article, landing page, web page,
guide, or FAQ page** — flag this request as **web content**. When flagged, the Web Content
Module (below) is applied during Step 4 in addition to everything else. For all other content
(emails, Slack messages, proposals, decks, social posts), skip the module entirely and follow
the normal workflow unchanged.

When flagged as web content, also record the piece's **target keyword** up front. Take it from
the editorial brief or the content cluster it belongs to (e.g. the pillar/spoke topic) when one
is provided; if it isn't stated anywhere, ask the user for it before drafting. The answer-first
opening and the keyword-placement criteria both depend on knowing this keyword before the first
sentence is written.

### 2. Apply Voice Constants

Voice is the brand's personality — it stays constant across all content:
- Apply "We Are / We Are Not" attributes from guidelines
- Use brand personality consistently
- Incorporate approved terminology; reject prohibited terms
- Follow messaging framework and value propositions

Refer to `references/voice-constant-tone-flexes.md` for the "voice constant, tone flexes" model.

### 3. Flex Tone for Context

Tone adapts by content type and audience. Use the tone-by-context matrix from guidelines to set:
- **Formality**: How formal or casual should this be?
- **Energy**: How much urgency or enthusiasm?
- **Technical depth**: How detailed or accessible?

### 4. Generate Content

Create content that:
- Matches brand voice attributes throughout
- Follows tone guidelines for this specific content type
- Incorporates key messages naturally (not forced)
- Uses preferred terminology
- Mirrors the quality and style of guideline examples

For complex or long-form content, delegate to the `content-generation` subagent.
For high-stakes content, delegate to the `quality-assurance` subagent for validation.

**If the request was flagged as web content (Step 1), apply the Web Content Module below
while drafting** — voice and GEO/SEO are applied together, in the same pass, not as a
later cleanup.

### 5. Validate and Explain

After generating content:
- Briefly highlight which brand guidelines were applied
- Explain key voice and tone decisions
- Note any areas where guidelines were adapted for context
- For web content, also report GEO/SEO coverage (see the module's checklist below)
- Offer to refine based on feedback

When `always-explain` is true in settings, include brand application notes with every response.

## Web Content Module (articles, blog posts, web pages)

Apply this module **only** when Step 1 flagged the request as web content. It adds discovery
and answer-engine optimization to the draft **as it is written** — never bolted on afterward.
Voice always wins: GEO/SEO shapes structure and phrasing, but it never overrides the brand's
voice, terminology, or tone.

Read `references/web-content-geo-seo.md` for the full, business-agnostic criteria. While
drafting, build in:

- **Answer-first opening** — lead with a self-contained ~40–60-word block that answers the main
  question in its first sentence and works the **exact target keyword** in within the first ~100
  words, placed **before** the narrative/brand opening and still in the brand's voice (see the
  reference for the full criterion, rationale, and before/after example).
- **Quotable passages** — self-contained ~130–170-word answers, each fully answering one
  question with its source named in the same passage (these are what AI assistants cite).
- **Question → answer structure** — phrase section headings as real user questions where
  natural; answer directly in the first sentences of the section.
- **Fact-first, voice-after** — open each section with a neutral, liftable factual claim, then
  let the brand voice follow and wrap it; the neutral claim is what AEO extracts, the brand voice
  is what carries EEAT. They stack — never let subjective framing replace the neutral answer
  (see reference §3).
- **Entity clarity** — name key entities (brand, people with their credential, laws/programs by
  official name) precisely and repeatedly, not only on first mention. Re-naming an entity does
  **not** mean repeating its full credential each time: give the full chain (name + role +
  affiliation + source) on first mention, then a short proper-noun anchor (surname / institution /
  source) afterward — never a pronoun or generic (see reference §4).
- **FAQ section** — when the topic warrants it, with direct 40–80-word answers.
- **Keyword placement** — primary keyword in the title, first ~100 words, at least one H2, and
  the main image alt; secondary keywords distributed naturally.
- **Heading hierarchy** — a single H1; descriptive H2/H3; no skipped levels.
- **Readability / visual breaks** — give the reader visual breaks (no walls of prose), keep it
  scannable, and make key data quick to look up: break up any 3–4 paragraph prose run with a list,
  comparison table, or callout; turn 3+ parallel items into a list and 2+ entities across 2+
  dimensions into a table — without fragmenting reflective brand prose (see reference §14).
- **Internal links** — weave links into the body with descriptive anchor text at the thematic
  point where they apply, not only grouped in a "Related articles" list at the foot.
- **Schema** — note the appropriate schema type(s) for the page.

**On sources/claims:** do NOT add a separate claim-validation mechanism here. Web content
still follows the citation rule already defined in the brand guidelines (e.g. "every figure
carries a named source"). Apply that rule as part of voice — nothing extra. Rigorous claim
validation (ledgers, source gates) is a separate downstream step, out of scope for this skill.

Where the project provides ready-made GEO/SEO checklists or an editorial brief, prefer those
project files over the generic reference. Keep this module business-agnostic: read targets
(keywords, audience, internal-link candidates) from the request, the brief, or the guidelines —
never hardcode them.

## Handling Conflicts

When the user's request conflicts with brand guidelines:
1. Explain the conflict clearly
2. Provide a recommendation
3. Offer options: follow guidelines strictly, adapt for context, or override

Default to adapting guidelines with an explanation of the tradeoff.

## Open Questions Awareness

Open questions are unresolved brand positioning decisions flagged during guideline generation, stored in the guidelines under an "Open Questions" section. When generating content, check if the brand guidelines contain open questions:
- If content touches an unresolved open question, note it
- Apply the agent's recommendation from the open question unless the user specifies otherwise
- Suggest resolving the question if it significantly impacts the content

## Reference Files

- **`references/voice-constant-tone-flexes.md`** — The "voice constant, tone flexes" mental model, "We Are / We Are Not" table structure, and tone-by-context matrix explanation
- **`references/before-after-examples.md`** — Before/after content examples per content type showing enforcement in practice
- **`references/web-content-geo-seo.md`** — GEO/AEO + on-page SEO criteria to apply while drafting web content (articles, blog posts, pages). Loaded only when Step 1 flags the request as web content.
