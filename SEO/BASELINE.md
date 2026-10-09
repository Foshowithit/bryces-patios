# Bryce's Patios — Search Baseline (session 17, 2026-10-08)

**Why this file exists:** you cannot prove SEO work did anything without a dated
"before" snapshot. This is that snapshot. It is intentionally unflattering.

## Method (and why it matters)

The **only** reliable SERP instrument on this machine is **Google, read through a real
Chrome browser** (`ego-browser`), with `hl=en&gl=us&pws=0&nfpr=1` (no personalisation,
no auto-correct).

Everything else was tested and is **unusable on this box** — recorded here so no future
session wastes hours re-testing them:

| Instrument | Result when tested |
|---|---|
| Bing HTML | Serves geo-broken / irrelevant results even to a logged-out real browser |
| DuckDuckGo HTML | 0 results returned |
| Startpage | 0 results |
| Mojeek | 0 results |
| `curl` + scraper | Blocked / consent-walled |

**Google rate-limits hard from this IP.** After ~3–4 searches it serves the
"unusual traffic" interstitial (IP `100.40.45.60`). Baseline runs must therefore be
**≤3 queries per browser session with 10–20 s spacing**, or spread across the day.
Two queries in the 2026-10-08 run returned the interstitial and are marked
`BLOCKED — re-read` below.

## Baseline table (checked 2026-10-08)

| Query | Bryce's site ranks? | What actually ranks | Notes |
|---|---|---|---|
| `brycespatios` | **No** | Google auto-corrects to "bryce patios"; no organic result for the domain | Entity is *known to Google* but not linked to the site |
| `bryce patios mansfield` | **No** | **#1 = Facebook page "Bryces Patio Service and Landscape \| Mansfield MA"** with the correct 885 West St | A Facebook page is doing the website's job |
| `"bryces patios" mansfield ma` | **No** (Map only) | Google Map pin shown; brand recognised | No organic listing |
| `stone patio installer mansfield ma` | **No** | #1 Stonewalls 2 Patios → Backyard Patios → Houzz → D.R. Stonework → Yelp/Angi lists | AI Overview names Stonewalls 2 + Collins |
| `patio installer mansfield ma` | **No** | #1 **Stonewalls 2 Patios, Inc.**, then aggregators (Houzz, Yelp, buildzoom, Thumbtack) | Local pack = Collins Landscaping + Stonewalls 2 |
| `patio installers near me mansfield` | **BLOCKED — re-read** | — | Google interstitial |
| `"brycespatios.work"` | **BLOCKED — re-read** (brand+domain matched before the wall) | — | Google interstitial |
| `hardscaping mansfield ma` | **BLOCKED — re-read** | — | Google interstitial |
| Google Maps: `bryce patios mansfield ma` | **No listing at all** | Only **Stonewalls 2 Patios, Inc.** appears | **There is no Google Business Profile for Bryce.** |

## The single most important finding

**Bryce has no Google Business Profile.** That is the reason the site is invisible in
every local query. Organic ranking for "patio installer mansfield ma" is a multi-year
fight; the **local pack is decided largely by GBP presence, categories, service area,
photos and reviews** — all of which Bryce currently has zero of. A GBP can be created
today and is the highest-leverage single action available.

## Competitor set (for tracking)

| Business | Rating | Reviews | Notes |
|---|---|---|---|
| **Stonewalls 2 Patios, Inc.** | 5.0 | 28 | 20 Cabot Blvd Ste 300, Mansfield MA 02048 · (978) 230-9060 · the #1 result on every commercial query |
| **Collins Landscaping** | 4.9 | 67 | 10 Otis St · (774) 219-7879 · appears in the local pack |
| **D.R. Stonework & Masonry** | — | — | Ranks on branded-ish queries |

## What "done" looks like (measurable)

1. Site appears **on page 1** for `brycespatios` and `bryces patios mansfield` (brand queries —
   easiest win, purely a matter of getting indexed + a linked entity).
2. A **live Google Business Profile** with correct NAP, category, 20-town service area,
   ≥15 photos, and the website linked.
3. **First 5 Google reviews** live, with `aggregateRating` then added to the site schema.
4. Site appears on **page 1–2** for `patio installer mansfield ma` (hard; long game).
5. `SEO/BASELINE.md` re-run monthly; changes logged.

## Re-run procedure

