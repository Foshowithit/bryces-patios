# Bryce's Patios — Visibility Plan (re-planned 2026-10-08, 1B budget)

**Objective.** Make Bryce's Patios (`brycespatios.work`) rank and be findable
everywhere a Mansfield-area homeowner looks — search, maps, AI answers, and the
local directories — and prove it with dated measurements.

**Budget.** 1,000,000,000 tokens. Keep going without pausing to ask.

**Why this file exists.** The thread's goal object cannot be re-created (the tool
rejects a second goal while one is active). This file *is* the goal: it is the
plan of record, and the status column is updated as work lands.

**Definition of done** (all verifiable, from the thread goal object):
1. Google Business Profile LIVE and verified at 885 West St Mansfield MA, NAP
   identical to the site, linked to brycespatios.work, 20 service areas, photos.
2. Site indexable: multi-page (home, `/learn/` hub, per-service, per-town,
   service×town), full `sitemap.xml`, internal linking, unique titles/metas,
   valid rich results (LocalBusiness + FAQ + Breadcrumb), keyword-strong H1s.
3. NAP reconciled everywhere (site, Facebook page, citations match exactly).
4. 30+ citations/submissions executed live.
5. Review engine live: QR + short-link request flow, GBP review link, reply
   templates, `aggregateRating` added only once ≥5 real reviews exist.
6. Monitoring automation running (quiet unless change).
7. Content: AI-disclosed gallery + 6+ noob blog posts, voice-gated, non-slop.
8. Measured: page 1 for brand queries, live GBP, first 5 reviews, page 1–2 for
   `patio installer mansfield ma`. Before/after tracked in `SEO/BASELINE.md`.

**Hard rules.** Never fabricate credentials, licences, insurance, warranties or
reviews. Never use Gemini. AI imagery stays disclosed. Every new copy file passes
`ow-writing-gate` before it is committed. Commit rule (`LAUNCH.md` §9): never mix
layout and copy in one commit. Google probing: ≤3 queries/session, 10–20 s apart,
≤1×/hour (Google walls the IP at 100.40.45.60).

---

## Where we are (verified 2026-10-08)

| Thing | State |
|---|---|
| Live site | `https://brycespatios.work` — 56 pages, GitHub Pages, `main` |
| Pages | 1 home · 1 learn hub · 12 guides · 1 services hub · 4 service · 1 areas hub · 12 town · 24 service×town = **56** |
| Sitemap | **56 URLs**, `<image:image>` on key photos |
| Rich results | `LocalBusiness` (`LandscapingBusiness`) + `FAQPage` + `BreadcrumbList`, `@id`-linked |
| Google Business Profile | **NONE.** Biggest single reason he is invisible on Maps. |
| Indexed pages | ~1 (fresh URL, no GBP, no backlinks yet) |
| Reviews | 0 |
| Citations | 0 live (package ready in `SEO/CITATIONS.md`) |
| Monitoring | weekly crontab watcher live (`~/tmp/bryce-seo-watch/watch.py`, Mon 09:00) |
| Voice gate | last full-site run **SHIP, 0/0/0, 0.9/100 (21,467 words)** |

---

## Workstreams + status

Legend: `TODO` · `WIP` · `DONE` · `HUMAN` (blocked on Bryce/user action)

### WS1 — Indexable multi-page site  `DONE`
Static HTML on GitHub Pages, no build step. Generator in `work/gen/` holds the
verified business data so every page's head, breadcrumb and JSON-LD are identical
in shape.
- [x] `/learn/` hub + 12 guide pages, split from the home `#learn` articles
- [x] 4 service pages · 12 MA town pages · 24 service×town pages (unique copy)
- [x] Every page: unique title/meta · keyword-strong H1 · self-canonical ·
      OG/Twitter · voice-gated copy · shared `style.css` + `main.js`

### WS2 — Sitemap + crawl hygiene  `DONE for us` (GSC submit = HUMAN)
- [x] `sitemap.xml` (56 URLs) + real `lastmod` from file mtime
- [x] `<image:image>` extensions for key photos
- [x] `robots.txt` intact · `apple-touch-icon` + `site.webmanifest`
- [x] `max-image-preview:large`
- [ ] **(HUMAN)** submit sitemap + request indexing per URL in Search Console

### WS3 — Internal linking  `WIP`
- [x] footer "Explore" column links home ↔ `/learn/` ↔ services ↔ towns
- [x] every page ≤3 clicks from home, descriptive anchors
- [ ] **Related-guides block** on every guide page (same topic family, 3 links)
- [ ] **Contextual in-prose links** from guides to the matching service page
- [ ] Service×town → parent town + parent service cross-links verified

