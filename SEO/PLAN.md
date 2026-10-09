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

## Priority order (re-planned 2026-10-08) — off-site visibility is the work now

The site itself is built and at target. **The remaining gap is not on the site.
It is that the site is not yet *discovered*.** A perfect page with no profile, no
citations and no index presence gets zero calls. So the primary workstream is
off-site visibility + indexation; the site work is now maintenance.

| # | Workstream | Who | Status | Why it matters |
|---|---|---|---|---|
| **P1** | **Google Business Profile live + verified** | **HUMAN** | **NONE** | The single biggest lever. A local service business with no GBP is invisible in Maps and the local pack, which is where most "patio installer near me" intent converts. Copy is ready in `SEO/GBP.md`. |
| **P2** | **Google Search Console claimed + sitemap submitted** | **HUMAN** | **unclaimed** | Only fast path to Google indexation, and the only source of real impressions/clicks/query data. Everything downstream depends on this. |
| **P3** | **Bing Webmaster Tools + IndexNow confirm** | ours + HUMAN | IndexNow 200s, **0 indexed** | Bing ignores ping-only for a brand-new domain. Webmaster Tools gives a crawl/index dashboard and the honest signal we are missing. |
| **P4** | **Citations / NAP submissions live** | HUMAN (we prep) | **0 live** | Directory + MapQuest/Yelp/BBB presence creates the entity signals that let a no-backlink site rank. Kit ready in `SEO/CITATIONS.md`. |
| **P5** | **Review engine live (needs GBP first)** | HUMAN | none | Reviews are the ranking + trust signal for local. Flow + templates ready in `SEO/REVIEWS.md`. `aggregateRating` only at ≥5 real reviews. |
| **P6** | **Off-site social signal** (FB posts, profiles) | HUMAN | kit ready | `social/SOCIAL-KIT.md` + 8 covers ready; posting needs Bryce's OK. |
| **P7** | **On-site maintenance** (depth, schema, icons, linking) | ours | **DONE / at target** | Already at target: 81 pages, voice gate SHIP, valid rich results. Only touch this to fix a real defect. |

**Rule from here:** every session should move a HUMAN item forward (make it a
one-click, copy-paste list) or fix a verified on-site defect. Do not re-polish
on-site copy that already passes the gate.

---

## Full discoverability stack (added 2026-10-08 ck97) — "think of everything"

The user's charge: *he is not visible in search, and we are probably not even
close to done.* Correct. Below is the **complete** list of surfaces where a
Mansfield-area homeowner, or a search/AI crawler, could encounter him. Rows
marked **OURS** are things we can do with no human identity; **HUMAN** needs
Bryce/Adam's login; **BLOCKED** needs an external gate (e.g. Google API access).

### A. Owned surfaces (we control fully)
| # | Surface | Who | Status | Note |
|---|---|---|---|---|
| A1 | Website (81 pages) | OURS | **DONE** | depth + schema + voice at target |
| A2 | `sitemap.xml` + `robots.txt` + `feed.xml` | OURS | **DONE** | 81 urls, Atom feed |
| A3 | `llms.txt` (AI-answer guidance file) | OURS | **DONE** (ck98) | live at `/llms.txt`, linked from `robots.txt` (`LLMs-Txt:`) and from a `<link rel=alternate>` in all 81 heads |
| A4 | Root `/favicon.ico` safety net | OURS | **DONE** (ck98) | real root `/favicon.ico` shipped (byte-identical to `assets/img/favicon.ico`); bare path now 200 |
| A5 | Structured data valid on every page | OURS | **DONE** | LocalBusiness+FAQ+Breadcrumb, `@id`-linked |
| A6 | Real-photo coverage per service×town | OURS/Bryce | **STRONGER (ck120)** | Every one of the 17 shipped photos is now a **real** Bryce job photo (was 6 real + AI). Zero AI renders ship. alt=100%, image sitemap 81/81. Open ask to Bryce: clean originals (source shots carry a "© Google" corner mark that the crops avoid) and a matched before/after pair. See `work/PHOTO-AUDIT.md`. |