```
cat > /tmp/baseline.js <<'JS'
const task = await taskSpace("baseline");
const page = task.page("p1");
for (const q of ["brycespatios","bryce patios mansfield","patio installer mansfield ma"]) {
  await page.goto("https://www.google.com/search?q="+encodeURIComponent(q)+"&num=20&hl=en&gl=us&pws=0&nfpr=1",
                  {waitUntil:"domcontentloaded",timeout:30000});
  await page.waitForTimeout(9000);
  const r = await page.evaluate(()=>({
    blocked:/unusual traffic|Before you continue/i.test(document.body.innerText.slice(0,1200)),
    items:[...document.querySelectorAll("#rso h3")].slice(0,10).map(h=>h.innerText.trim()),
    brandHit:/bryce'?s patios/i.test(document.body.innerText)}));
  console.log(q, JSON.stringify(r));
  await page.waitForTimeout(12000);
}
await task.finish({keep:[]});
JS
timeout 200 ~/.local/bin/ego-browser nodejs < /tmp/baseline.js
```
Run **≤3 queries**, never more than once an hour, or Google walls the IP.


---

## After — first deploy (2026-10-08, session 17)

The site shipped this session. Everything below is **machine-verified**, not claimed.

| Check | Result |
|---|---|
| Pages emitted | **55** (3 hubs + 12 guides + 4 services + 12 MA towns + 24 service×town) |
| `sitemap.xml` URLs | **56** (55 pages + `/`) |
| Live HTTP sweep | **56 OK / 0 BAD** (every sitemap `<loc>`, desktop UA, 2026-10-08) |
| `/learn/` hub | **12** guide cards rendered |
| New guides live | 6 new (`paver-cost`, `patio-vs-concrete`, `winter-ready`, `choosing-contractor`, `driveway-aprons`, `yard-grades`) — all 200 |
| Canonical + JSON-LD | correct on home, `/learn/`, guides, town pages (browser-verified) |
| Cache version | `?v=b8d52f03` on `style.css` + `main.js` |
| Working tree | clean at commit `287724c` |

**Still not done (human):** Google Business Profile (§"single most important finding"
above — this is *the* blocker on local visibility); Search Console sitemap submit +
per-URL indexing requests; citations; reviews. The site can rank for **brand + long-tail
guide queries** without a GBP, but **cannot enter the local pack** without one.

The `BLOCKED — re-read` rows in the baseline table above are historical (Google
interstitial); they are left in place as a record of that run.

### Watch run — 2026-10-08 20:08 EDT

- Sitemap: **56** URLs · live **OK 56 / BAD 0**
- /learn/ hub: **12** guide cards
- Facebook public page: unreadable
- SERP: skipped (use --serp, Google rate-limits this IP)
- No change, nothing broken.

### Content-depth pass — 2026-10-08 (ck64)

Full-site depth rebuild, copy-only.

| Check | Result |
|---|---|
| Pages emitted | **56** |
| Word depth (site avg) | **507** (was 479) |
| Min page depth | **400** (`areas/north-attleboro/walkways`, `areas/norton/walkways`) |
| Guides ≥550 words | **12 / 12** — none below 550 |
| Town pages ≥420 words | **12 / 12** — none below 420 |
| Service×town ≥400 words | **24 / 24** — none below 400 |
| Voice gate (human-voice) | **SHIP — fatal=0 tier1=0 p1=0, 1.3/100 (24,740 words)** |

Depth history: 314 → 325 → 378 → 398 → 423 → 435 → 462 → 479 → **507**.
Fixed one filler phrase ("in terms of") that the gate flagged in `learn/yard-grades`.

### After-log — ck65 … ck73 (2026-10-08, content + discovery + internal links)

Five commits landed since ck64. Everything below is re-measured, not estimated.

| Commit | What | Verified result |
|---|---|---|
| `6b1d92a` | fix titles (double-escaped `&`), cap at 65 chars, top up Foxborough fire-pit copy | 0 titles >65, 0 duplicates |
| `fe04028` | `.work__note--disclosure` style modifier (single rule, no double rule) | layout only |
| `abb86ea` | on-page AI-imagery disclosure in the work gallery + footer note | visible, voice-gated |
| `86c017f` | visible FAQ + `FAQPage` schema on **all 56 pages**; added a visible `<section id="faq">` (4 `<details class="qa">`) to home matching its JSON-LD verbatim | home `id="faq"`=1, `class="qa"`=4 |
| `03cb1d3` | service pages link to their 6 service×town children + sibling services (`<nav class="related">`) | 6 `/areas/*/*/` links on each of 4 service pages |

**Depth after ck73 (visible text, `<main>` only):**

