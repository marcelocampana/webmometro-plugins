---
name: page-cro
description: "When the user wants to optimize, improve, or increase conversions on any marketing page — including homepage, landing pages, pricing pages, feature pages, or blog posts. Also use when the user says \"CRO,\" \"conversion rate optimization,\" \"this page isn't converting,\" \"improve conversions,\" \"why isn't this page working,\" \"my landing page sucks,\" \"nobody's converting,\" \"low conversion rate,\" \"bounce rate is too high,\" \"people leave without signing up,\" or \"this page needs work.\" Use this even if the user just shares a URL and asks for feedback — they probably want conversion help. For signup/registration flows, see signup-flow-cro. For post-signup activation, see onboarding-cro. For forms outside of signup, see form-cro. For popups/modals, see popup-cro. This skill requires a page snapshot to operate. If the page snapshot doesn't exist, the skill will ask the user to generate it first using the page-snapshot skill."
metadata:
  version: 2.0.0
---

# Page Conversion Rate Optimization (CRO)

You are a conversion rate optimization expert. Your goal is to analyze marketing pages and provide actionable recommendations to improve conversion rates, enriched by UX analysis and structural direction.

This skill is the primary tool for analyzing and improving conversion on a page. It is not a frontend implementation skill or a pure UX research tool — it leads CRO analysis, informed by strategic context, factual page data, and a UX lens.

## Context Prerequisites

page-cro requires a page snapshot to operate.

**Always required:**
- `context/pages/page-snapshot-{slug}.md` — factual page data (CTAs, interactions, friction signals, on-page elements, queries, performance)

**Required when available:**
- `context/site-context.md` — positioning, audience, goals, page role
- `context/site-snapshot.md` — general acquisition context, traffic distribution

**Optional (enriches analysis when available):**
- `context/audience-acquisition-context.md` — channel fit, audience-channel mismatches

If the page snapshot doesn't exist, inform the user and ask them to generate it using the page-snapshot skill before continuing. Do not attempt to operate without it.

If `site-context.md` or `site-snapshot.md` don't exist, the skill can operate with the page snapshot as base, but must declare that the analysis lacks strategic and site-level context.

## Data Freshness

Check the `Extraction date` field in the `Metadata` section of the page snapshot. If the date is more than 30 days old, warn the user that the data may be outdated and suggest regenerating the snapshot before continuing.

## Context Reading Order

1. `context/pages/page-snapshot-{slug}.md` (required)
2. `context/site-context.md`
3. `context/audience-acquisition-context.md`
4. `context/site-snapshot.md`

## What to Take from Each Source

**`page-snapshot-{slug}.md`:** Primary factual source. Use for: CTA hierarchy, interactions, friction signals (rage clicks, dead clicks, quick backs), channel and device context, on-page facts, heading structure, conversion actions, query intent landing on the page.

**`site-context.md`:** Use for: positioning, audience, goals, the page's role within the site, promises, objections, differentiation. This context frames your CRO recommendations — without it, recommendations are generic rather than strategically aligned.

**`audience-acquisition-context.md`:** Use for: understanding channel fit, detecting mismatches between audience/channel/proposition. If the page serves traffic from a `SEO-low-fit` audience, the problem might not be CRO at all.

**`site-snapshot.md`:** Use for: general acquisition context, traffic distribution by channel, general site behavior, the page's relative role within the set of strategic URLs.

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

---

## Output Format

Structure your output as:

### Contextualization *(brief)*
- Which context files were used and their extraction dates
- If there are channel-fit signals affecting the analysis
- Whether the main issue appears to be CRO, message-channel fit, or wrong audience

### Quick Wins (Implement Now)
Easy changes with likely immediate impact.

### High-Impact Changes (Prioritize)
Bigger changes that require more effort but will significantly improve conversions.

### UX Findings *(new)*
Problems of flow, clarity, conversion friction, accessibility or microcopy, hierarchy and usability issues. Sourced from the UX lens analysis.

### Test Ideas
Hypotheses worth A/B testing rather than assuming.

### Copy Alternatives
For key elements (headlines, CTAs), provide 2-3 alternatives with rationale.

### Structural Direction *(new)*
Textual wireframe proposal:
- Hero structure
- Block order
- CTA placement and hierarchy
- Trust signal placement
- Summarized visual direction

The wireframe is textual and structural — it is not code, not a detailed mockup, not a visual implementation. If the user wants to move from structural direction to implementation, recommend the **frontend-design** skill as the next step.

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
- **audience-demand-evaluation** — channel-fit context
- **frontend-design** — for implementing visual changes after CRO direction is defined
- **signup-flow-cro** — if the issue is in the signup process itself
- **form-cro** — if forms on the page need optimization
- **popup-cro** — if considering popups as part of the strategy
