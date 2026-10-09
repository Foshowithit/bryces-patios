# Off-site visibility checklist — do these in order (~30 min total)

**Why:** the website is built and passes the voice/quality gate. It gets **zero
calls until it is discovered.** Google, Maps, and the directories are where
Mansfield homeowners actually find a patio contractor. Every item below is
**free**. Nobody but Bryce (or Adam, once added as Manager) can do these — they
need his identity.

**The one rule:** the business name is exactly `Bryce's Patios` everywhere. Not
`Bryce's Patios Mansfield`, not `Bryce's Patios | Patio Installer`. Keyword-stuffed
names get listings suspended.

---

## 1. Google Business Profile  ← THE #1 ITEM

- [ ] Google Maps → search `Bryce's Patios Mansfield`. **If anything comes up, claim
      that listing instead of creating a new one.** Two profiles = both banned.
- [ ] Go to **https://business.google.com/add**
- [ ] Sign in with a Gmail Bryce will keep forever (it owns the reviews + Maps history)
- [ ] Business name: `Bryce's Patios`
- [ ] Primary category: `Paving Contractor` (from the dropdown). Secondaries:
      `Masonry Contractor`, `Landscaper`
- [ ] Address: `885 West St, Mansfield, MA 02048` — then set **"show address" = NO**
- [ ] Service area: paste the **20 towns** from `SEO/GBP.md` §4 (Google caps this field at
      20; the site + directories describe the full 22-town area, see `SEO/CITATIONS.md` §0)
- [ ] Phone: `(508) 212-6433` · Website: `https://brycespatios.work`
- [ ] Hours: Mon–Fri `8:00 AM – 6:00 PM`, Sat/Sun closed (say "by appointment" in the
      description text instead)
- [ ] Description: paste the 741-char block from `SEO/GBP.md` §2
- [ ] Services: add all 8 rows from `SEO/GBP.md` §7
- [ ] Attributes: `Small business`, `Locally owned`, `Free estimates`,
      `Onsite services`, `Appointment required`
- [ ] Photos: upload logo + cover + 4 finished-job photos **the same day**
- [ ] Submit the verification video (Google asks for it — film the truck + the yard)
- [ ] After it's live: **add Adam as Manager** (Settings → People and access)
- [ ] POST SCRIPT: seed the 10 Q&As from `SEO/GBP.md` §10

**Full build-out, copy, and video script:** `SEO/GBP.md` (source of truth).

---

## 2. Google Search Console  ← only fast path to Google index

- [ ] **https://search.google.com/search-console** → Add property → **Domain** →
      `brycespatios.work`
- [ ] Verify with the DNS **TXT** record (Porkbun → DNS → add TXT)
- [ ] Sitemaps → submit `https://brycespatios.work/sitemap.xml`
- [ ] (Optional but good) URL Inspection → paste the homepage → **Request indexing**

This is also the only place we will ever see real impressions, clicks, and the
queries people use. Without it we are blind.

---

## 3. Bing Webmaster Tools  ← IndexNow alone isn't working

Reality check recorded in `SEO/BASELINE.md`: after 3 rounds of IndexNow `HTTP 200`,
Bing still indexes **0** pages of this site. Pings are not enough for a new domain.

- [ ] **https://www.bing.com/webmasters** → Add site → `brycespatios.work`
- [ ] Verify (you can import directly from Google Search Console once §2 is done)
- [ ] Submit `https://brycespatios.work/sitemap.xml`
- [ ] Check Index → Pages after a few days and record the count

---

## 4. Facebook page → claim the handle

The site's footer and schema already link `@brycespatios`. Make it real.

- [ ] Page: `Bryces Landscape and Patio Service` (already exists)
- [ ] Set the website field to `https://brycespatios.work`
- [ ] Set phone `(508) 212-6433`, Mansfield service area, same photos
- [ ] **Do not edit anything else on the page without Bryce's OK.**

---