### B. Search engine properties (indexation + measurement)
| # | Surface | Who | Status | Note |
|---|---|---|---|---|
| B1 | Google Search Console | HUMAN | **unclaimed** | API access needs a GCP OAuth project → **BLOCKED**, not ours |
| B2 | Bing Webmaster Tools | HUMAN | not set up | IndexNow 200s but **0 indexed**; WMT gives the crawl dashboard |
| B3 | Google Business Profile | HUMAN | **NONE** | #1 lever. Copy ready `SEO/GBP.md` |
| B4 | Bing Places for Business | HUMAN | none | free, mirrors GBP; Bing is where we already ping |
| B5 | Apple Business Connect | HUMAN | none | powers Apple Maps + Siri + Spotlight; free, underused |

### C. Directories / citations (entity signals)
| # | Surface | Who | Status |
|---|---|---|---|
| C1 | Yelp · C2 | BBB · C3 Nextdoor · C4 Houzz · C5 Angi · C6 Thumbtack · C7 MapQuest · C8 YellowPages · C9 Chamber (Tri-Town) · C10 Porch · C11 HomeAdvisor | HUMAN | 0 live; kit `SEO/CITATIONS.md` |
| C12 | Apple Maps (via B5) · C13 Bing Places (via B4) · C14 Facebook Page | HUMAN | FB page exists, unclaimed-edit |

### D. Social / off-site content
| # | Surface | Who | Status |
|---|---|---|---|
| D1 | Facebook page (NAP + posts) | HUMAN | kit `social/SOCIAL-KIT.md` |
| D2 | Instagram · D3 TikTok · D4 YouTube (mini showreel) | HUMAN | covers ready; **video = Dell render** |
| D5 | Nextdoor local recommendations | HUMAN | highest-intent local social |

### E. AI-answer surfaces (2026 reality)
| # | Surface | Who | Status |
|---|---|---|---|
| E1 | `llms.txt` + clean entity data | OURS | **DONE** (ck98) (= A3) |
| E2 | Consistent NAP so AI assistants cite the right facts | OURS+HUMAN | partial |
| E3 | FAQ structured data (already live) feeding AI answers | OURS | **DONE** |

**Rule:** the only rows we can move with no human are A3, A4, A6-prep, and
E1–E3. Everything else is a HUMAN checklist item. So the job is: (1) knock out
every OURS row, (2) keep the HUMAN rows as tight copy-paste lists so Bryce does
them in one sitting.

### F. Extra surfaces we had not written down (added 2026-10-08 ck112)

Everything the user could reasonably mean by *"think of everything"*. Same legend:
**OURS** = no human identity needed · **HUMAN** = needs Bryce's (or Adam's) login ·
**BLOCKED** = an external gate we cannot pass · **VERIFY** = reachability checked,
self-serve path unconfirmed, must be confirmed in a real browser before promising it.

