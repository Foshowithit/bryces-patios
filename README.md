# Bryce's Patios — website

**Live:** https://brycespatios.work
**Repo fallback:** https://foshowithit.github.io/bryces-patios/

A single-page site for Bryce's Patios — custom patios, walkways and outdoor living
in Mansfield, Massachusetts.

Hand-built HTML, CSS and JavaScript. No build step, no framework, no dependencies. Open
`index.html` in a browser and it runs.

---

## Read this first

The site is live. The photography is AI-generated and disclosed on the page; it exists so the
site launches looking finished rather than empty. Real job photos should replace it as soon
as Bryce can shoot them.

Everything on the page is real:

- **Phone:** (508) 212-6433
- **Email:** bryces-patios@agentmail.to
- **Address:** 885 West St, Mansfield, MA
- **Service area:** Southeastern Massachusetts and Rhode Island, roughly a few hours of
  travel when a job justifies it

No licenses, insurance, certifications, warranties, or reviews are claimed anywhere,
because none have been verified. Add them only once confirmed.

Full details, including the remaining launch work: **[LAUNCH.md](LAUNCH.md)**.

---

## What's in here

```
index.html                  the whole site — one page
assets/css/style.css        design system
assets/js/main.js           nav, before/after slider, estimate form, film
assets/img/                 photos and diagrams used by the page
social/SOCIAL-KIT.md        handles, bios, 30-day content calendar, captions, hashtags
social/highlight-covers/    8 Instagram highlight covers (1080×1920)
LAUNCH.md                   what to replace, how to deploy, what to add next
```

`_masters/` (full-size PNG originals) is gitignored — it's 28 MB the site never requests.

## Sections

Hero → the promise → featured work → process → craftsmanship → about → learn →
service area → estimate form → footer.

## Interactions

- Sticky nav with scroll progress and a mobile slide-out menu
- **Draggable before/after slider** — mouse, touch, and arrow keys
- **3-step estimate form** with per-step validation; on finish it opens a pre-filled
  text message to Bryce, with copy and email fallbacks
- **"Watch the build"** — an animated sequence built from the stills. Swap in real
  footage later.
- Sticky call/estimate bar on phones
- Responsive images via `srcset`, reduced-motion support, works without JavaScript

## Publishing

The site is live on GitHub Pages via the `CNAME` file in the repo root. Commit to `main`,
push, and the change is usually live in about a minute:

```bash
git add -A && git commit -m "describe the change" && git push
```

Do **not** upload `_masters/`. It's 28 MB of source files the site never requests.