## 5. Free high-authority citations (one ~15-min setup each)

Paste the NAP block from `SEO/CITATIONS.md` §0 everywhere, exactly as written.

- [ ] **Yelp** — https://business.yelp.com/claim (claim the free tier)
- [ ] **BBB** — https://www.bbb.org/get-accredited (free profile)
- [ ] **Nextdoor** — https://business.nextdoor.com (free; hide street address)
- [ ] **Houzz** — https://pro.houzz.com/pro (free pro profile; design-led)
- [ ] **Angi** — https://signup.angi.com/pro (free profile only — do NOT buy leads,
      a one-man shop loses money on shared leads)

---

## 5b. Phase-3 breadth — do these AFTER Google is live (each ~10 min, all free)

These add citation depth once the profile exists. Order by impact. Full detail in
`SEO/PLAN.md` §F.

- [ ] **Foursquare** — https://foursquare.com (free listing; its place data feeds
      a lot of navigation + map apps, so it punches above its weight)
- [ ] **Bing Places** — https://www.bingplaces.com (free, mirrors the GBP copy;
      Bing is also where our IndexNow pings land)
- [ ] **BuildZoom** — https://www.buildzoom.com (free contractor profile; it
      already appeared in our own search baseline, so claim it)
- [ ] **D&B** — https://www.dnb.com (free basic business profile)
- [ ] **Bark** — https://www.bark.com (free profile only; do NOT buy shared leads)
- [ ] **Tri-Town Chamber** — https://www.tri-townchamber.org (member directory
      entry is a strong local citation; membership is paid — decide with Bryce)
- [ ] **Pinterest** — design-led, patio photos travel well and link back
- [ ] **YouTube** — upload the mini showreel (`~/Movies/bryce-patios-reel/`,
      16:9 / 9:16 / 1:1 all rendered and ready)
- [ ] **Facebook Marketplace + local groups** — finished-yard photos, plain price
      range, no spam. This is where local jobs actually get seen.
- [ ] **Reddit** (r/massachusetts, r/landscaping, r/HomeImprovement) — real answers
      only, **no link-dropping** (instant ban). Reputation, not a citation.
- [ ] **Patch Mansfield** — confirm the current Mansfield hub in a browser
      (`patch.com/massachusetts/mansfield` 404s; `mansfield.patch.com` is up), then
      check for a free business listing
- [ ] **Yandex Business** — https://yandex.com/sprav (verify the self-serve URL in a
      browser first; `biz.yandex.ru` does not resolve from our host)
- [ ] **MA HIC registry** — Massachusetts publishes a HIC registration lookup.
      **Only pursue if Bryce is actually registered.** Never claim a licence he
      does not hold. If he is registered, this is a top-tier trust citation.

**Do not bother with:** Waze, TomTom, Here WeGo marketplaces, or Yandex
"map" signups — there is **no direct contractor self-serve** for those; place data
reaches them downstream from Apple/Bing/Yelp/Foursquare. Marked BLOCKED in
`SEO/PLAN.md` §F14 so nobody hunts a signup that does not exist.

---

## 6. After GBP is live — turn on the review engine

- [ ] Copy the GBP review short-link into `SEO/REVIEWS.md`
- [ ] Print/save the QR code and text it to the next happy customer
- [ ] Ask in person, the day the job ends, phone in hand
- [ ] At **5+ real reviews**, tell us and we add `aggregateRating` to the schema.
      Until then it stays out. Never invent one.

---

## Consistency audit (run after each listing goes live)

- [ ] Name exactly `Bryce's Patios`
- [ ] Phone exactly `(508) 212-6433`
- [ ] Website exactly `https://brycespatios.work`
- [ ] Address string exactly `885 West St, Mansfield, MA 02048` (where shown)
- [ ] Hours match; primary category is paving/landscaping, never generic "Contractor"
- [ ] The single approved long description (no per-site rewrites)
- [ ] No licence / insurance / warranty / rating claims anywhere
