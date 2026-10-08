# Bryce's Patios — live site guide

Everything in this folder is the live website at **https://brycespatios.work**. Open
`index.html` in a browser and it works — no build step, no npm, no framework.

---

## 1. What's here

```
bryces-patios/
├── index.html            ← the whole site (one page)
├── assets/
│   ├── css/style.css     ← the design system
│   ├── js/main.js        ← nav, slider, form, film
│   └── img/              ← photos and diagrams
├── _masters/             ← full-size PNG originals — do NOT upload this folder
├── robots.txt
└── sitemap.xml
```

**Sections, in order:** hero → the promise → featured work → process → craftsmanship →
about → learn → service area → estimate form → footer.

**What it does:** sticky nav with a scroll progress bar, a mobile slide-out menu, scroll
reveals, a draggable before/after slider (mouse, touch, and arrow keys), a 3-step estimate
form with validation that opens a pre-filled text message to Bryce, a sticky
"call / get an estimate" bar on phones, and a "Watch the build" film that animates through
the photography. It respects reduced-motion settings and works with JavaScript disabled.

---

## 2. Contact details on the site

These are live values. Change them in one pass if they ever change:

| What | Current value | Where |
|---|---|---|
| **Phone** | `(508) 212-6433` / `+15082126433` | nav, mobile menu, form success, footer, sticky bar, structured data |
| **Email** | `bryces-patios@agentmail.to` | footer, `assets/js/main.js`, structured data |
| **Address** | 885 West St, Mansfield, MA | structured data |
| **Service area** | SE Massachusetts and Rhode Island | service area section, structured data |
| **Social handles** | `@brycespatios` | footer icons (unclaimed as of 2026-10-08) |

The social handles are placeholders until claimed. The footer links point at the URLs
Bryce should claim; they will 404 until he does.

---

## 3. What's real and what isn't

**The photography is AI-generated.** It is there so the site launched looking finished
instead of looking empty. It is **not** Bryce's work, and the site says so out loud under the
featured-work section. Real job photos should replace these as soon as possible — see §5.

**The About section contains no invented biography.** No fake years in business, no made-up
credentials, no fabricated family history. It describes how the work is done, which is true
by construction. Two paragraphs are written generically so they can be personalised —
the one starting *"Bryce's Patios is a local, owner-operated hardscaping business…"* and the one
starting *"We keep the crew small on purpose…"*. Give those Bryce's real story.

**No licences, insurance, certifications, warranties, or reviews are claimed anywhere** —
because none were verified. Add them only once confirmed. They are genuinely valuable for
conversion, so it's worth chasing them down.

---

## 4. Where it's hosted

Live on GitHub Pages at **https://brycespatios.work**.

| | |
|---|---|
| Repo | `github.com/Foshowithit/bryces-patios` (public) |
| Fallback URL | `foshowithit.github.io/bryces-patios/` |
| Hosting | GitHub Pages — free |
| DNS | Porkbun |
| Running cost | the domain only, ~$10–12/year |

**How the DNS is set up** — already done, recorded here so it can be rebuilt:

- Four `A` records on the apex → `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`
- Four `AAAA` records → `2606:50c0:8000::153` through `2606:50c0:8003::153`
- `CNAME www` → `foshowithit.github.io` (must point at the *user* domain, never include the
  repo name)
- Porkbun's default parking records were removed: an `ALIAS` on the apex, and a
  **wildcard CNAME `*.brycespatios.work`** — GitHub specifically warns against wildcards
  because they invite domain takeover.
- The `CNAME` file in the repo root tells GitHub which domain to serve. Don't delete it.
- A backup of the original DNS records is in `~/.agent-vault/domains/`.

**To publish a change:** commit and push to `main`. GitHub rebuilds in about a minute.

```bash
cd bryces-patios && git add -A && git commit -m "describe the change" && git push
```

**To move to different hosting** (Netlify, Cloudflare Pages, Vercel): drag the folder in,
then repoint the domain by replacing those A/AAAA records at Porkbun. Delete the `CNAME`
file at that point — it's GitHub-specific.

**One gotcha:** GitHub needs to see the domain resolve before it can issue the HTTPS
certificate. If the site loads on `http://` but not `https://`, the cert hasn't been issued
yet. Check *Settings → Pages → Enforce HTTPS*; it becomes available once the cert lands.

Do **not** upload `_masters/`. It's 28 MB the site never requests.

---

## 5. Swapping in real photos