| Bucket | n | min | avg | threshold | fails |
|---|---|---|---|---|---|
| Guides (`learn/*/`) | 12 | **732** | 764 | ≥550 | **0** |
| Town pages (`areas/*/`) | 12 | **617** | 640 | ≥420 | **0** |
| Service×town (`areas/*/*/`) | 24 | **404** | 422 | ≥400 | **0** |
| Content pages total | 48 | — | **562** | — | — |

Depth history: 314 → 325 → 378 → 398 → 423 → 435 → 462 → 479 → 507 → **562**.

**Titles/metas:** 56 pages · 0 titles >65 chars · 0 duplicate titles · 0 metas
outside 110–165.

**Voice gate:** `SHIP — fatal=0 tier1=0 p1=0, score 1.3/100 (**29,598 words**)`
(was 24,740 at ck64).

**Discovery plumbing now live:**
- `<link rel="alternate" type="application/atom+xml">` in generated `head()` and
  now also on **home** (`index.html` L37 — home is hand-maintained, so it had to
  be added by hand; generated pages inject it automatically).
- Footer "Guides feed" link on every page · `feed.xml` = 13 entries.
- IndexNow key file `b8be78077b664cf338d750ff4799d248.txt` at root · ping script
  `work/indexnow-ping.sh` → `HTTP 200` after every push.
  (Bing/Yandex/Seznam only — **Google does not participate**; do not retry Google.)
- `sitemap.xml` = 56 URLs, real `lastmod` from file mtime.

**Watcher (weekly Mon 09:00):** 56 OK / 0 BAD, 12 guide cards on `/learn/`,
nothing broken.

---

## After-log — ck74 … ck89 (2026-10-08, content depth + keyword + deploy)

Re-measured, not estimated. HEAD at time of writing: **`e978d12`** (Actions
`completed success`, 2026-10-09T02:19Z), deploy live ~1 min after push.

| Metric | Value |
|---|---|
| Pages live | **81 / 81 → HTTP 200** (full sweep) |
| Pages emitted by generator | 80 + 1 hand-maintained home = 81 |
| Sitemap | **81 URLs** |
| Feed | **14 entries** (`/learn/` hub + 13 guides) |
| Guides | **13** |
| Service×town pages | **48 / 48** (was 24) |

**Depth after ck89 (visible text, `<main>` only):**

| Bucket | n | min | avg | threshold | fails |
|---|---|---|---|---|---|
| Guides (`learn/*/`) | 13 | **732** | 779 | ≥550 | **0** |
| Town pages (`areas/*/`) | 12 | **617** | 642 | ≥420 | **0** |
| Service×town (`areas/*/*/`) | 48 | **415** | 444 | ≥400 | **0** |
| Content pages total | 73 | — | **536** | — | — |

Depth history: … → 507 → 562 → **536** (avg dips because 24 extra service×town
pages, which are deliberately shorter, joined the set; no page is under target).

**Voice gate:** `SHIP — fatal=0 tier1=0 p1=0, score 1.6/100 (**45,938 words**, 81
pages)` (was 29,598 words at ck73 — the extra pages are real content, not filler).

**What changed ck74 → ck89:**
- **TOP_TOWNS slice bug fixed** (`5911c3f`): service×town matrix was built only
  for `TOP_TOWNS[:6]` → 24 pages. Now all 12 MA towns → **48 pages**.
- **Fire-pit guide added** (`e849bb2`): `/learn/fire-pit-basics/`, 960 words.
  Closed the one service with zero guide coverage.
- **Service ↔ guide linking both ways** (`e849bb2`): `GUIDE_SERVICE` reverse map —
  each guide links up to its money page, each service page links down to its guides.
- **Keyword gap closed** (`e978d12`): home + Mansfield now carry
  "patio installer … Mansfield, MA" phrasing; `/learn/paver-cost/` retitled for
  "stone patio costs in Massachusetts". Verified present in live HTML.

**SERP baseline (re-checked this session):**
- **Google — unmeasurable from this IP.** `curl` returns a JS-redirect shell /
  "unusual traffic" wall. Do not treat a curl result as a ranking signal.
- **Bing — still not indexed.** `site:brycespatios.work` returns ~1 irrelevant
  result despite repeated IndexNow `HTTP 200` (81 urls). Recorded so we stop
  re-pinging in hope: the lever is Search Console + citations, not more pings.
- **Google Maps:** still **no listing** for Bryce. GBP remains the #1 gap.

**The honest read:** page quality, depth, schema, linking and voice are all at
target. We are now blocked on things that need Bryce's identity or hands: create
the GBP, claim Search Console, then citations and reviews. Nothing on the site
side is the bottleneck.
