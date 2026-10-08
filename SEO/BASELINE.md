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
