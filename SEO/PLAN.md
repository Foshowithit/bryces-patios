# Bryce's Patios — Visibility Plan (re-planned, 1B budget)

**Objective.** Make Bryce's Patios (`brycespatios.work`) rank and be findable
everywhere a Mansfield-area homeowner looks, and prove it with dated measurements.
Budget 1,000,000,000 tokens. Keep going without pausing to ask.

**Why this file exists.** The thread's goal object cannot be re-created (the tool
rejects a second goal while one is active). This file *is* the goal: it is the
plan of record, and its status column is updated as work lands.

---

## Where we actually are (verified 2026-10-08)

| Thing | State |
|---|---|
| Live site | `https://brycespatios.work` — single page, GitHub Pages, clean `main` @ `e02b2bf` |
| Google Business Profile | **NONE.** This is the single biggest reason he is invisible on Maps. |
| Indexed pages | 1 (home) |
| Rich results | `LandscapingBusiness` + `FAQPage` on home only |
| Titles / H1 | Home title has keywords; **H1 is keyword-free** ("A better backyard starts here") |
| Sitemap | 1 URL |
| Brand SERP | site absent; Facebook page ranks instead |
| Reviews | 0 |
| Citations | 0 live (8.9 KB package ready in `SEO/CITATIONS.md`) |

---

## Workstreams + status

Legend: `TODO` · `WIP` · `DONE` · `HUMAN` (blocked on Bryce/user action)

### WS1 — Indexable multi-page site  `WIP`
Static HTML on GitHub Pages, no build step. Generator in `work/gen/` holds the
verified business data so every page's head, breadcrumb and JSON-LD are identical
in shape.

- [ ] `/learn/` hub + 6 guide pages split from the existing `#learn` articles
- [ ] 4 service pages: patios · walkways · retaining walls · fire pits
- [ ] 12 MA town pages: Mansfield, Attleboro, North Attleboro, Norton, Foxborough,
      Seekonk, Rehoboth, Plainville, Franklin, Taunton, Easton, Sharon
- [ ] Service × town matrix (`/patios/mansfield-ma/` etc.) — 4 services × top 6
      towns = 24 pages, each with genuinely unique local copy (never spun)
- [ ] Every page: unique title/meta · keyword-strong H1 · self-canonical ·
      OG/Twitter · voice-gated copy · shared `style.css` + `main.js`

### WS2 — Sitemap + crawl hygiene  `TODO`
- [ ] `sitemap.xml` with every URL + real `lastmod` from file mtime
- [ ] `<image:image>` extensions for key photos
- [ ] `robots.txt` stays intact
- [ ] `apple-touch-icon` + `site.webmanifest`
- [ ] keep `max-image-preview:large`
- [ ] submit sitemap + request indexing per URL in Search Console (after deploy)

### WS3 — Internal linking  `TODO`
- [ ] footer "Explore" column links home ↔ `/learn/` ↔ services ↔ towns
- [ ] on-page guides index
- [ ] every page ≤ 3 clicks from home, descriptive anchors

### WS4 — Home page fixes  `TODO`
- [ ] keyword-bearing H1 (or visible keyword subhead)
- [ ] audit the 39 em-dashes down (visible-copy ones are the risk, not comments)
- [ ] zero visible exclamation marks
- [ ] all copy passes `ow-writing-gate`

### WS5 — Google Business Profile  `HUMAN`
Package complete in `SEO/GBP.md` (741-char description, 20 service areas, photos,
hours, coords `42.022753, -71.256955`). Needs Bryce to verify. **Never fake it.**

### WS6 — Citations  `HUMAN` / partly ours
`SEO/CITATIONS.md` covers Apple/MapQuest/Bing Places/Yelp/BBB/Chamber/Facebook/
Nextdoor/YP/Angi/Thumbtack/Houz + local MA/RI. Most need accounts or phone
verification. We do everything that can be done without Bryce's identity.

### WS7 — Reviews  `HUMAN`
`SEO/REVIEWS.md`: QR + short link + reply templates. `aggregateRating` goes into
schema **only at ≥5 real reviews**. None yet. Never invent one.

### WS8 — Blog / education content  `TODO`
6+ noob-friendly patio-craft posts, AI-disclosed, voice-gated. Own copy — no slop.

### WS9 — Monitoring  `TODO`
Quiet weekly Google baseline (brand query, `patio installer mansfield ma`, GBP
status, new-review detection). **Notify only on meaningful change / completion /
failure / required user action.** Built with the `automation_update` tool.

### WS10 — Measurement  `WIP`
Dated before/after log in `SEO/BASELINE.md`: `site:` indexed count, brand SERP
position, local-pack presence, GBP views/calls/direction-requests, review count,
per-page impressions/clicks once Search Console exists. Google-only, ≤3 queries
per session.

---

## Schema / entity rules (every page)

- One `@id` scheme: `https://brycespatios.work/#business`, referenced from every
  page so Google merges the entity.
- Per page add `@id`-linked `WebSite` + `WebPage` + `BreadcrumbList`.
- `LocalBusiness` (`LandscapingBusiness`) + per-page `FAQPage` with 3–4 unique Q&As.
- **Remove `foundingDate: "2024"`** — unverified, do not assert it.
- **Add weekend `openingHoursSpecification`** to match the copy (Sat/Sun by
  appointment).

---

## Hard rules

- Never fabricate credentials, licences, insurance, warranties or reviews.
- Never use Gemini. Vision lane is `deepseek-v4.1-flash` via commandcode.
- AI imagery stays disclosed on the site.
- Copy stays simple and human — every new copy file passes `ow-writing-gate`
  before it is committed.
- Commit rule (`LAUNCH.md` §9): never mix layout and copy in one commit.

---

## Measure of done

All pages live and crawlable · brand query and `bryce patios mansfield` return the
site · GBP live · first reviews · before/after logged in `SEO/BASELINE.md` ·
everything pushed to `github.com/Foshowithit/bryces-patios`.