| # | Surface | Who | Status | Note |
|---|---|---|---|---|
| F1 | **Yandex Business** (`yandex.com/sprav`) | HUMAN | **VERIFY** | Free listing. `biz.yandex.ru` did not resolve from this host (000). IndexNow already pings Yandex, so a verified Yandex listing is a real citation. Confirm the self-serve URL in a browser first. |
| F2 | **Foursquare** (`foursquare.com`) | HUMAN | reachable (200) | Free business listing. Foursquare place data feeds many navigation and map apps, so it is a high-leverage citation for a service-area trade. |
| F3 | **Reddit** (r/massachusetts, r/landscaping, r/HomeImprovement) | HUMAN | reachable | Highest-trust local answers, but **no link-dropping** — that is an instant ban. Only genuine, photo-backed answers from Bryce's real account. Treat as reputation, not a citation. |
| F4 | **Facebook Marketplace + local groups** (Mansfield / Bristol County buy-sell + homeowner groups) | HUMAN | reachable | Where actual local jobs get posted. Post finished-yard photos with a plain price-range line. Never spam a group. |
| F5 | **Patch.com Mansfield, MA** | HUMAN | **RESOLVED — real hub found** | VERIFIED in-browser 2026-10-09 via ego-browser: the town hub is **`https://patch.com/massachusetts/mansfield-ma`** (“Mansfield News, Breaking News in Mansfield, MA”). `mansfield.patch.com` redirects to Mansfield-**Storrs, CT** (wrong state) and `patch.com/massachusetts/mansfield` 404s. Patch has **no free contractor business directory** — use it as a community/news surface only (post a real build photo, no link-drop). Reclassified from citation to community channel. |
| F6 | **Tri-Town Chamber of Commerce** | HUMAN | reachable (200) | `tri-townchamber.org` is up. Paid membership, **but the member directory entry is a strong, geo-relevant citation** and it is the local institution. |
| F7 | **BuildZoom** | HUMAN | reachable (200) | Appeared in our own SERP baseline. Free contractor profile; claim it so the aggregator stops representing him worse than his own site does. |
| F8 | **D&B / `dnb.com`** | HUMAN | reachable (301→200) | Free basic business profile. Feeds a lot of B2B/entity data. |
| F9 | **Bark.com** | HUMAN | reachable (301) | Free pro signup exists; leads are paid. Sign up for the free profile only, same rule as Angi: **do not buy shared leads** for a one-man shop. |
| F10 | **Pinterest** | HUMAN | reachable | Design-led; patio/walkway/fire-pit imagery travels well here and links back. Needs owned photos ideally — AI imagery only with the same disclosure rule. |
| F11 | **YouTube** (the mini showreel) | HUMAN | **assets real + ready (ck120)** | The 16:9 / 9:16 / 1:1 cuts are re-rendered from **eight real job photos** and committed under `assets/video/` (`…-dba670bb.mp4`). Silent, 29 s, no audio stream. Upload = HUMAN. This is the one off-site surface where we already have finished, real assets. |
| F12 | **MA HIC (Home Improvement Contractor) registry** | HUMAN | **VERIFY — never assert** | Massachusetts publishes a public HIC registration lookup. **Only useful if Bryce actually holds an HIC registration.** We must not claim a licence he does not have. If he is registered, a matching registry entry is a top-tier trust citation; if he is not, this row is struck and nothing is written anywhere. |
| F13 | **Apple Business Connect** | HUMAN | **DONE** as B5 | Listed here only so nobody adds it twice. |
| F14 | **Map-data partners** (Waze · TomTom · Here WeGo `wego.here.com`) | — | **BLOCKED (no direct self-serve)** | There is no free contractor signup for these. Place data reaches them downstream via Apple/Bing/Yelp/Foursquare-style providers. So the *real* action is F2 + B4 + B5, not signing up for Waze directly. Marking them here stops a future session from burning hours hunting a signup that does not exist. |

---

## Where we are (verified 2026-10-08)

| Thing | State |
|---|---|
| Live site | `https://brycespatios.work` — 81 pages, GitHub Pages, `main` |
| Pages | 1 home · 1 learn hub · 13 guides · 1 services hub · 4 service · 1 areas hub · 12 town · 48 service×town = **81** |
| Sitemap | **81 URLs**, `<image:image>` on **81/81** URLs |
| Content depth | site avg **536** words (n=73) · guides min **732** avg 779 (n=13) · towns min **617** avg 642 (n=12) · service×town min **415** avg 444 (n=48) (all met) |
| Rich results | `LocalBusiness` (`LandscapingBusiness`) + `FAQPage` + `BreadcrumbList`, `@id`-linked |
| Google Business Profile | **NONE.** Biggest single reason he is invisible on Maps. |
| Indexed pages | ~1 (fresh URL, no GBP, no backlinks yet) |
| Reviews | 0 |
| Citations | 0 live (package ready in `SEO/CITATIONS.md`) |
| Monitoring | weekly crontab watcher live (`~/tmp/bryce-seo-watch/watch.py`, Mon 09:00) |
| Extractibility | `llms.txt` live + linked from `robots.txt` (`LLMs-Txt:`) and a `<link rel=alternate>` in all 81 heads |
| Icon/crawl plumbing | root `/favicon.ico` real (200), `assets/img/favicon.ico`, `icon-192/512`, `apple-touch-icon`, `site.webmanifest` all 200 |
| Image search | 100/100 `<img>` carry alt text; image sitemap 81/81 |
| Titles/meta | **0 over-length** (no title >60, no meta >160) and **0 duplicate titles** across all 81 pages (fixed 12 town-hub dup groups + 1 long meta, ck99) |
| Voice gate | last full-site run **SHIP, 0/0/0, 1.6/100 (45,950 words, 81 pages)** (ck98) |
| Discovery | `feed.xml` (Atom) + `rel=alternate` in every head (incl. home) · IndexNow key + ping script live · footer feed link |

---

## Workstreams + status

Legend: `TODO` · `WIP` · `DONE` · `HUMAN` (blocked on Bryce/user action)

