# Bryce's Patios — launch guide

Everything in this folder is the live website. Open `index.html` in a browser and it works —
no build step, no npm, no framework. Drag the folder onto any host and it's online.

---

## 1. What's here

```
bryces-patios/
├── index.html            ← the whole site (one page, 8 sections)
├── assets/
│   ├── css/style.css     ← the design system
│   ├── js/main.js        ← nav, slider, form, film
│   └── img/              ← 9 photos, each in 2 sizes
├── _masters/             ← full-size PNG originals — do NOT upload this folder
├── robots.txt
└── sitemap.xml
```

**Sections, in order:** hero → the promise → featured work → before/after transformation →
craftsmanship → about → service area → estimate form → footer.

**What it does:** sticky nav with a scroll progress bar, a mobile slide-out menu, scroll
reveals, a draggable before/after slider (mouse, touch, and arrow keys), a 3-step estimate
form with validation, a sticky "call / get an estimate" bar on phones, and a "Watch the
build" film that animates through the photography. It respects reduced-motion settings and
works with JavaScript disabled.

---

## 2. ⚠️ Replace these before it goes live

These are the only invented values on the site. Everything else is real or generic.

| What | Current placeholder | Where |
|---|---|---|
| **Phone** | `(508) 555-0134` | nav, mobile menu, form success, footer, sticky bar, structured data |
| **Email** | `hello@brycespatios.work` | footer, `assets/js/main.js`, structured data |
| **Social handles** | `@brycespatios` | footer icons |
| **Project names & towns** | Norton MA, Cumberland RI, Rehoboth MA | featured work section |

`555-01xx` is a reserved fiction number — it is **not** a working phone line. It must be
replaced.

The domain is **not** a placeholder — `brycespatios.work` is bought and pointed at this
site. See §4.

One command replaces the phone and email everywhere:

```bash
cd bryces-patios
sed -i '' 's/(508) 555-0134/(508) 123-4567/g; s/+15085550134/+15081234567/g' index.html
sed -i '' 's/hello@brycespatios.work/real@address.com/g' index.html assets/js/main.js
```

(Use the real digits — both the display version and the `tel:` version need changing.)

---

## 3. Two honest caveats

**The photography is AI-generated.** It is there so the site launches looking finished
instead of looking empty. It is **not** Bryce's work, and the site says so out loud under the
featured-work section. Real job photos should replace these as soon as possible — see §5.
When they do, delete this line in `index.html`:

```html
<p class="work__note" data-reveal>…</p>
```

**The About section contains no invented biography.** No fake years in business, no made-up
credentials, no fabricated family history. It describes how the work is done, which is true
by construction. Two paragraphs are written generically so they can be personalised — the
one starting *"Bryce's Patios is a local, owner-operated hardscaping business…"* and the one
starting *"We keep the crew small on purpose…"*. Give those Bryce's real story.

**No licences, insurance, certifications, warranties, or reviews are claimed anywhere** —
because none were verified. Add them only once confirmed. They are genuinely valuable for
conversion, so it's worth chasing them down.

**The site is deliberately set to not be indexed by search engines.** Because the
photography isn't real, letting Google index this page would mean it could surface as
Bryce's work — and that's hard to walk back once it's cached. Two things to reverse at
launch, and only when real photos are in:

1. Delete the `<meta name="robots" content="noindex, nofollow">` line in `index.html`
   (it's marked with a ⚠️ comment so it's easy to find)
2. Replace `robots.txt` with the version quoted in the comment at the top of that file

Until then it's a private-ish preview link: shareable with Bryce, not discoverable by his
customers.

---

## 4. Where it's hosted

Already live on GitHub Pages at **https://brycespatios.work**.

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
  **wildcard `CNAME *.brycespatios.work`** — GitHub specifically warns against wildcards
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

Do **not** upload `_masters/`. It's 28 MB of source files the site never requests.

---

## 5. Swapping in real photos

Drop a new photo into `assets/img/` using the **exact same filename** and it appears on the
site. Nothing else to change.

| Filename | Where it appears | Shoot it as |
|---|---|---|
| `hero.jpg` | top of the page | Your best finished job, wide, late afternoon |
| `project-firepit.jpg` | featured work, card 1 | Fire pit or evening patio, warm light |
| `project-walkway.jpg` | featured work, card 2 | Steps, walkway, or a grade change |
| `project-dining.jpg` | featured work, card 3 | Dining or entertaining space, daytime |
| `transform-before.jpg` | slider, "before" | Bare yard, from a fixed spot |
| `transform-after.jpg` | slider, "after" | **Same spot, same height, same lens** |
| `craft-base.jpg` | craftsmanship, large | Mid-build: base, gravel, tools |
| `craft-edge.jpg` | craftsmanship, small | Close-up of an edge, joint, or cut |
| `about-site.jpg` | about section | Jobsite, truck, tools, or Bryce at work |

**Priority order:** the before/after pair first (the slider is the most persuasive thing on
the page and it only works if the two shots line up), then the three project photos, then
the hero.

Each image also needs a `-900.jpg` version (900px wide, quality ~78) for phones. On a Mac:

```bash
cd assets/img
for f in *.jpg; do sips -Z 900 -s format jpeg -s formatOptions 78 "$f" --out "${f%.jpg}-900.jpg"; done
```

---

## 6. Making the estimate form actually deliver

Right now the form collects everything, validates it, then hands the visitor a pre-filled
email to send. That works with zero backend and no monthly cost — but it's one extra click,
and some people won't take it.

To make it deliver straight to an inbox, sign up at [formspree.io](https://formspree.io)
(free tier is fine), then open `assets/js/main.js` and fill in one line at the top:

```js
const FORM_ENDPOINT = 'https://formspree.io/f/yourIDhere';
```

That's it. The form will POST the lead directly, and automatically fall back to the email
route if the endpoint ever fails.

---

## 7. Google Business Profile — do this first

For a local contractor, this matters **more than the website**. It's how people find you on
Maps, and it's free.

1. [business.google.com](https://business.google.com) → add Bryce's Patios
2. Category: **Paving contractor** or **Landscaper** (whichever fits — pick the most specific)
3. Service area: Attleboro plus the towns listed on the site
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
