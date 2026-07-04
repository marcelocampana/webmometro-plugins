# How Each AI Platform Picks Sources

Each AI search platform has its own search index, ranking logic, and content preferences. This guide covers what matters for getting cited on each one, and which DataForSEO tool verifies visibility on it.

> **Vigencia de las cifras.** Statistics in this file were compiled ~February 2025 from dated studies: Princeton GEO study (KDD 2024), SE Ranking domain authority study, ZipTie content-answer fit analysis. Treat every percentage as a **directional heuristic**, not a current fact — re-verify before quoting exact figures in a report, and always cite them with their source and date ("según el estudio GEO de Princeton, KDD 2024…").

> **Mercados hispanos.** AI Overview availability and LLM answer behavior vary by country and language. Never assume US-market data applies: run every verification with the project's real `location_name`/`language_code` (e.g., Chile / `es`). If a platform or endpoint doesn't cover that market, the report must say "dato no disponible para este mercado" — which is a data limitation, not a finding against the content.

---

## The Fundamentals

Every AI platform shares three baseline requirements:

1. **Your content must be in their index** — Each platform uses a different search backend (Google, Bing, Brave, or their own). If you're not indexed, you can't be cited.
2. **Your content must be crawlable** — AI bots need access via robots.txt. Block the bot, lose the citation.
3. **Your content must be extractable** — AI systems pull passages, not pages. Clear structure and self-contained paragraphs win.

Beyond these basics, each platform weights different signals.

---

## Google AI Overviews

**Verify with DataForSEO:** `serp_organic_live_advanced` (detects the AI Overview item in the SERP and which sources it cites) and `ai_opt_llm_ment_*` with `platform: google`.

Google AI Overviews pull from Google's own index and lean heavily on E-E-A-T signals. At the time of the source studies they appeared in roughly 45% of US Google searches — coverage in Spanish-language markets differs and must be verified per query.

**What makes them different:** Google already has your traditional SEO signals — backlinks, page authority, topical relevance. The AI layer adds a preference for content with cited sources and structured data. The source studies correlated authoritative citations with a +132% visibility boost and authoritative (not salesy) tone with +89% (dated heuristics — see header).

**AI Overviews don't just recycle the traditional Top 10:** only ~15% of AI Overview sources overlapped with conventional organic results in the source data. Pages outside page 1 can get cited if they have strong structured data and clear, extractable answers.

**What to focus on:**
- Schema markup is the single biggest lever — Article, FAQPage, HowTo, Product (30-40% visibility boost in the source studies)
- Build topical authority through content clusters with strong internal linking
- Include named, sourced citations in your content (not just claims)
- Author bios with real credentials — E-E-A-T is weighted heavily
- Get into Google's Knowledge Graph where possible (an accurate Wikipedia entry helps)
- Target "how to" / "cómo" and "what is" / "qué es" query patterns — these trigger AI Overviews most often

---

## ChatGPT

**Verify with DataForSEO:** `ai_optimization_llm_response` (`llm_type: chat_gpt`, `web_search: true`), `ai_optimization_chat_gpt_scraper`, and `ai_opt_llm_ment_*` with `platform: chat_gpt`.

ChatGPT's web search draws from a Bing-based index, combined with training knowledge, citing the web sources it relied on.

**What makes it different:** Domain authority matters more here than on other AI platforms. The SE Ranking analysis (129,000 domains) attributed ~40% of citation likelihood to authority/credibility signals, ~35% to content quality, ~25% to platform trust. Sites with 350K+ referring domains averaged 8.4 citations per response vs. 6 for slightly lower trust scores.

**Freshness is a major differentiator:** content updated within the last 30 days was cited ~3.2x more often than older content.

**The most important signal is content-answer fit:** the ZipTie analysis (400,000 pages) attributed ~55% of citation likelihood to how well the content's style and structure match ChatGPT's own response format — far above domain authority (12%) or on-page structure (14%) alone. Write the way ChatGPT would answer the question.

**Beyond your site:** Wikipedia accounted for 7.8% of all ChatGPT citations, Reddit 1.8%, Forbes 1.1%. Third-party mentions carry significant weight.

**What to focus on:**
- Invest in backlinks and domain authority — the strongest baseline signal
- Update competitive content at least monthly
- Structure content the way ChatGPT structures answers (conversational, direct, well-organized)
- Include verifiable statistics with named sources
- Clean heading hierarchy (H1 > H2 > H3) with descriptive headings

---

## Perplexity

**Verify with DataForSEO:** `ai_optimization_llm_response` (`llm_type: perplexity`, `web_search: true`). Not covered by the LLM-mentions endpoints.

Perplexity always cites its sources with clickable links — the most transparent AI search platform. It combines its own index with Google's and runs multiple reranking passes, including ML-based quality evaluation that can discard entire result sets.

**What makes it different:** the most research-oriented engine. It maintains curated lists of authoritative domains (Amazon, GitHub, major academic sites) with inherent boosts, and uses a time-decay algorithm that evaluates new content quickly — fresh publishers get a real shot.