### WS1 — Indexable multi-page site  `DONE`
Static HTML on GitHub Pages, no build step. Generator in `work/gen/` holds the
verified business data so every page's head, breadcrumb and JSON-LD are identical
in shape.
- [x] `/learn/` hub + 13 guide pages, split from the home `#learn` articles
- [x] 4 service pages · 12 MA town pages · **48** service×town pages (all 12 towns x 4 services, unique copy)
- [x] Every page: unique title/meta · keyword-strong H1 · self-canonical ·
      OG/Twitter · voice-gated copy · shared `style.css` + `main.js`

### WS2 — Sitemap + crawl hygiene  `DONE for us` (GSC submit = HUMAN)
- [x] `sitemap.xml` (81 URLs) + real `lastmod` from file mtime
- [x] `<image:image>` extensions for key photos
- [x] `robots.txt` intact · `apple-touch-icon` + `site.webmanifest`
- [x] `max-image-preview:large`
- [ ] **(HUMAN)** submit sitemap + request indexing per URL in Search Console

### WS3 — Internal linking  `DONE`
- [x] footer "Explore" column links home ↔ `/learn/` ↔ services ↔ towns
- [x] every page ≤3 clicks from home, descriptive anchors
- [x] **Related-guides block** on every guide page (same topic family, 3 links)
- [x] **Contextual in-prose links** from guides to the matching service page
- [x] Service×town → parent town + parent service cross-links verified
- [x] service pages link to their 6 service×town children + sibling services
      (`03cb1d3`, `<nav class="related">`, 6 `/areas/*/*/` links each)

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

### WS8 — Blog / education content  `DONE`
- [x] 13 noob-friendly patio-craft guides live, AI-disclosed, voice-gated
- [x] thicken the thin pages — all thresholds met (guides min 732, towns min 617,
      service×town min 415; site avg 536)
- [x] service<->guide linking both ways: every guide links to its matching money
      page, every service page links down to its guides (`GUIDE_SERVICE`)
- [x] fire-pit guide added (`/learn/fire-pit-basics/`) — closed the last service
      with zero guide coverage
- [ ] Optional next guides (write only if genuinely distinct, not spun):
      *"Retaining walls 101"* · *"Drainage around a foundation"* ·
      *"Prepping a yard for a patio"*

### WS9 — Monitoring  `DONE`
Quiet weekly watcher live via crontab (Mon 09:00). Notifies only on meaningful
change / completion / failure / required user action. Last run: 81 OK / 0 BAD.

### WS10 — Measurement  `WIP`
Dated before/after log in `SEO/BASELINE.md`: `site:` indexed count, brand SERP
position, local-pack presence, GBP views/calls/direction requests, review count,
per-page impressions/clicks once Search Console exists. Google-only, ≤3/session.

### WS11 — Discovery plumbing  `DONE` (except Google's non-participation, noted)
Getting the 81 URLs *noticed* now, not in six weeks.
- [x] `feed.xml` (Atom) + `<link rel="alternate">` in `head()` **and on home**
      + footer "Guides feed" link on every page
- [x] **IndexNow** key file at site root (`b8be78077b664cf338d750ff4799d248.txt`)
      + `work/indexnow-ping.sh` for all 81 URLs, `HTTP 200` after each push
      (Bing/Yandex/Seznam; **Google does not participate** — be honest about that,
      do not retry Google sitemap pings)
- [x] Sitemap submitted where it is accepted; IndexNow covers the rest
- [x] `SEO/` ops scripts documented in `SEO/README.md`

### WS12 — Off-site signal  `WIP` (drafts ready, posting = HUMAN)
- [ ] Facebook page → site link verified in NAP (do NOT edit the page without
      Bryce; note the ask)
- [x] `social/SOCIAL-KIT.md` — handle table (`@brycespatios` IG/TikTok/YT,
      `brycespatios` FB), profile bios, highlight covers (`social/highlight-covers/`)
- [ ] Post the 13 guides as FB posts (drafts ready; publish only after Bryce OK)
- [ ] One photo-driven FB post template per service for Bryce to reuse

---

## Content depth targets (words, visible text)

Current average across the 73 content pages ≈ **536 w**. No page is
below its target: guides min 732 / avg 779 (n=13) · towns min 617 / avg 642 (n=12) ·
service×town min 415 / avg 444 (n=48). The old thin pages are all fixed.

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

---

## Keyword → page map (added 2026-10-08, ck89)

Written so no future session re-guesses which query each page is built to win.
"phrase present" = the exact split words appear in visible copy on that page.

