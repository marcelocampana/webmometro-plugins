# Web Performance & Core Web Vitals

This reference is the canonical performance-interpretation layer for the SEO suite. `seo-audit`
owns it; `page-cro` and `ai-seo` point here rather than duplicating thresholds or optimization
guidance. It converts the **raw, unrated** PageSpeed/CrUX numbers recorded in the snapshots
(`snapshot-sitio.md`, `snapshot-pagina-{slug}.md`) into ratings, diagnosis, and fixes.

Snapshots are data-only by design: they store `LCP = 3200 ms`, never "LCP is poor." The rating
lives here, in the analytical layer, so the factual baseline stays unbiased.

## Lab data vs. field data — read them differently

| | Lab (Lighthouse) | Field (CrUX) |
|---|---|---|
| Source | Simulated single run | Real users, 28-day rolling p75 |
| In the snapshot | `mcp__dataforseo__on_page_lighthouse` fallback (desktop, lab-only) or PSI script | PSI/CrUX via the shared `pagespeed_field.py` script (only when a Google API key is configured) |
| Use for | **Debugging** — pinpoint the cause (which resource, which element) | **Verdict** — whether real users pass Core Web Vitals |

Rules when interpreting the snapshot:
- **Field data is the source of truth** for whether a page passes CWV. If the snapshot has field
  (CrUX) values, rate against those.
- **Lab data is diagnostic only.** A good lab score does not mean users are having a good
  experience; use it to explain *why* a field metric is bad, not to overrule it.
- If the snapshot marks field data as **unavailable** (no API key configured → DataForSEO
  lab-only fallback), say so explicitly in the finding and rate on lab data *provisionally*,
  recommending the user enable CrUX field data for a real verdict. Never present a lab number as
  if it were real-user performance.

## Thresholds

### Core Web Vitals (rate at the 75th percentile)

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ 2.5 s | 2.5 s – 4.0 s | > 4.0 s |
| **INP** (Interaction to Next Paint) | ≤ 200 ms | 200 ms – 500 ms | > 500 ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |

### Supporting metrics

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| **FCP** (First Contentful Paint) | ≤ 1.8 s | 1.8 s – 3.0 s | > 3.0 s |
| **TTFB** (Time to First Byte) | ≤ 0.8 s | 0.8 s – 1.8 s | > 1.8 s |

### Lighthouse category scores (lab)

| Score | Rating |
|---|---|
| 90–100 | Good 🟢 |
| 50–89 | Needs Improvement 🟡 |
| 0–49 | Poor 🔴 |

A page "passes" Core Web Vitals only when **LCP, INP, and CLS are all in Good** at p75.

## Diagnosis → fix, by metric

Recommend fixes in this priority order: (1) the failing Core Web Vital with the most affected
users, (2) the specific resource or element causing it, (3) supporting metrics. Tie each
recommendation to the metric it moves.

### Slow LCP (usually image, web font, or slow server)

The LCP element is typically the hero image, a heading, or a large text block. Identify it, then:

- Serve modern formats (WebP/AVIF), compress, and size responsively with `srcset`/`sizes`.
- Set explicit `width`/`height` (also prevents CLS) and **do not** lazy-load the LCP image.
- Preload the LCP resource; preconnect to its origin if it is cross-origin.

```html
<link rel="preconnect" href="https://cdn.example.com" />
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high" />
<img src="/hero.webp"
     srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
     sizes="(max-width: 600px) 400px, 1200px"
     width="1200" height="800" alt="…" />
```

Server-side: reduce TTFB (caching, CDN, faster backend) — a slow TTFB caps LCP no matter what
the front end does.

### Poor INP (main-thread blocked by JavaScript)

- Break up long tasks; defer or lazy-load non-critical JS.
- Reduce third-party script weight and load it `async`/`defer`.
- Avoid large synchronous work on interaction handlers.

```html
<script src="/app.js" defer></script>
<script async src="https://analytics.example.com/a.js"></script>
```

### High CLS (layout shifting during load)

- Reserve space: explicit dimensions or `aspect-ratio` for images, videos, ads, and embeds.
- Never insert content above existing content after load.
- Use `font-display: optional`/`swap` and preload fonts to avoid late reflow.

```css
.media { width: 100%; aspect-ratio: 16 / 9; }
```

### Render-blocking CSS/JS (hurts FCP and LCP)

- Inline critical CSS; defer the rest.
- Add `defer`/`async` to scripts; remove unused CSS/JS; code-split routes.

```html
<link rel="preload" href="/styles.css" as="style" onload="this.rel='stylesheet'" />
```

### Inefficient fonts (FOIT/FOUT, layout shift)

- `font-display: swap` (or `optional`), preload the critical font, subset to needed glyphs,
  prefer `woff2`, and fall back to system fonts where acceptable.

### No caching / repeat-visit slowness

- Long-lived, immutable `Cache-Control` for static assets; serve via CDN.

```
Cache-Control: public, max-age=31536000, immutable
```

## Reporting guidance

- Rate each metric with the tables above and state the data type (field vs. lab) behind each
  rating. Flag any metric where the snapshot only has lab data.
- When you propose a fix, name the metric it targets and the expected direction of movement.
- If the fix touches title/meta copy or any user-facing text, defer copy production to
  **brand-voice-enforcement** (see the Brand Voice Guardrail) — this reference gives technical
  direction only.
- Recommended actions still follow the parseable-checklist format (`slug`, `area`, `target_url`,
  `prioridad`) so they reconcile against **seo-change-tracker**. Performance fixes use
  `area: tecnico`.

## Official references (indexable)

- PageSpeed Insights: https://pagespeed.web.dev/ · https://developers.google.com/speed/docs/insights/v5/about
- Core Web Vitals: https://web.dev/vitals/ · thresholds: https://web.dev/defining-core-web-vitals-thresholds/
- CrUX (field data): https://developer.chrome.com/docs/crux/
- Optimize LCP: https://web.dev/optimize-lcp/ · INP: https://web.dev/optimize-inp/ · CLS: https://web.dev/optimize-cls/