**Unique content preferences:**
- **FAQ Schema (JSON-LD)** — pages with FAQ structured data get cited noticeably more often
- **PDF documents** — publicly accessible PDFs (whitepapers, research reports) are prioritized; gated PDFs are invisible
- **Publishing velocity** — frequency matters more than keyword targeting
- **Self-contained paragraphs** — atomic, semantically complete paragraphs it can extract cleanly

**What to focus on:**
- Allow PerplexityBot in robots.txt
- Implement FAQPage schema on any page with Q&A content
- Host PDF resources publicly
- Add Article schema with publication and modification timestamps
- Write in clear, self-contained paragraphs that work as standalone answers
- Build deep topical authority in your specific niche

---

## Microsoft Copilot

**Verify with DataForSEO:** no direct endpoint — infer from Bing indexation and the shared fundamentals. Declare this limitation in the report when Copilot matters to the user.

Copilot is embedded across Microsoft's ecosystem (Edge, Windows, Microsoft 365, Bing) and relies entirely on Bing's index.

**What makes it different:** the Microsoft ecosystem connection. Mentions/content on LinkedIn and GitHub provide boosts other platforms don't offer. Copilot also weights page speed heavily — sub-2-second load times are a clear threshold.

**What to focus on:**
- Submit the site to Bing Webmaster Tools (many sites only submit to Google Search Console)
- Use IndexNow protocol for faster indexing
- Optimize page speed to under 2 seconds
- Write explicit, extractable entity definitions
- Build presence on LinkedIn (articles, company page) and GitHub if relevant
- Ensure Bingbot has full crawl access

---

## Claude

**Verify with DataForSEO:** `ai_optimization_llm_response` (`llm_type: claude`, `web_search: true`). Not covered by the LLM-mentions endpoints.

Claude uses Brave Search as its search backend when web search is enabled — not Google, not Bing. Brave Search visibility directly determines whether Claude can find and cite you.

**What makes it different:** extremely selective; very low citation rate but the highest precision standard. It looks for the most factually accurate, well-sourced content on a topic. Data-rich content with specific numbers and clear attribution performs significantly better than general-purpose content.

**What to focus on:**
- Verify your content appears in Brave Search results (search.brave.com)
- Allow ClaudeBot and anthropic-ai user agents in robots.txt
- Maximize factual density — specific numbers, named sources, dated statistics
- Use clear, extractable structure with descriptive headings
- Cite authoritative sources within your content
- Aim to be the most factually accurate source on your topic

---

## Gemini

**Verify with DataForSEO:** `ai_optimization_llm_response` (`llm_type: gemini`, `web_search: true`).

Gemini pulls from Google's index and Knowledge Graph. The Google AI Overviews guidance above largely applies: E-E-A-T, schema markup, topical authority, Knowledge Graph presence. `Google-Extended` in robots.txt governs both Gemini and AI Overviews grounding.

---

## Allowing AI Bots in robots.txt

If robots.txt blocks an AI bot, that platform can't cite the content. User agents to allow:

```
User-agent: GPTBot           # OpenAI — model training and search
User-agent: ChatGPT-User     # ChatGPT browsing mode
User-agent: OAI-SearchBot    # OpenAI — ChatGPT search index
User-agent: PerplexityBot    # Perplexity AI search
User-agent: ClaudeBot        # Anthropic Claude
User-agent: anthropic-ai     # Anthropic Claude (alternate)
User-agent: Google-Extended  # Google Gemini and AI Overviews grounding
User-agent: Bingbot          # Microsoft Copilot (via Bing)
Allow: /
```

**Training vs. search:** some AI bots serve both model training and search citation. To be cited without contributing to training, options are limited — GPTBot handles both for OpenAI (OAI-SearchBot is the search-specific crawler). **CCBot** (Common Crawl) can be blocked safely without affecting search citations — it only feeds training datasets. Present blocking decisions as a business tradeoff, never as an error.

**llms.txt:** an emerging convention — a Markdown file at `/llms.txt` that curates the site's key content for LLM consumption. Its adoption by platforms is uneven; check whether the domain publishes one and report it factually (presente / ausente), without treating its absence as a defect.

---

## Where to Start

Prioritize by where the audience actually is:

1. **Google AI Overviews** — largest reach; the site likely has Google SEO foundations already. Add schema, cited sources, E-E-A-T. Verify availability per query in the project's market first.
2. **ChatGPT** — the most-used standalone AI search for tech and business audiences. Freshness, domain authority, content-answer fit.
3. **Perplexity** — valuable for researcher/early-adopter audiences. FAQ schema, public PDFs, self-contained paragraphs.
4. **Copilot and Claude** — lower priority unless the audience skews enterprise/Microsoft (Copilot) or developer/analyst (Claude).

**Actions that help everywhere:**
1. Allow AI bots in robots.txt
2. Implement schema markup (FAQPage, Article, Organization at minimum; MedicalWebPage for health)
3. Include statistics with named sources
4. Update content regularly — monthly for competitive topics
5. Clear heading structure (H1 > H2 > H3)
6. Page load time under 2 seconds
7. Author bios with credentials
