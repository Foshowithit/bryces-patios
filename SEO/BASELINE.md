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

---

## ck94 → ck96 (2026-10-08) — icons, schema cleanup, off-site plan

**What changed:**

- **Home service-link gap fixed** (ck94, `05e3229`): the home page's `#work`
  project cards and the `.work__services` row now link to the 4 money pages
  (was: 0 real service links from home → now 4). Cache-buster bumped to
  `b7d3f918`.
- **`favicon.ico` was 404 on every page** (found ck96, verified live-404 before
  fix). The head declared only an inline data-URI SVG, so browsers that request
  `/favicon.ico` by convention got nothing. Fixed in `53efffa`: shipped a real
  `favicon.ico` (16/32/48/64), `favicon-32.png`, `apple-touch-icon.png` (180),
  `icon-192.png`, `icon-512.png`, generated from the site's own 4-paver mark,
  plus a real `site.webmanifest` (name/short_name/icons/theme) and a proper
  light/dark `theme-color` media pair on all 81 pages. The `apple-touch-icon`
  also stopped misusing the 1200×630 `og-cover.jpg` (931 KB, wrong aspect).
- **`chore(img)` `f190b2a`**: dropped an accidentally-committed
  `assets/img/icon-source.png` from shipped assets.
- **JSON-LD cleanup** (ck96, `0eb5ab2`): home `LandscapingBusiness` `image[]`
  had `project-dining.jpg` listed twice (6 → 5 declarations, 5 unique); `logo`
  moved from the 1200×630 `og-cover.jpg` to the square `icon-512.png` 512×512.
  JSON re-validated with `json.loads` after the edit.

**Verified after each rebuild:** `emit.py` → **81 pages / 81 sitemap urls /
14 feed entries**; `grep -rl 'assets/img/favicon.ico' --include=index.html .` →
**81**; mansfield + home heads show manifest link + light/dark theme-color pair.
Live checks after push: home 200 · `/favicon.ico` 200 · `/favicon-32.png` 200 ·
`/apple-touch-icon.png` 200 · `/site.webmanifest` 200 · sitemap 81 `<loc>`.

**Voice gate:** re-ran on the full visible-copy extract — **SHIP, fatal=0
tier1=0 p1=0, 1.6/100**. Depth unchanged and at target: guides min 732 / avg
779 (n=13) · towns min 617 / avg 642 (n=12) · service×town min 415 / avg 444
(n=48).

**Search visibility (re-confirmed 2026-10-08):**

- **Bing: still 0 pages indexed.** `site:brycespatios.work` returns the
  date-range filter widget and zero result URLs — the signature of "Bing has
  nothing for this site." Three rounds of IndexNow `HTTP 200` (81 urls each) did
  not change this. Honest conclusion: **the lever is Search Console + Bing
  Webmaster Tools + citations, not more pings.**
- **Google: unmeasurable from this host** (JS shell / "unusual traffic" wall).
  Do not read a curl result as a ranking signal.
- **Google Maps: still no listing.** GBP remains the #1 gap.

**Bookkeeping (so these are not re-chased):** the ck94 `site.webmanifest` 404 was
a probe of a *conventional* path — nothing referenced it. It is now a real file.
`manifest.json` and `browserconfig.xml` 404s remain **unreferenced — ignore.**

**Plan of record updated:** `SEO/PLAN.md` now opens with a **priority table** that
names **off-site visibility + indexation as the primary remaining workstream**
(P1 GBP → P2 GSC → P3 Bing WMT → P4 citations → P5 reviews → P6 social) and
demotes on-site maintenance to "at target." New one-page human checklist:
`SEO/OFFSITE-CHECKLIST.md`.

**Honest read after ck96:** the site side is done — pages, depth, schema, icons,
linking, voice and crawl plumbing are all at target and verified. **Visibility is
blocked on human actions that need Bryce's identity:** create the GBP, claim
Search Console, set up Bing Webmaster Tools, then citations and reviews. Nothing
we can do on the site will move a 0-index, no-profile business into Maps.

---

## ck97 → ck98 (2026-10-08) — llms.txt, root favicon, AI-extractibility

Closed the remaining OURS gaps on the AI-answer / crawl-plumbing surface. No
visible copy changed.

**Shipped**
- `llms.txt` — AI-assistant guidance file live at `https://brycespatios.work/llms.txt`,
  pointed to from `robots.txt` with an `LLMs-Txt:` line.
- `<link rel="alternate" type="text/plain" title="llms.txt" href=".../llms.txt">`
  added to every page head (emitted in `site.py render_shell` + the
  hand-maintained `index.html`), so 81/81 pages advertise it.
- Real root `/favicon.ico` shipped (byte-identical to `assets/img/favicon.ico`);
  the bare `/favicon.ico` path now returns 200 instead of 404.