| Query | Intent | Landing page | Phrase present |
|---|---|---|---|
| `bryce patios mansfield` | brand | `/` (home) | yes |
| `patio installer mansfield ma` | commercial local | `/` + `/areas/mansfield/` | yes |
| `patio installer near me mansfield` | commercial local | `/areas/mansfield/` | yes (town pages) |
| `patio installation massachusetts` | commercial | `/services/patios/` | yes |
| `stone patio cost massachusetts` | research → money | `/learn/paver-cost/` | yes |
| `stone patio massachusetts` | commercial | `/services/patios/` | yes |
| `paver patio vs concrete` | research | `/learn/patio-vs-concrete/` | yes |
| `how long does a patio last frost` | research | `/learn/frost/` | yes |
| `walkway installer mansfield` | commercial local | `/services/walkways/` (+ 12 town pages) | yes |
| `retaining wall installer mansfield ma` | commercial local | `/services/retaining-walls/` | yes |
| `fire pit installer mansfield ma` | commercial local | `/services/fire-pits/` | yes |
| `hardscaping mansfield ma` | commercial local | home + `/areas/mansfield/` | partial (word on page) |

Rule: new pages only get added if they own a query that is not already owned.
Never two pages chasing the same phrase (cannibalisation).

## Town × service matrix — 48 / 48

All 12 MA towns (`Mansfield · Attleboro · North Attleboro · Norton · Foxborough ·
Seekonk · Rehoboth · Plainville · Franklin · Taunton · Easton · Sharon`) have a
page for each of the 4 services (`patios · walkways · retaining-walls ·
fire-pits`) = **48 service×town pages**, each with unique town-specific copy
(`LOCAL_NOTE` + `SVC_TOWN_DETAIL`), a parent-town link and a parent-service link.
Before ck88 only the 6 `TOP_TOWNS` existed (24 pages) — that was a `TOP_TOWNS`
slice bug, now fixed.

## Guide list — 13 (`/learn/` hub + 13 pages)

`choosing-contractor · drainage · driveway-aprons · fire-pit-basics · frost ·
materials · patio-base · patio-vs-concrete · paver-cost · the-quote ·
winter-ready · yard-grades · your-questions`

Every guide links up to its matching money page and every service page links down
to its guides (`GUIDE_SERVICE` reverse map). Gap fixed in ck88: `fire-pit-basics`
→ `/services/fire-pits/` (previously fire-pits had zero guide coverage).

## Off-site platform order (do in this order)

Phase 1 — identity (unblocks everything else):
1. **Google Business Profile** — #1 leverage, still NONE. Copy ready in `SEO/GBP.md`.
2. **Google Search Console** — the only fast path to get Google to index 81 URLs.
3. **Facebook page** — `@brycespatios`; verify site link in NAP. Never edit without Bryce's OK.

Phase 2 — anchor citations (once identity exists):
4. **Yelp** · 5. **BBB** · 6. **Nextdoor** · 7. **Houzz** · 8. **Angi** — per `SEO/CITATIONS.md`.
   SAB rule: hide the street address on Google/Nextdoor; put it on Yelp/Angi/Houz/BBB/FB.
   Business name must be exactly `Bryce's Patios` everywhere.

Phase 3 — depth (the F table above, §F1–F12): **Foursquare** (feeds map apps) ·
**Bing Places** (B4) · **Apple Business Connect** (B5) · **Yandex** (F1) ·
**BuildZoom** (F7) · **D&B** (F8) · **Bark free tier** (F9) · **Tri-Town Chamber**
(F6) · **Patch Mansfield** (F5) · **Pinterest** (F10) · **YouTube showreel** (F11) ·
**Facebook Marketplace + local groups** (F4) · **Reddit** (F3, no link-dropping) ·
**MA HIC registry** (F12 — verify he is registered before writing anything).
Phase 3 is *breadth*, and it is strictly after Phase 1. Fifty citations with no GBP
still lose to one competitor with a verified profile and five reviews.

## ck89 change note

Three copy-only patches landed to close a measured keyword gap:
- home hero lede now carries "owner-operated patio installer out of Mansfield, MA"
- `/areas/mansfield/` carries "patio installer in Mansfield, MA"
- `/learn/paver-cost/` retitled to target "stone patio costs in Massachusetts"

