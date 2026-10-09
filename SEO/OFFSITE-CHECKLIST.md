# Off-site visibility checklist — do these in order (~30 min total)

**Why:** the website is built and passes the voice/quality gate. It gets **zero
calls until it is discovered.** Google, Maps, and the directories are where
Mansfield homeowners actually find a patio contractor. Every item below is
**free**. Most rows need Bryce's (or Adam's-as-Manager) identity to execute; the
`[OURS]` rows are ours to build, check, and monitor.

**Adam's Google session is signed in on this box** (`adamnorm4wd@gmail.com`),
so the Google rows (GBP, Search Console) are **not** blocked on Bryce's login if
Adam acts as Manager. Bryce still has to own the profile long term (it owns the
reviews + Maps history), and the verification video needs the truck and a job site,
so a sitting with Bryce is still the right way. Verified in-browser 2026-10-09:
`business.google.com/add` and `search.google.com/search-console/welcome` both open
Google sign-in with Adam's account. Apple Business Connect is `business.apple.com`
(`businessconnect.apple.com` redirects there). Bing Places is `bingplaces.com`
(redirects to `bing.com/forbusiness/`).

**Ownership markers (added 2026-10-09).** Every row below is tagged:

- **`[HUMAN]`** — needs Bryce's (or Adam's-as-Manager) identity or a login; **we
  cannot do it**, it is copy-paste sitting for them. This is the entire remaining
  gap: it is account work, not build work.
- **`[OURS]`** — our job: build, copy, content, code, monitoring, or a check we run.

`SEO/PLAN.md` §F carries the same split as the plan of record.

**The one rule:** the business name is exactly `Bryce's Patios` everywhere. Not
`Bryce's Patios Mansfield`, not `Bryce's Patios | Patio Installer`. Keyword-stuffed
names get listings suspended.

---

## START HERE - the five things that matter, in order

Everything else in this file is detail. If you only do five things, do these. The
first three take about 15 minutes and are the whole ballgame.

1. **Google Business Profile.** `business.google.com/add` -> sign in as
   `adamnorm4wd@gmail.com` -> name `Bryce's Patios`, category `Paving Contractor`,
   address hidden, the 20 towns from `SEO/GBP.md` S4, description from S2, then the
   verification video (S9 in `SEO/GBP.md` has the shot list). **This is the #1 lever
   by a wide margin. Nothing else matters as much.**
2. **Search Console.** `search.google.com/search-console/welcome` -> Add property ->
   **Domain** -> `brycespatios.work` -> verify with the DNS TXT record (Porkbun) ->
   Sitemaps -> submit `https://brycespatios.work/sitemap.xml`. This is the only way
   to ever see what people search.
3. **Facebook page.** Set the website to `https://brycespatios.work` and the phone
   to `(508) 212-6433`. It already exists and already ranks for the brand.
4. **Then the anchor citations** (S5): Yelp, BBB, Nextdoor, Houzz, Angi. Same NAP
   block every time, from `SEO/CITATIONS.md` S0.
5. **Then reviews.** At 5+ real reviews the profile starts to win the local pack.
   Never buy them.

Add Adam as Manager on the GBP the moment it is live (Settings -> People and access)
so the work continues without Bryce at the keyboard.

---

## 1. Google Business Profile  ← THE #1 ITEM

- [ ] `[HUMAN]` Google Maps → search `Bryce's Patios Mansfield`. **If anything comes up, claim
      that listing instead of creating a new one.** Two profiles = both banned.
- [ ] `[HUMAN]` Go to **https://business.google.com/add**
- [ ] `[HUMAN]` Sign in with a Gmail Bryce will keep forever (it owns the reviews + Maps history)
- [ ] `[HUMAN]` Business name: `Bryce's Patios`
- [ ] `[HUMAN]` Primary category: `Paving Contractor` (from the dropdown). Secondaries:
      `Masonry Contractor`, `Landscaper`
- [ ] `[HUMAN]` Address: `885 West St, Mansfield, MA 02048` — then set **"show address" = NO**
- [ ] `[HUMAN]` Service area: paste the **20 towns** from `SEO/GBP.md` §4 (Google caps this field at
      20; the site + directories describe the full 22-town area, see `SEO/CITATIONS.md` §0)