**Verified live (200):** `/` · `/llms.txt` · `/favicon.ico` · `/robots.txt` ·
`/site.webmanifest` · `/assets/img/favicon.ico` · `/assets/img/icon-512.png`.

**Unchanged / at target**
- Sitemap **81 `<loc>`**; `<image:image>` on **81/81** URLs.
- Alt text **100/100 `<img>`**; every one of the 81 pages has ≥1 image.
- JSON-LD parse: **0 failures** on all 81 pages.
- Content depth unchanged: guides min 732 / avg 779 (n=13) · towns min 617 /
  avg 642 (n=12) · service×town min 415 / avg 444 (n=48).
- Voice gate full-site re-run: **SHIP — fatal=0 tier1=0 p1=0, score 1.6/100
  (45,950 words, 81 files)**.

**Indexation re-probe (ck98)**
- IndexNow ping: HTTP 200, 81 urls + 2 new files.
- Bing `site:brycespatios.work`: **still 0 indexed** — the SERP returns the
  empty-result widget. Repeated 200 pings are not producing indexation; the real
  lever is Bing Webmaster Tools + citations, not more pings.
- Google: unmeasurable from this host (WAF). GBP still the #1 gap.

**Read after ck98:** every OURS row in `SEO/PLAN.md` is now DONE. The honest
remaining surface is (a) human identity actions — GBP, GSC, Bing WMT, Bing
Places, Apple Business Connect, 30+ citations, reviews — and (b) more **real
photos** from Bryce (40 ship, only 6 real-labeled), plus a real video for the
showreel (Dell render lane only).

---

## ck99/ck100 — SERP truncation + duplicate-title fixes (pushed f010697)

Found and fixed in the generator (`work/gen/`), then regenerated all 81 pages.

1. **`learn/fire-pit-basics` meta description was 165 chars** (SERP truncates
   ~155-160). Trimmed to **157**.
2. **Duplicate-title bug — 12 groups / 24 pages.** Every town hub
   (`areas/<town>/`) carried the exact same `<title>` as its child
   (`areas/<town>/patios/`): `Stone Patios in {town}, MA | Bryce's Patios`.
   Town hub retitled to `Stone Patios in {town}, MA | Patio Builder`. **DUPGROUPS 0.**
3. **Service x town titles ran 61-65 chars** (worst case North Attleboro
   walkways = 65). Suffix `| Local Patio Builder` -> `| Free Estimates`; worst
   case now 56 chars, all under 60.

**Post-fix audit (all 81 pages):** `PAGES 81 · JSONLD_FAIL 0 · LONG [] · DUPGROUPS 0`
— no title >60, no meta >160, no duplicate title anywhere.

**Live proof after push (build `f010697` — completed success):**
- `/areas/north-attleboro/walkways/` `<title>` -> `... | Free Estimates` (was `| Local Patio Builder`)
- `/areas/north-attleboro/` `<title>` -> `... | Patio Builder` (now distinct from its patios child)
- `/learn/fire-pit-basics/` meta length -> **157**

**Re-verified unchanged after push**
- `/` **200** · sitemap **81 `<loc>`** · `/llms.txt` 200 · `/favicon.ico` 200 ·
  `/robots.txt` 200 · `/site.webmanifest` 200 · `/assets/img/favicon.ico` 200 ·
  `/assets/img/icon-512.png` 200.
- Images re-audited: **102 `<img>`, 0 missing alt, 100 lazy, 102 with width+height**
  (CLS-safe).
- Content depth unchanged: guides min 732/avg 779 (13) · towns min 617/avg 642 (12)
  · service×town min 415/avg 444 (48).
- Voice gate full-site re-run: **SHIP — fatal=0 tier1=0 p1=0, score 1.6/100
  (45,950 words, 81 files)**.
- IndexNow re-ping after the content change: **HTTP 200, 81 urls**.

## ck106–ck111 — QA, showreel, form-to-SMS, and honest re-verification (2026-10-08)

Checkpoints ck101–ck105 were never logged. This entry back-fills the range so the
log has no hole, and records what was actually proven versus what was assumed.

### ck101–ck104 — the four "bugs" were all false positives
An early handoff listed four "glitches" on the site. Every one of them was an
artefact of screenshots taken mid-reveal-animation: the QA script captured a
frame while `opacity:0` reveal transitions were still in flight, so sections
looked missing. Re-shot with settled frames. **All four are false positives.**
Nothing was fixed because nothing was broken.