Drop a new photo into `assets/img/` using the **exact same filename** and it appears on the
site. Nothing else to change.

| Filename | Where it appears | Shoot it as |
|---|---|---|
| `hero.jpg` (+ `hero-900.jpg`) | top of the page | Your best finished job, wide, late afternoon |
| `big-yard.jpg` (+ `-900`) | featured work, card 1 | Wide backyard patio with deck/pool |
| `patio-herringbone.jpg` (+ `-900`) | featured work, card 2 | Herringbone detail running to deck stairs |
| `walkway.jpg` (+ `-900`) | featured work, card 3 | Walkway or grade change mid-job |
| `yard.jpg` (+ `-900`) | before/after "before" frame | Bare / rough yard, from a fixed spot |
| `big-yard.jpg` (reused) | before/after "after" frame | **Same spot, same height, same lens** |
| `steps-detail.jpg` (+ `-900`) | craftsmanship, large | Mid-build: base, gravel, tools |
| `stairs-landing.jpg` (+ `-900`) | craftsmanship, small | Close-up of an edge, joint, or cut |
| `stone-arch.jpg` (+ `-900`) | craftsmanship, third card | Wide shot showing scale / equipment |
| `patio-base.svg` (+ `-mobile`) | craftsmanship diagram | Cross-section illustration |

`og-cover.jpg` is the social share image (1200×630). Update it whenever the hero changes.

**Priority order:** the before/after pair first (the slider is the most persuasive thing on
the page and it only works if the two shots line up), then the three project photos, then
the hero.

Each photo also needs a `-900.jpg` version (900px wide) for phones. On a Mac:

```bash
cd assets/img
for f in *.jpg; do sips -Z 900 -s format jpeg -s formatOptions 82 "$f" --out "${f%.jpg}-900.jpg"; done
```

---

## 6. The estimate form

The form is **SMS-first**. When a visitor finishes it, the site builds a plain-text summary
and opens a pre-filled text message to **+1 (508) 212-6433**. One tap and the lead is in
Bryce's Messages app — no backend, no monthly cost, no lead leaking into a form service.

The success panel also offers:

- **Copy my details** — copies the same summary to the clipboard
- **Email instead** — opens a pre-filled email to `bryces-patios@agentmail.to`
- **Rather talk? Call Bryce** — direct `tel:` link

If the browser blocks the `sms:` link, the visitor gets the copy button and the phone/email
fallbacks instead of a dead end.

### Optional: a real endpoint later

If Bryce ever wants leads to also land in an inbox automatically, set `FORM_ENDPOINT` at the
top of `assets/js/main.js`:

```js
const FORM_ENDPOINT = 'https://formspree.io/f/yourIDhere';
```

When set, the form POSTs the lead first and falls back to the SMS path if the endpoint
fails. Leave it empty to stay on the pure SMS path.

---

## 7. Google Business Profile — do this first

For a local contractor, this matters **more than the website**. It's how people find you
on Maps, and it's free.

1. [business.google.com](https://business.google.com) → add Bryce's Patios
2. Category: **Paving contractor** or **Landscaper** (whichever fits — pick the most specific)
3. Service area: Mansfield plus the towns listed on the site
4. Hours, phone, website URL
5. Upload 10+ photos immediately (before/after pairs perform best)
6. Ask the first 5 happy customers for a review — send them the direct review link

Then keep it alive: one new photo a week, and reply to every review.

---

## 8. What to add next, in order

1. **Real photos** — the single biggest upgrade available
2. **Google reviews** — add a reviews section once there are 5+; it's the highest-converting
   element a contractor site can have
3. **A real film** — Bryce's phone, one finished job, 30–45 seconds. Drop it at
   `assets/video/hero-film.mp4` and the "Watch the build" button can play it instead of the
   photo sequence
4. **A licence / insurance / warranty line** — once verified, in the hero meta row and footer
5. **A dedicated gallery page** — once there are 15+ real jobs to show
6. **A second page per service** — patios, walkways, fire pits. Good for local search

---

## 9. Editing the site

Open `index.html` in any text editor. The sections are labelled with comment banners like
`<!-- ══ 03 TRANSFORMATION ══ -->`, so you can find what you want by searching for it.

Colours and fonts live at the top of `assets/css/style.css` under `:root`. Change
`--moss` and the whole site's accent colour follows.

**One rule: don't change the copy while you're moving things around.** Text edits and layout
edits in the same pass are how a working page gets broken.