### WS4 — Home page fixes  `DONE`
- [x] keyword-bearing H1 / visible keyword subhead
- [x] em-dash audit (visible copy clean) · zero visible exclamation marks
- [x] hero swapped to real photo, real 4-paver logo mark, new favicon
- [x] copy passes `ow-writing-gate` (SHIP, 0/0/0)

### WS5 — Google Business Profile  `HUMAN`
Package complete in `SEO/GBP.md` (741-char description, 20 service areas, photos,
hours, coords `42.022753, -71.256955`). Needs Bryce to create + verify. Never fake.
**This is the #1 leverage item: without it the business is invisible on Maps.**

### WS6 — Citations  `HUMAN` / partly ours
`SEO/CITATIONS.md` covers Apple/MapQuest/Bing Places/Yelp/BBB/Chamber/Facebook/
Nextdoor/YP/Angi/Thumbtack/Houz + local MA/RI. Most need an account or phone
verification. We do everything possible without Bryce's identity.

### WS7 — Reviews  `HUMAN`
`SEO/REVIEWS.md`: QR + short link + reply templates. `aggregateRating` goes into
schema **only at ≥5 real reviews**. None yet. Never invent one.

### WS8 — Blog / education content  `WIP`
- [x] 12 noob-friendly patio-craft guides live, AI-disclosed, voice-gated
- [ ] Thicken the thin pages (depth targets below), voice-gate each edit
- [ ] Planned guides (write only if copy is genuinely distinct, not spun):
      *"Retaining walls 101"* · *"Fire pit types and siting"* ·
      *"Drainage around a foundation"* · *"Prepping a yard for a patio"*

### WS9 — Monitoring  `DONE`
Quiet weekly watcher live via crontab (Mon 09:00). Notifies only on meaningful
change / completion / failure / required user action. Last run: 56 OK / 0 BAD.

### WS10 — Measurement  `WIP`
Dated before/after log in `SEO/BASELINE.md`: `site:` indexed count, brand SERP
position, local-pack presence, GBP views/calls/direction requests, review count,
per-page impressions/clicks once Search Console exists. Google-only, ≤3/session.

### WS11 — Discovery plumbing  `WIP` (new)
Getting the 56 URLs *noticed* now, not in six weeks.
- [ ] `feed.xml` (Atom) + `<link rel="alternate">` in `head()` and footer link
- [ ] **IndexNow** key file at site root + ping script for all 56 URLs
      (Bing/Yandex/Seznam; Google does not participate — be honest about that)
- [ ] Sitemap ping to Google + Bing on each deploy
- [ ] `SEO/` ops scripts documented in `SEO/README.md`

### WS12 — Off-site signal  `WIP` (new, ours where possible)
- [ ] Facebook page → site link verified in NAP (do NOT edit the page without
      Bryce; note the ask)
- [ ] Post the 12 guides as FB posts (draft only until Bryce approves)
- [ ] One photo-driven FB post template per service for Bryce to reuse

---

## Content depth targets (words, visible text)

Current average across 56 pages ≈ 432 w. Thin pages to thicken:
`learn/your-questions` 254 · `learn/frost` 310 · `areas/sharon` 328 ·
`areas/rehoboth` 330 · `learn/paver-cost` 429 · `areas/mansfield` 351.

Targets: guide pages ≥ 550 w · town pages ≥ 420 w · service×town ≥ 400 w.
Add real information, never filler: cost ranges, frost depth, drive times, yard
types, material behavior, timelines, and the failure modes a homeowner can check.

---

## Schema / entity rules (every page)

- One `@id` scheme: `https://brycespatios.work/#business`, referenced from every
  page so Google merges the entity.
- Per page add `@id`-linked `WebSite` + `WebPage` + `BreadcrumbList`.
- `LocalBusiness` (`LandscapingBusiness`) + per-page `FAQPage` with 3–4 unique Q&As.
- **Remove `foundingDate`** — unverified, do not assert it.
- Weekend `openingHoursSpecification` matches the copy (Sat/Sun by appointment).
- `sameAs` = the single live Facebook page only.

---

## Authority / E-E-A-T notes

- The site must read as a real, local, owner-operated business: real address,
  real phone, real photos, plain answers, no invented credentials.
- Every claim on the page must be something Bryce could stand behind in person.
- Do not claim licence, insurance, warranty, years-in-business or review counts.
- AI imagery is disclosed; real job photos are labeled as real.
- Author voice: one person who digs and lays the stone explaining what he does.
  Short sentences. Concrete numbers. No marketing adjectives, no em-dashes.

---

## Measure of done

All pages live and crawlable · brand query and `bryce patios mansfield` return the
site · GBP live · first reviews · before/after logged in `SEO/BASELINE.md` ·
IndexNow + feed live · everything pushed to
`github.com/Foshowithit/bryces-patios`.