### ck105 — `shot2.mjs` is the reliable screenshot instrument
`/tmp/shot.mjs` produced the false positives. `/tmp/shot2.mjs` waits for layout
to settle, then writes **17 full-page PNGs plus a geometry JSON**. Use it, not
`shot.mjs`. Recipe (from `SEO/README.md` / this log's recipes):
```
mkdir -p /tmp/bryceqaN && cd /tmp && timeout 220 node /tmp/shot2.mjs "https://brycespatios.work/" /tmp/bryceqaN 1280 800
```
Mobile width is `390 844`.

### ck106 — full-page geometry verified, no gaps
`SHOTS 17 HEIGHT 13009` at 1280×800. Sections are contiguous and in order:
`#faq top=10714 h=756` → `#estimate top=11470 h=1119` → `footer top=12589 h=420`.
No blank band, no overlap, no double-rendered section. The "glitchy" complaint
does not reproduce against the current live build.

### ck107 — showreel verified playing
`1920×1080`, `32.284 s`, `HTTP 206` range streaming, 8 photos, MP4
`14,921,367 B`, poster `assets/img/project-firepit.jpg`, `preload='none'`,
launch control `#film-launch`, `VideoObject` schema with an 8-part `hasPart`,
and a `video:` entry in `sitemap.xml`. Aspect crops shipped to
`~/Movies/bryce-patios-reel/`: `showreel-1080p.mp4` (16:9),
`showreel-reel-9x16.mp4` (9:16), `showreel-square-1x1.mp4` (1:1).

### ck108 — the estimate form → text message works end to end
Proven with `/tmp/qa_wizard.mjs`. Three steps (1 What do you need → 2 Your yard →
3 Your details) → success panel → `#send-sms`. The final href is
`sms:+15082126433?body=…` (body ≈300 chars, verified). Gotcha recorded:
the chip/radio `<input>`s are **visually hidden**, so Playwright `page.check()`
**times out** — click the **label** instead
(`#estimate label.chip:has(input[value="X"])`). `FORM_ENDPOINT=''`, so the user
taps "Text Bryce" and the SMS is pre-filled. **User-approved; leave as-is.**
Screenshot kept at `/tmp/bryceqa6/form-success.png`.

### ck109 — image truth, stated plainly
**Every photo on the site is an AI-generated rendering.** Zero real job photos
ship. The disclosure is in the footer of all **81** pages (`AI-generated` appears
on 81/81) and in the work-section note. 33 JPGs + 4 PNG icons + 2 SVG diagrams
ship in `assets/img/`. More real shots from Bryce = the biggest single trust and
image-search upgrade, **and** the removal condition for the disclosure (removed
page by page as real photos land, never all at once). Ask sheet:
`work/BRYCE-SHOT-LIST.md` (untracked scratch by design — `work/*` is gitignored).

### ck110 — three doc writes
`SEO/GBP.md` §4, `SEO/CITATIONS.md` §0, and `SEO/OFFSITE-CHECKLIST.md` §2 were
all annotated with the **20-vs-22 town resolution**: Google's service-area field
caps at 20, so `SEO/GBP.md` §4 lists the top-20 subset (excludes Smithfield and
North Smithfield, RI); the site and the free-text directories describe the full
**22-town** area. This is a documented difference, **not a bug — do not "fix" it.**

### ck111 — live re-verification + 5-viewport visual QA (this checkpoint)
Own eyes, not prior claims:
- `curl -sI https://brycespatios.work/` → **HTTP/2 200**, GitHub Pages/Fastly,
  `cache-control: max-age=600`.
- `sitemap.xml` → **81 `<url>`**.
- `shot2.mjs` → **`SHOTS 17 HEIGHT 13009`**, sections contiguous (`#faq`
  `top=10714`, `#estimate top=11470`, `footer top=12589`).
- **5 viewports inspected** (00-y0, 01-y800, 04-y3200, 08-y6400, 15-y12000): hero
  is a real-looking flagstone patio with a dark nav and a "Get a free estimate"
  CTA; "Recent work" is 6 well-lit patio/walkway tiles; "Common questions" is a
  clean 6-item accordion; "Free estimate" is the 3-step wizard; footer renders
  correctly with NAP + the `(508) 212-6433` call button. **No visible glitches.**
- **Conclusion recorded honestly:** the site is in good shape at 1280×800. The
  "still glitchy / errors / bugs" complaint is stale or refers to an older build.

### Also recorded: dead instruments (do not retest)
`r.jina.ai` is now **Cloudflare-challenged for this host** — ck110 hit a
"Just a moment..." interstitial for all 7 targets tried. Direct `curl` to those
same hosts was also challenged. Already dead and recorded: Bing HTML scrape
(geo-poisoned), DuckDuckGo, Startpage, Mojeek. Google `curl` is WAF'd. **The only
real SERP / browser read is `ego-browser`** (real Chromium), and Google probing
stays ≤3 queries/session, 10–20 s apart, ≤1×/hour.

---

## Session 18 — ck112–ck113 (2026-10-09)

### ck112 — the showreel audio defect, fixed and shipped *silent*
**The bug the user actually heard:** the shipped showreel carried a TTS voice track
that repeated *"You understand? Good, let's go."* roughly **8 times** over a
32 s reel. It sounded broken and wrong for a patio company. It is **gone**.

**What was wrong, exactly:** `assets/video/showreel-1080p.mp4` and a sibling
`assets/audio/showreel.mp3` both shipped; `main.js` ran a narration path that
unmuted/played that track behind the muted film. The strip commit (`6e34d59`)
deleted the audio file, re-encoded the mp4 video-only, and cut the narration code.

**Measured, before → after:**
- mp4 bytes **`14,921,367` → `14,238,968`** (−682,399 B).
- `assets/audio/` **deleted** — the directory does not exist in the tree.
- `ffprobe` on the live file → **`0,h264,video,1920,1080,32.233333`** — **exactly
  one stream, no audio**. There is no voice-on-the-reel failure mode left to hit.
- `main.js` narration block −42/+11 lines; `grep -c 'muted\|volume\|narration'` in
  the live bundle = **1**, and that one hit is the `aria-label` string
  *"…silent: eight real jobs…"*, not a control. `node --check assets/js/main.js` = **OK**.
- The dead `#film__mute` CSS block was removed in the layout commit.

**Root cause of the delay (recorded so it never repeats):** the fix was
**committed but never pushed** in the prior session, so `brycespatios.work` was
still serving the old **14,921,367 B** file with the bad voice. The user was
correct that the reel was still broken. It is now pushed (`6e34d59` … `c456d4d`)
and **live-verified**: `GET /assets/video/showreel-1080p.mp4` → **HTTP 200,
`content-length: 14238968`, `content-type: video/mp4`**.

**Proof of the transcript, for the record:** the repeated line was
*"You understand? Good, let's go."* — an artifact of the TTS generation, not a
script we wrote. Removing the track removes it completely. **Lesson: a fix is not
shipped until it is pushed AND read back from the live URL.**

### ck113 — layout pass + live re-verification (this checkpoint)
Own eyes and byte-reads, not prior claims.

**Layout commit `9d04333`** (41 lines, 18 ins / 23 del, 7 hunks) — confirmed numbers:
1. `.promise__grid` `align-items:center`→`start` + `.promise__body` `padding-top`
   `.5rem`→`.35rem` — killed a **58px** lead/body offset (all three columns now `top:1012`).
2. `.form-progress` margin-bottom `clamp(2rem,4vw,2.75rem)`→`clamp(1.25rem,2.5vw,1.75rem)` — gap **44 → 28**.
3. `.step-panel__legend` `2rem`→`1.5rem` (row `t12867 h94`) · `.step-panel__num`
   `.75rem`→`.5rem` · `.step-panel__hint` gained `margin-top:.35rem`.
4. `.chips` gained `margin-bottom:1.75rem` — chips→size gap **0 → 28**.
5. `.step-nav` margin-top `2.25rem`→`1.75rem`, padding-top `1.75rem`→`1.5rem`
   (row `t13225 h78 b13303`).
6. `.film__mute` CSS block removed (dead after the ck112 JS cleanup).
7. `.learn__grid` `align-items:start`→`stretch` + `grid-auto-rows:1fr`;
   `.guide__list` / `.guide__checklist` → `flex column; gap .55rem; margin-top:auto;
   margin-bottom:0; padding-top:1rem; border-top:1px solid var(--line)`.

**Guide-grid fix, verified:** the **15rem checklist cap is REMOVED** — `hiddenPx 0`
at every breakpoint (`overflows=false`). At 1440 the guide grid is `rows=2`,
`cols=[3,3]`, **`h=[763,763]`** — both rows now equal height, checklist cards
pinned to the bottom by `margin-top:auto`. Row 1 all `t8529 h763 b9292`; row 2 all
`t9328 h763 b10091`. `.guide__list` bottom `10058`. At 1024/820 → `[2,2,2]`
`h701/h723`; at 760/390 → 6×`[1]`. `.guide__checklist` renders only on
`/learn/the-quote/` at its natural height (372).

**One intended change:** `#learn` section height **`2433 → 2624`** (+191px). This
is the `grid-auto-rows:1fr` stretch doing its job (equal card heights), not a
regression.

**Two instrument artifacts disproven this session (do not re-litigate):**
- **Playwright blank PNGs** = instrument artifact, not a site bug.
- **Vision "blank image" reports** = artifacts; DOM audit found **`BROKEN: []`,
  `ZERO_SIZE: []`, 16/16 `complete:true`** with natural widths. Images are fine.

**Also fixed:** a `404.html` cache-buster **straggler** (it still carried token
`d18aa156` while the other 81 pages had moved on). Token reconciled to
**`8f6a48a0`** everywhere — `index.html` + `404.html` hand-edited, the other 81
emitted by `work/gen/emit.py`. Single source of truth: `work/gen/site.py:17`
`V = "8f6a48a0"`. **Note: running `site.py` directly is a no-op — `emit.py` is the
generator.**

**Live re-verification (curl, this checkpoint):**
| URL | Result |
|---|---|
| `/` | 200, 62,862 B |
| `/learn/` | 200, 26,808 B |
| `/services/` | 200, 19,783 B |
| `/areas/` | 200, 19,586 B |
| `/areas/mansfield/patios/` | 200, 17,569 B |
| `/learn/the-quote/` | 200, 19,532 B |
| `/404.html` | 200, 6,390 B |
| `/sitemap.xml` | 200, **81 `<loc>`** |
| `/llms.txt` | 200, 2,049 B |
| `/feed.xml` | 200, 6,057 B |
| `/robots.txt` | 200, 164 B |
| `/assets/video/showreel-1080p.mp4` | 200, **14,238,968 B**, `video/mp4` |

`last-modified: Fri, 09 Oct 2026 04:49:49 GMT` — confirms `c456d4d` is what GitHub
Pages is serving.

### Recorded: `/about/` and `/contact/` 404s are NOT a bug — do not "fix" them
There are **no `/about/` or `/contact/` routes, and none are linked.** They are
**on-page anchors** on the homepage: `#about` (`index.html:636`) and `#estimate`
(`index.html:923`). Every "About" link in the footer points at `href="#about"`.
`grep -rn 'href="about\|href="contact\|href="/about\|href="/contact' --include='*.html' .`
→ **exit 1, zero matches** (quote the glob; unquoted `*.html` makes zsh fail with
*no matches found*). **Do not invent `/about/` or `/contact/` pages.**


---

## ck114 — 2026-10-09 — LIVE QA via real browser + BOTH-engine index truth

**Tool:** ego-browser (real Chromium) against `https://brycespatios.work/`, 7 viewport
shots `y=0…13,000`, plus the film modal. Screenshots: `/Users/adam26/bryce-live-qa/`.

### Live page health (measured, not assumed)
- title `Stone Patio Installation in Mansfield, MA | Bryce's Patios`
- imgs **17**, **broken 0** · `tel:` **5** · `sms:` **0** (the one text CTA is
  `#send-sms` → `sms:` deep link on tap, by design) · exactly **1 `<h1>`**
- `overflowX: false` · viewport 1602 · `docH` 13,908
- section tops all present: work 1753 · process 2973 · craft 4972 · about 6341 ·
  learn 7255 · area 10227 · faq 11578 · estimate 12358
- **Film modal works:** `#film-launch` → `<video>` `showreel-1080p.mp4`, `muted:true`,
  `paused:false`, `readyState:4`, `duration:32.233`, `1920×1080`, `currentTime` advancing.
  The AI-rendering disclosure line renders under the film as intended.

### ⚠️ THE REAL GAP — both engines index ZERO pages (re-measured this session)
- **Google** `site:brycespatios.work` → *"Your search … did not match any documents."*
  (`resBlocks 0`). Same SERP shows Google's own promo:
  *"Do you own brycespatios.work? Get indexing and ranking data from Google."*
  → **proves Search Console is NOT verified.** No GSC = Google has no submission path.
- **Bing** `site:brycespatios.work` → *"There are no results"*; the 10 `b_algo`
  blocks are irrelevant fallbacks (`abrhs.abschools.org` etc.). Bing = **0 indexed**.
- Conclusion: IndexNow `HTTP 200` does **not** index a brand-new domain (confirmed
  3rd time). The only fast path to Google is **GSC (DNS TXT via Porkbun)**; Bing's
  is **Bing WMT**. Both are BLOKED on Bryce's account/identity.

### IndexNow re-ping (81 live URLs, this session)
Re-submitted all 81 `<loc>` URLs to `api.indexnow.org` + `www.bing.com/indexnow`
with `keyLocation https://brycespatios.work/b8be78077b664cf338d750ff4799d248.txt`
(keyfile serves 200). Kept as hygiene; **do not expect indexation from it.**

### Honest status
The site is **live, clean, and fast** (17 imgs, 0 broken, 1 h1, no overflow, film
plays). It is **invisible in search** and that is **not fixable by us** — it needs:
(1) Bryce's Gmail for GBP + GSC (DNS TXT), (2) Bing WMT (imports from GSC), then
(3) citations. On-site work is at target; discovery is 100% identity-blocked.

---

## ck115 — 2026-10-09 · srcset true-width fix + 404 icon fix + schema exoneration (pushed)

**Three defects from the ck114 audit, closed.** Commits `f8402d7` (fix) + `0a8a6ab`
(regen), pushed to `main`; GitHub Pages live-verified.

### DEFECT 1 — srcset width descriptors were false (REAL mobile-speed defect) · FIXED
- Root cause: `work/gen/emit.py:54` hardcoded `.../{name}.jpg 2000w`, but `IMG_DIMS`
  (`emit.py:42-47`) holds the **true** widths (1200/1400/1600). Description was wrong on
  **all 80 emitted pages**, so a 2x-DPR phone selected the full 458–616 KB JPG instead of
  the 90–230 KB `-900` variant — real payload waste on the slowest devices.
- Fix: descriptor now uses `{w}` from `IMG_DIMS` (single source of truth → cannot drift again).
  `index.html` is hand-maintained, so its two figures were corrected by hand
  (`stone-arch`, `stairs-landing` `1600w → 1200w`; both are 1200 px images).
- **Verified:** `sips pixelWidth` comparison across **all 82 HTML files** → **216 srcset
  descriptors checked, 0 mismatches**. `grep -rl 2000w --include='*.html'` → **0 files**.
  Live: `https://brycespatios.work/` DOM `srcset2000 = 0`.

### DEFECT 2 — 404.html referenced a nonexistent favicon · FIXED
- `404.html:10` linked `/assets/img/favicon.svg` (file does not exist → 404) and was the
  only page on the site not carrying the icon set.
- Fix: replaced that line with the **exact five icon declarations every other page uses**
  (`favicon.ico`, `favicon-32.png`, inline `data:image/svg+xml`, `apple-touch-icon.png`,
  `/site.webmanifest`). No new file created.
- **Verified:** `grep -rn 'favicon\.svg'` → **0** repo-wide; live
  `https://brycespatios.work/404.html` → 200, `favicon.svg` refs **0**, icon set present.

### DEFECT 3 — "82 pages missing LocalBusiness schema" · RESOLVED AS FALSE POSITIVE
- The audit flag was a **parser artifact**: the regex looked for literal `LocalBusiness`,
  but the pages correctly emit `LandscapingBusiness` (a valid `LocalBusiness` subtype),
  and the breadcrumb is nested rather than flat.
- Dumped JSON-LD from `areas/mansfield/` + `services/patios/`: **4 blocks each** —
  `WebSite` / `LandscapingBusiness`(+`PostalAddress`,`GeoCoordinates`,
  `OpeningHoursSpecification`,`City`) / `WebPage`(+`BreadcrumbList`,`ListItem`) /
  `FAQPage`(+`Question`,`Answer`), all `@id`-linked. **Schema is complete and correct.**
  Matches ck98 "JSON-LD 0 failures". **Nothing to fix.** (Honest correction to the audit's
  own alarm — recorded rather than silently dropped.)

### Live QA after deploy (7 viewports + interior)
- Home: `title` ✓ · **1 h1** · imgs 17 · **broken 0** · `tel:` 5 · `overflowX false` ·
  `docH` 13,908 · JSON-LD 3 · **srcset2000 0**.
- Interior `services/patios/`: 1 h1 · broken 0 · JSON-LD **4** · `tel:` 6 · no overflow.
- **Film modal works live:** `#film-launch` → `<video>` `showreel-1080p.mp4`,
  `muted:true`, `paused:false`, `readyState:4`, `duration 32.233`, `1920×1080`, playhead
  advancing. The AI-rendering disclosure still renders under the film.
- Shots: `/Users/adam26/bryce-live-qa2/` (`00-y0`…`06-y13000`, `90-showreel`,
  `95/96-services-patios`, `97-mansfield`).

### Gate + emission invariants (re-run this turn)
- **Voice gate:** `SHIP — fatal=0 tier1=0 p1=0 score=1.5/100 (46,320 words)` across all 82
  pages (counters match ck114 baseline; no copy changed this turn — regression check only).
- `work/gen/emit.py` → `wrote 81 pages, sitemap has 81 urls, feed has 14 entries`.
- **IndexNow re-ping:** 81 URLs → `HTTP 200`. (Kept as hygiene. Does not index a new domain;
  still the honest finding.)
- Tree clean: `git status --short` → 0 files. `sitemap.xml` serves **81** `<loc>`.

### Unchanged truth
On-site is at target and maintenance-only. **Both engines still index ZERO pages** —
the only fast paths are **GSC (DNS TXT via Porkbun)** and **Bing WMT**, both blocked on
Bryce's identity. Nothing in this ck changes that.

## ck116 — 2026-10-09 · showreel "voice" root-caused: a stale cache, not a bad build

**The report:** the owner heard a synthetic TTS voice in the showreel, saying
"good, let's go" repeatedly, and asked for it fixed.

**What the deployed build actually was (verified before touching anything):**
silent and correct. `assets/js/main.js` had **0** references to `muteBtn` or an
`Audio()` object, `video.muted = true`, and an aria-label reading
*"silent: eight real jobs"*. The shipped mp4 had **1 video stream, 0 audio
streams**. The narrated TTS cut was stripped in `6e34d59`.

**So why did the owner hear a voice? Two stale-cache holes, both now closed.**

1. **The asset cache-buster was never bumped after the strip.** `V` in
   `work/gen/site.py:17` stayed at `8f6a48a0`, so `main.js?v=8f6a48a0` kept
   resolving to the older script that still built the audio element. GitHub Pages
   serves `max-age=600` with an etag that never changed, so a reload inside the
   window — and any CDN edge holding the old object — handed back the narrated
   script. The build was right; the URL lied.
2. **The mp4 had no cache-buster and shared its filename with the narrated Dell
   master.** `main.js` fetched `assets/video/showreel-1080p.mp4` with no query
   string, and the Dell's `~/bryce-reel/out/showreel-1080p.mp4` (14,921,367 B,
   with the aac voice track) carried the same name as the shipped silent file
   (14,238,968 B). A cached mp4 could therefore serve the voice even after the
   script was fixed.