Before the patch, `patio installer mansfield ma` and `stone patio cost
massachusetts` split-words did **not** all appear on the obvious page. After, all
rows in the map above show "yes". Rebuilt (81 pages), re-gated (**SHIP 1.6/100,
45,938 words**), committed `e978d12`, deployed, IndexNow re-pinged (HTTP 200, 81
urls).

## ck98 change note

Closed the AI-extractibility + crawl-plumbing gaps; no copy changed.
- `llms.txt` shipped and linked from `robots.txt` (`LLMs-Txt:` line) and from a
  `<link rel="alternate" type="text/plain">` in all 81 heads (emitted in
  `site.py render_shell` + the hand-maintained `index.html`).
- Real root `/favicon.ico` shipped (was 404 on the bare path).
- Verified live: `/`, `/llms.txt`, `/favicon.ico`, `/robots.txt`,
  `/site.webmanifest`, `/assets/img/favicon.ico`, `/assets/img/icon-512.png`
  all **200**; sitemap **81 `<loc>`**; alt text **100/100**; image sitemap
  **81/81**; JSON-LD **0 failures**; voice gate **SHIP 0/0/0 1.6/100**.
- **Bing re-probe: still 0 indexed** (site: returns the empty-result widget)
  despite repeated IndexNow 200s. Indexation remains the blocker, not quality.

## Honest status of visibility (2026-10-08)

- **Site quality is fine.** 81/81 pages live 200; depth, schema, linking, voice
  all meet target.
- **Indexation is the blocker, not quality.** Bing has not indexed the domain
  despite repeated IndexNow 200s (re-confirmed ck98: `site:brycespatios.work`
  returns the empty-result widget). Google is unmeasurable from this IP (WAF);
  Search Console is the only real read, and it is unclaimed.
- **Off-site authority is the other blocker.** Zero citations, zero reviews, no
  GBP. Organic ranking for the commercial queries is a multi-year fight; the
  local pack is decided by GBP + reviews, which is why GBP is item #1.
- **Do not promise a timeline.** The honest lever we control is: GBP live,
  Search Console claimed, 30+ citations, then real reviews.

## ck112 change note (2026-10-08) — discoverability stack made complete

The user's charge was correct: the plan claimed to "think of everything" but the
F table did not exist. This checkpoint adds it.

- **Added `§F. Extra surfaces we had not written down`** to the Full
  discoverability stack: 14 rows covering Foursquare, Yandex, Reddit, Facebook
  Marketplace + local groups, Patch Mansfield, Tri-Town Chamber, BuildZoom, D&B,
  Bark (free tier only), Pinterest, YouTube, the MA HIC registry, Apple Business
  Connect (dedupe pointer to B5), and the map-data partners (Waze/TomTom/Here
  WeGo) marked **BLOCKED — no direct self-serve** so nobody hunts a signup that
  does not exist. Every row is tagged OURS / HUMAN / BLOCKED / VERIFY, and
  **VERIFY rows are explicitly unconfirmed** — reachability was curl-checked from
  this host, nothing more.
- **Rewrote the off-site platform order into three phases.** Phase 1 is identity
  (GBP + GSC + Facebook), Phase 2 the anchor citations, Phase 3 the F-table
  breadth. Breadth is strictly after identity, with the reason stated: fifty
  citations without a verified profile still lose to one competitor with a live
  profile and five reviews.
- **Back-filled `SEO/BASELINE.md` ck106–ck111** (ck101–ck105 were never logged, so
  that hole is closed too).
- No site files changed. No copy changed. `PAGES 81` unchanged.

### Honest reachability results from this host (curl, 2026-10-08)
| Host | HTTP | Read |
|---|---|---|
| `foursquare.com` | 200 | reachable |
| `buildzoom.com` | 200 | reachable |
| `tri-townchamber.org` | 200 | reachable |
| `business.apple.com` | 200 | reachable |
| `patch.com/massachusetts/mansfield-ma` | 200 | **the real Mansfield, MA hub** (verified in-browser 2026-10-09). `mansfield.patch.com` redirects to Mansfield-Storrs, CT; `patch.com/massachusetts/mansfield` = 404. |
| `dnb.com` | 301 → 200 | reachable |
| `bark.com` | 301 | reachable |
| `yelp.com` | 403 | WAF — not a real read, do not conclude it is down |
| `biz.yandex.ru` | 000 | did not resolve here — **unverified** |
| `mass.gov` (HIC pages) | 403 | WAF — **registry path unverified, must be checked in a browser** |

---
