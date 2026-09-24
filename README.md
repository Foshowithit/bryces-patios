# Bryce's Patios — website concept

**Live:** https://brycespatios.work
**Repo fallback:** https://foshowithit.github.io/bryces-patios/

A single-page site concept for Bryce's Patios — custom patios, walkways and outdoor living
in Attleboro, Massachusetts.

Hand-built HTML, CSS and JavaScript. No build step, no framework, no dependencies. Open
`index.html` in a browser and it runs.

---

## ⚠️ Read this first

This is a **concept**, not a finished site. Two things are not real:

1. **The photography is AI-generated.** It is not Bryce's work. It's there so the design
   can be reviewed as a finished thing rather than as an empty shell. The page says so
   out loud under the featured-work section.
2. **The phone number, email, domain, social handles and project towns are placeholders.**
   `(508) 555-0134` is a reserved fiction number and does not ring.

The site is set `noindex` and `Disallow: /` on purpose, so it can't surface in search
results as Bryce's real work before it is. Both are marked in the code with the exact
lines to reverse at launch.

Full details, including the launch checklist: **[LAUNCH.md](LAUNCH.md)**.

---

## What's in here

```
index.html                  the whole site — 8 sections
assets/css/style.css        design system
assets/js/main.js           nav, before/after slider, estimate form, film
assets/img/                 9 photos, each in 900w and 1536w
social/SOCIAL-KIT.md        handles, bios, 30-day content calendar, captions, hashtags
social/highlight-covers/    8 Instagram highlight covers (1080×1920)
LAUNCH.md                   what to replace, how to deploy, what to add next
```

`_masters/` (full-size PNG originals) is gitignored — it's 28 MB the site never requests.

## Sections

Hero → the promise → featured work → before/after transformation → craftsmanship → about →
service area → estimate form → footer.

## Interactions

- Sticky nav with scroll progress and a mobile slide-out menu
- **Draggable before/after slider** — mouse, touch, and arrow keys
- **3-step estimate form** with per-step validation
- **"Watch the build"** — an animated sequence built from the stills, so it works with no
  video file. Swap in real footage later.
- Sticky call/estimate bar on phones
- Responsive images via `srcset`, reduced-motion support, works without JavaScript

## Making variants

To try an alternative direction, drop it in a subfolder and it gets its own URL for free:

```
v2/index.html   →  https://foshowithit.github.io/bryces-patios/v2/
```

Push and it's live in about a minute. Nothing else to configure.