**The fix (commit `837df6b`):**
- `V` bumped `8f6a48a0` → `c41d7b93` in `work/gen/site.py:17`; all 81 emitted
  pages regenerated; `index.html` and `404.html` hand-patched to match. **82/82
  pages** now carry `v=c41d7b93` on both `style.css` and `main.js` (164 refs).
- The reel renamed to **`showreel-1080p-silent.mp4`** so the narrated file can
  never resolve to that URL again. Updated `main.js` `VIDEO_SRC`, `index.html`
  JSON-LD `contentUrl`, the sitemap `<video:content_loc>`, and `SEO/VIDEO.md`.
- Verified: **0** refs to the old video name anywhere in the repo;
  `node --check assets/js/main.js` passes.

**Live verification (real browser, not curl):** a fresh page load requests
`main.js?v=c41d7b93`, `style.css?v=c41d7b93`, and
`assets/video/showreel-1080p-silent.mp4` — nothing else. The served `main.js`
is byte-identical to local (md5 `ea9fb9555f7a048a66e3ac4662c6d5f8`). The old
video URL returns **404**; the new one returns **200**, `video/mp4`.

**Lesson recorded:** docs mention the cache-buster must be bumped on every asset
change; the miss was letting the strip commit and the bump commit come from
different windows so the *URL* never moved. Any change to `main.js` or the reel
now requires a new `V` **and** a new reel filename in the same commit.