- [ ] `[HUMAN]` Phone: `(508) 212-6433` · Website: `https://brycespatios.work`
- [ ] `[HUMAN]` Hours: Mon–Fri `8:00 AM – 6:00 PM`, Sat/Sun closed (say "by appointment" in the
      description text instead)
- [ ] `[HUMAN]` Description: paste the 741-char block from `SEO/GBP.md` §2
- [ ] `[HUMAN]` Services: add all 8 rows from `SEO/GBP.md` §7
- [ ] `[HUMAN]` Attributes: `Small business`, `Locally owned`, `Free estimates`,
      `Onsite services`, `Appointment required`
- [ ] `[HUMAN]` Photos: upload logo + cover + 4 finished-job photos **the same day**
- [ ] `[HUMAN]` Submit the verification video (Google asks for it — film the truck + the yard)
- [ ] `[HUMAN]` After it's live: **add Adam as Manager** (Settings → People and access)
- [ ] `[HUMAN]` POST SCRIPT: seed the 10 Q&As from `SEO/GBP.md` §10

**Full build-out, copy, and video script:** `SEO/GBP.md` (source of truth).

---

## 2. Google Search Console  ← only fast path to Google index

- [ ] `[HUMAN]` **https://search.google.com/search-console** → Add property → **Domain** →
      `brycespatios.work`
- [ ] `[HUMAN]` Verify with the DNS **TXT** record (Porkbun → DNS → add TXT)
- [ ] `[HUMAN]` Sitemaps → submit `https://brycespatios.work/sitemap.xml`
- [ ] `[HUMAN]` (Optional but good) URL Inspection → paste the homepage → **Request indexing**

This is also the only place we will ever see real impressions, clicks, and the
queries people use. Without it we are blind.

---

## 3. Bing Webmaster Tools  ← IndexNow alone isn't working

Reality check recorded in `SEO/BASELINE.md`: after 3 rounds of IndexNow `HTTP 200`,
Bing still indexes **0** pages of this site. Pings are not enough for a new domain.

- [ ] `[HUMAN]` **https://www.bing.com/webmasters** → Add site → `brycespatios.work`
- [ ] `[HUMAN]` Verify (you can import directly from Google Search Console once §2 is done)
- [ ] `[HUMAN]` Submit `https://brycespatios.work/sitemap.xml`
- [ ] `[OURS]` Check Index → Pages after a few days and record the count in `SEO/BASELINE.md` (HUMAN only submits the sitemap; the re-check is ours)

---

## 4. Facebook page → claim the handle

The site's footer and schema already link `@brycespatios`. Make it real.

- [ ] `[HUMAN]` Page: `Bryces Landscape and Patio Service` (already exists — **checked live 2026-10-09: 31 followers, phone `(508) 212-6433` correct, address 885 West St correct, but there is NO website link on the page**)
- [ ] `[HUMAN]` **Add the website field `https://brycespatios.work`** — this is the one gap on the page, and the page already ranks #1 for "bryce patios mansfield". Do this one first; it is a two-minute edit.
- [ ] `[HUMAN]` Set phone `(508) 212-6433`, Mansfield service area, same photos
- [ ] `[HUMAN]` **Do not edit anything else on the page without Bryce's OK.**

---

## 5. Free high-authority citations (one ~15-min setup each)

Paste the NAP block from `SEO/CITATIONS.md` §0 everywhere, exactly as written.

- [ ] `[HUMAN]` **Yelp** — https://business.yelp.com/claim (claim the free tier)
- [ ] `[HUMAN]` **BBB** — https://www.bbb.org/get-accredited (free profile)
- [ ] `[HUMAN]` **Nextdoor** — https://business.nextdoor.com (free; hide street address)
- [ ] `[HUMAN]` **Houzz** — https://pro.houzz.com/pro (free pro profile; design-led)
- [ ] `[HUMAN]` **Angi** — https://signup.angi.com/pro (free profile only — do NOT buy leads,
      a one-man shop loses money on shared leads)

---

## 5b. Phase-3 breadth — do these AFTER Google is live (each ~10 min, all free)

These add citation depth once the profile exists. Order by impact. Full detail in
`SEO/PLAN.md` §F.

- [ ] `[HUMAN]` **Foursquare** — https://foursquare.com (free listing; its place data feeds
      a lot of navigation + map apps, so it punches above its weight)
- [ ] `[HUMAN]` **Bing Places** — https://www.bingplaces.com (free, mirrors the GBP copy;
      Bing is also where our IndexNow pings land)