---

## ck117 — 2026-10-09 — form step-2 to step-3 "blocker" was a harness bug; latent panel-display bug found and fixed

**Reported symptom.** The estimate form appeared to stall: step 2 accepted
input, but the "next" click did nothing and step 3 never showed. It read as a
site bug and was carried as one across a full session.

**Root cause of the report: the test harness, not the site.** The probe did
`document.querySelector('button[data-next]')`. That returns the **first**
match in document order, which is **step 1's** button — hidden at the time.
Clicking a hidden button does nothing, so the probe concluded "step 2 to 3 is
broken." Scoping the selector to the visible panel
(`.step-panel.is-active button[data-next]`) advanced step 2 to 3 cleanly
(`activeAfter: "3"`). The site was fine. The instrument lied.

**A real latent bug found on the way.** `main.js` submit path
(`main.js:317`) sets an **inline** `display = 'none'` on every `.step-panel`.
`goTo()` only toggled the `.is-active` **class**. Inline styles beat classes, so
if a panel was ever re-shown after a submit (back button, retry, validation
bounce), it would stay blank with `.is-active` set and nothing on screen. Not
triggered by the normal happy path, which is why it survived. `goTo()` now
clears inline display before toggling the class.

**Full end-to-end flow, measured in a real browser** (step 1 chip click sets
`input.checked`; step 1→2; step 2 town + timing chip sets the radio; step 2→3
with the correct selector; submit reveals `#form-success`; `#send-sms` href is
`sms:+15082126433?body=...` containing every field; no em-dash and no curly
apostrophe in the body; `#send-mail` href builds a matching `mailto:`; the
60 ms SMS auto-open does fire). All assertions closed.

**Cache work.** `V` moved to a **fixed token `f4a9c1d2`** across all 82 pages
(164 refs) and `work/gen/site.py:17`, and the reel was renamed
`showreel-1080p-silent.mp4` → `showreel-1080p-silent-f4a9c1d2.mp4`, with
`main.js` `VIDEO_SRC`, the home JSON-LD `contentUrl`, and `404.html` updated to
match. Both changes ship in the **same commit** as the `main.js` edit, per the
ck116 rule.

**Trap recorded: do not derive `V` from a hash of `main.js`.** The first attempt
used `md5(main.js)` as `V`. But renaming the reel edits `main.js`, which changes
the md5, which changes `V`, which edits every page — a circle with no fixed
point. `V` is now an **independent, fixed token** and is not required to match
any file hash. `main.js` md5 is `42f161a68309790ac4dd83ff60f5c2eb`; `V` is
`f4a9c1d2`; they intentionally differ.

**Live verification (2026-10-09, `c3d23cb` pushed):** new reel
`/assets/video/showreel-1080p-silent-f4a9c1d2.mp4` returns **200**
(14,238,968 B); old `showreel-1080p-silent.mp4` returns **404**;
`main.js?v=f4a9c1d2` returns **200** and the served copy contains the `goTo`
fix; the home page serves `main.js?v=f4a9c1d2`. `node --check` passes;
0 stale `V`/reel refs in the tree.