- [ ] `[HUMAN]` **BuildZoom** — https://www.buildzoom.com (free contractor profile; it
      already appeared in our own search baseline, so claim it)
- [ ] `[HUMAN]` **D&B** — https://www.dnb.com (free basic business profile)
- [ ] `[HUMAN]` **Bark** — https://www.bark.com (free profile only; do NOT buy shared leads)
- [ ] `[HUMAN]` **Tri-Town Chamber** — https://www.tri-townchamber.org (member directory
      entry is a strong local citation; membership is paid — decide with Bryce)
- [ ] `[HUMAN]` **Pinterest** — design-led, patio photos travel well and link back
- [ ] `[HUMAN]` **YouTube** — upload the mini showreel (we render it on the Dell; the upload needs his channel) (`~/Movies/bryce-patios-reel/`,
      16:9 / 9:16 / 1:1 all rendered and ready)
- [ ] `[HUMAN]` **Facebook Marketplace + local groups** — finished-yard photos, plain price
      range, no spam. This is where local jobs actually get seen.
- [ ] `[HUMAN]` **Reddit** (r/massachusetts, r/landscaping, r/HomeImprovement) — real answers
      only, **no link-dropping** (instant ban). Reputation, not a citation.
- [ ] `[OURS]`/`[HUMAN]` **Patch Mansfield, MA** — VERIFIED in-browser 2026-10-09:
      the town hub is **`https://patch.com/massachusetts/mansfield-ma`**
      (title "Mansfield News, Breaking News in Mansfield, MA"). Do **not** use
      `mansfield.patch.com` (redirects to Mansfield-**Storrs, CT**, wrong state) or
      `patch.com/massachusetts/mansfield` (404s). Patch runs no free business
      directory, so this is only useful as a real-news/community surface — HUMAN
      posts a genuine build photo or a quick "before/after" note there, no link-drop.
- [ ] `[OURS]`/`[HUMAN]` **Yandex Business** — VERIFIED in-browser 2026-10-09: the
      self-serve add-business page is `https://business.yandex.ru/sprav/index`
      (`yandex.com/sprav` redirects there). A contractor self-serve does exist.
      HUMAN signs up and copies the NAP block from `SEO/CITATIONS.md` §0.
- [ ] `[OURS]`/`[HUMAN]` **MA HIC registry** — the lookup is
      **`https://hicsearch.attorneygeneral.gov`** (verified in-browser 2026-10-09;
      fields: Registration No., Business Name, Primary Applicant, City, State). Search
      `Bryce` + State `Massachusetts`. Never claim a licence he does not hold. If he
      is registered, this is a top-tier trust citation and HUMAN adds it to the
      listings. (Do not use `elicensing.mass.gov` — DOL moved to eLIPSE and the old
      paths 404.)

**Do not bother with:** Waze, TomTom, Here WeGo marketplaces, or Yandex
"map" signups — there is **no direct contractor self-serve** for those; place data
reaches them downstream from Apple/Bing/Yelp/Foursquare. Marked BLOCKED in
`SEO/PLAN.md` §F14 so nobody hunts a signup that does not exist.

---

## 6. After GBP is live — turn on the review engine

- [ ] `[HUMAN]` Copy the GBP review short-link into `SEO/REVIEWS.md`
- [ ] `[HUMAN]` Print/save the QR code and text it to the next happy customer
- [ ] `[HUMAN]` Ask in person, the day the job ends, phone in hand
- [ ] `[OURS]` At **5+ real reviews** we add `aggregateRating` to the schema. Until
      then it stays out. Never invent one. HUMAN only shares the review link and
      collects the reviews.

---

## Consistency audit — `[OURS]` to run against live listings; `[HUMAN]` to fix any mismatch

- [ ] `[HUMAN]` Name exactly `Bryce's Patios`
- [ ] `[HUMAN]` Phone exactly `(508) 212-6433`
- [ ] `[HUMAN]` Website exactly `https://brycespatios.work`
- [ ] `[HUMAN]` Address string exactly `885 West St, Mansfield, MA 02048` (where shown)
- [ ] `[HUMAN]` Hours match; primary category is paving/landscaping, never generic "Contractor"
- [ ] `[HUMAN]` The single approved long description (no per-site rewrites)
- [ ] `[HUMAN]` No licence / insurance / warranty / rating claims anywhere