**Rule restated (ck116, still binding):** any change to `main.js` or the reel
requires a new `V` **and** a new reel filename in the **same** commit. And a
green `curl` proves nothing about behaviour — the step-2-to-3 false alarm cost a
session. Exercise the interaction in a real browser, and scope DOM selectors to
the visible panel.

---

## ck118 — 2026-10-09 · indexation probe honesty, capy craft study, Bryce ask ready

**Bing scrape is dead for this purpose. Stop re-probing it.** `site:brycespatios.work`
through the headless browser now returns a **bot challenge wall** ("One last step /
Please solve the challenge below to continue"), with an `rdr=1` redirect and **0
`li.b_algo` result blocks**. Nothing readable comes back. This matches every earlier
probe: Bing shows the domain as **not indexed**. The lever is **Bing Webmaster Tools
plus Google Search Console**, and both need Bryce's own identity (Gmail / DNS TXT).
Do not spend another session scraping Bing. Record the number once from WMT/GSC
after access is granted.

**IndexNow re-pinged after the `c3d23cb` push:** HTTP **200**, **81 urls** submitted.
IndexNow is hygiene only. It does not index a brand-new domain by itself, and Google
does not participate in IndexNow at all.

**Google probe cadence is unchanged and still binding:** at most 3 queries per
session, 10–20 seconds apart, at most once per hour. The egress IP gets walled
otherwise.

**capy.ai craft study (visual quality reference).** Fetched and rendered
`capy.ai` (HTTP 200, 1,085,927 B) and compared it to the live Bryce home page.

- capy: `abcSocialMono`, white background, black text, h1 76px / line-height 76px
  (ratio 1.0) / letter-spacing -0.704px / weight 400, tiny ALL-CAPS section kickers.
- bryce: Inter + Fraunces, background `rgb(247,244,238)`, h1 99.2px / line-height
  97.2 / letter-spacing -3.472px / weight 400, h2 54.4px / line-height 57.7.
- The site CSS already carries the same craft: radii `--r-sm 3px / --r-md 5px /
  --r-lg 8px`, low-alpha shadows (`0 1px 2px rgba(20,23,26,.04)`), one accent
  `--moss #55613E`, uppercase eyebrows, a breakpoint ladder, `--ease`
  `cubic-bezier(.16,1,.3,1)`.

**Verdict: bryce already matches capy's craft level. No CSS churn warranted.**
capy's dark developer-tool aesthetic does not transfer to a warm outdoor contractor
anyway. Adopt the craft, not the look. The only candidate tweak (a slightly smaller
h1 on the 350–768 ladder) is low value and not worth touching passing CSS.

**`work/BRYCE-TEXT.md` created (56 lines, voice gate SHIP).** Text-message-ready
photo ask, two versions: V1 to send today (6 numbered phone shots in plain
language, no filenames), V2 the exact filenames for drop-in, plus a "do not send"
block. This is the actionable form of `work/BRYCE-SHOT-LIST.md`. Gate result:
fatal=0, tier1=0, p1=0, score 1.5/100. One earlier Tier-1 flag (`landscape`) was
fixed to `wide`. `work/*` is gitignored except `gen/`, `indexnow-ping.sh`,
`.indexnow-key` — never `git add -f` these.

**New artifact for the human sitting:** `work/BRYCE-TEXT.md` is ready to hand to
the user to send to Bryce. Off-site submission (GBP, GSC, citations) remains
blocked on Bryce's Gmail / Porkbun DNS access and is the true remaining gap.
