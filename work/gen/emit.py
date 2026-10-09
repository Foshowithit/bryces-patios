#!/usr/bin/env python3
"""Emit layer for the Bryce's Patios static site.

Imported by work/gen/site.py at the bottom. Builds:
  /learn/                          guides hub
  /learn/<key>/                    six guide pages
  /services/                       services hub
  /services/<key>/                 four service pages
  /areas/                          service-area hub
  /areas/<town-slug>/              twelve MA town pages
  /areas/<town-slug>/<svc-key>/    twelve service x town pages (top 6 towns)
  sitemap.xml                      every URL, real lastmod
Pages reuse the shared style.css classes.
"""
from __future__ import annotations

import datetime as _dt
import importlib.util as _ilu
import sys as _sys
from pathlib import Path

# Load work/gen/site.py explicitly. `import site` alone would hit the stdlib
# `site` module (already in sys.modules at interpreter start).
_sys.path.insert(0, str(Path(__file__).resolve().parent))
_spec = _ilu.spec_from_file_location("bryce_site", Path(__file__).resolve().parent / "site.py")
site = _ilu.module_from_spec(_spec)
_sys.modules["bryce_site"] = site
_spec.loader.exec_module(site)
_GUIDE_LIST = site.GUIDES
_SVC_LIST = site.SERVICES
_MA = site.TOWNS_MA
_TOP = site.TOP_TOWNS

# ── shared bits ────────────────────────────────────────────────────────────
# real intrinsic dimensions of each full-size JPG (px) — must match assets/img/<name>.jpg
IMG_DIMS = {
    "about-site": (1200, 900), "big-yard": (1600, 1067), "craft-base": (1600, 1067),
    "craft-edge": (1600, 1067), "hero": (1600, 1067), "og-cover": (1200, 630),
    "patio-herringbone": (1600, 1067), "project-dining": (1600, 1067),
    "project-firepit": (1600, 1067), "project-walkway": (1600, 1067),
    "stairs-landing": (1200, 1200), "steps-detail": (1200, 800), "stone-arch": (1200, 1200),
    "transform-after": (1400, 933), "transform-before": (1400, 933),
    "walkway": (1600, 1067), "yard": (1600, 1066),
}

def _img(name: str, alt: str, sizes: str, *, cls: str = "", loading="lazy") -> str:
    esc = site.esc
    w, h = IMG_DIMS[name]
    c = f' class="{cls}"' if cls else ""
    return (
        f'<img{c} src="/assets/img/{name}.jpg" '
        f'srcset="/assets/img/{name}-900.jpg 900w, /assets/img/{name}.jpg 2000w" '
        f'sizes="{sizes}" width="{w}" height="{h}" loading="{loading}" decoding="async" '
        f'alt="{esc(alt)}">'
    )

def _sec_head(eyebrow: str, h2: str, sub: str = "", *, center=False) -> str:
    esc = site.esc
    cls = "section__head section__head--center" if center else "section__head"
    s = f'\n      <p class="section__sub">{esc(sub)}</p>' if sub else ""
    return f'''<header class="{cls}">
      <p class="eyebrow">{esc(eyebrow)}</p>
      <h2 class="h2">{esc(h2)}</h2>{s}
    </header>'''

def _faq_block(faqs) -> str:
    esc = site.esc
    rows = []
    for q, a in faqs:
        rows.append(
            f'<details class="qa"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        )
    return '<div class="qa-list">' + "".join(rows) + "</div>"

def _faq_ld(faqs, url: str) -> dict:
    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }

def _cta(url_trail, headline: str, sub: str) -> str:
    esc, PHONE_TEL, PHONE_TXT = site.esc, site.PHONE_TEL, site.PHONE_TXT
    return f'''<section class="section section--dark cta-band">
  <div class="wrap">
    <div class="cta-band__inner">
      <div>
        <h2 class="h2 h2--light">{esc(headline)}</h2>
        <p class="section__sub">{esc(sub)}</p>
      </div>
      <div class="cta-band__actions">
        <a class="btn btn--solid" href="/#estimate">Get a free estimate</a>
        <a class="btn btn--quiet" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a>
      </div>
    </div>
  </div>
</section>'''

# ── writers ────────────────────────────────────────────────────────────────
def write_page(root: Path, rel: str, html_str: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html_str, encoding="utf-8")
    return p

def _svc_links():
    return [(s["name"], f"/services/{s['key']}/") for s in _SVC_LIST]

def _town_links():
    return [(f"{t}, MA", f"/areas/{t.lower().replace(' ', '-')}/") for t in _MA]

def _guide_by_key(key: str) -> dict | None:
    for g in _GUIDE_LIST:
        if g["key"] == key:
            return g
    return None

def _svc_by_key(key: str) -> dict | None:
    for sv in _SVC_LIST:
        if sv["key"] == key:
            return sv
    return None

def _related_block(g: dict) -> str:
    """Three same-family guide links + one contextual service link."""
    esc = site.esc
    items = []
    for k in site.RELATED.get(g["key"], []):
        r = _guide_by_key(k)
        if not r:
            continue
        items.append(
            f'<li><span class="related__tag">{esc(r["tag"])}</span>'
            f'<a href="/learn/{r["key"]}/">{esc(r["title"])}</a></li>')
    if not items:
        return ""
    svc = _svc_by_key(site.GUIDE_SERVICE.get(g["key"], "patios"))
    svc_line = ""
    if svc:
        svc_line = ('<p class="related__svc">See the work: '
                    f'<a href="/services/{svc["key"]}/">{esc(svc["name"])}</a>.</p>')
    return ('<nav class="related" aria-label="More patio guides">'
            '<h2 class="related__h">Keep reading</h2>'
            '<ul class="related__list">' + "".join(items) + '</ul>'
            + svc_line + '</nav>')

def build_guide_one(root: Path, g: dict) -> None:
    trail = [("Home", "/"), ("Learn", "/learn/"), (g["title"], f"/learn/{g['key']}/")]
    body = []
    body.append('<section class="section"><div class="wrap wrap--narrow">')
    body.append(site.crumb_html(trail))
    body.append(f'<header class="section__head"><p class="eyebrow">{site.esc(g["tag"])}</p>'
                f'<h1 class="h2">{site.esc(g["h1"])}</h1></header>')
    body.append(site.page_actions())
    body.append(f'<p class="lede">{site.esc(g["lede"])}</p>')
    for para in g["paras"]:
        body.append(f'<p class="prose">{site.esc(para)}</p>')
    if g.get("bullets"):
        items = []
        for b in g["bullets"]:
            if isinstance(b, (tuple, list)):
                items.append(f'<li><strong>{site.esc(b[0])}</strong> {site.esc(b[1])}</li>')
            else:
                items.append(f'<li>{site.esc(b)}</li>')
        body.append('<ul class="guide__list">' + "".join(items) + "</ul>")
    if g.get("checklist"):
        body.append('<ul class="checklist">'
                    + "".join(f'<li>{site.esc(c)}</li>' for c in g["checklist"])
                    + "</ul>")
    if g.get("note"):
        body.append(f'<p class="prose prose--note">{g["note"]}</p>')
    body.append('<figure class="learn__figure">' + _img(g["img"], g["img_alt"], "(max-width:1024px) 100vw, 900px")
                + f'<figcaption><strong>{site.esc(g["title"])}.</strong></figcaption></figure>')
    body.append(_related_block(g))
    if g.get("cta"):
        body.append('<p><a class="btn btn--solid" href="/#estimate">Ask Bryce a question</a></p>')
    body.append('</div></section>')
    body.append(_cta(trail, "Ready when you are.", "Free estimates in Mansfield and the towns around it."))
    html_str = site.render_shell(
        title=f'{g["title"]} | Bryce\'s Patios',
        desc=g["meta"], url=f'{site.BASE}/learn/{g["key"]}/', trail=trail,
        body="".join(body), ld_extra=[],
        svc_links=_svc_links(), town_links=_town_links(),
    )
    write_page(root, f"learn/{g['key']}/index.html", html_str)

def build_learn_hub(root: Path) -> None:
    trail = [("Home", "/"), ("Learn", "/learn/")]
    cards = []
    for g in site.GUIDES:
        cards.append(f'''<a class="guide guide--link" href="/learn/{g['key']}/">
          <span class="guide__thumb">{_img(g['img'], g['img_alt'], "(max-width:700px) 100vw, 360px", cls="guide__thumb-img")}</span>
          <span class="guide__tag">{site.esc(g['tag'])}</span>
          <h3 class="guide__title">{site.esc(g['title'])}</h3>
          <p>{site.esc(g['lede'])}</p>
          <span class="guide__cta-text">Read the guide &rarr;</span>
        </a>''')
    body = f'''<section class="section"><div class="wrap">
      {site.crumb_html(trail)}
      <header class="section__head section__head--center">
        <p class="eyebrow">Patio guides</p>
        <h1 class="h2">How patio work goes, start to finish.</h1>
        <p class="section__sub">Plain-language answers about bases, drainage, frost and stone, written for homeowners who have never hired a patio contractor before.</p>
      </header>
      {site.page_actions(center=True)}
      <div class="learn__grid">{"".join(cards)}</div>
    </div></section>'''
    body += _cta(trail, "Questions about your yard?", "Ask Bryce directly. No pressure, no sales script.")
    html_str = site.render_shell(
        title="Patio Guides &amp; Answers | Bryce's Patios",
        desc="Plain-language guides to patio bases, drainage, frost and stone choice, written for homeowners in Massachusetts and Rhode Island.",
        url=f"{site.BASE}/learn/", trail=trail, body=body, ld_extra=[],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, "learn/index.html", html_str)

def build_service(root: Path, s: dict) -> None:
    town = "Mansfield"
    trail = [("Home", "/"), ("Services", "/services/"), (s["name"], f"/services/{s['key']}/")]
    faqs = [(q.format(town=town) if "{town}" in q else q,
             a.format(town=town) if "{town}" in a else a) for q, a in s["faq"]]
    body = [f'<section class="section"><div class="wrap wrap--narrow">']
    body.append(site.crumb_html(trail))
    body.append(f'<header class="section__head"><p class="eyebrow">Service</p>'
                f'<h1 class="h2">{site.esc(s["h1"].format(town=town))}</h1></header>')
    body.append(site.page_actions())
    body.append(f'<p class="lede">{site.esc(s["blurb"])}</p>')
    body.append('<ul class="checklist">' + "".join(f'<li>{site.esc(b)}</li>' for b in s["bullets"]) + '</ul>')
    body.append('<figure class="learn__figure">' + _img(s["img"], s["img_alt"], "(max-width:1024px) 100vw, 900px")
                + f'<figcaption><strong>{site.esc(s["name"])}.</strong> Built on a full-depth compacted base.</figcaption></figure>')
    body.append('</div></section>')
    body.append(f'<section class="section"><div class="wrap wrap--narrow">'
                + _sec_head("Common questions", f"{s['name']} questions, answered")
                + _faq_block(faqs) + '</div></section>')
    body.append(_cta(trail, f"Planning {s['short']}?", "Tell Bryce about the yard and get a free estimate."))
    html_str = site.render_shell(
        title=f'{s["name"]} Contractor in Mansfield, MA | Bryce\'s Patios',
        desc=s["meta"].format(town=town), url=f'{site.BASE}/services/{s["key"]}/', trail=trail,
        body="".join(body), ld_extra=[_faq_ld(faqs, f'{site.BASE}/services/{s["key"]}/')],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, f"services/{s['key']}/index.html", html_str)

def build_services_hub(root: Path) -> None:
    trail = [("Home", "/"), ("Services", "/services/")]
    cards = []
    for s in site.SERVICES:
        cards.append(f'''<a class="guide guide--link" href="/services/{s['key']}/">
          <span class="guide__tag">{site.esc(s['name'])}</span>
          <h3 class="guide__title">{site.esc(s['h1'].format(town='Mansfield'))}</h3>
          <p>{site.esc(s['blurb'][:180])}&hellip;</p>
          <span class="guide__cta-text">See {site.esc(s['short'])} &rarr;</span>
        </a>''')
    body = f'''<section class="section"><div class="wrap">
      {site.crumb_html(trail)}
      <header class="section__head section__head--center">
        <p class="eyebrow">Services</p>
        <h1 class="h2">Stone work for the yard, done to last.</h1>
        <p class="section__sub">Patios, walkways, retaining walls and fire pits. Owner-operated out of Mansfield, serving southeastern Massachusetts and Rhode Island.</p>
      </header>
      {site.page_actions(center=True)}
      <div class="learn__grid">{"".join(cards)}</div>
    </div></section>'''
    body += '<section class="section"><div class="wrap wrap--narrow"><figure class="learn__figure">'
    body += _img("project-firepit", "A circular stone fire pit set into a stone patio with seating around it.",
                 "(max-width:1024px) 100vw, 900px")
    body += '<figcaption><strong>Patios, walls, walkways and fire pits.</strong> One crew, one standard of base work, on every job.</figcaption></figure></div></section>'
    body += _cta(trail, "Not sure which you need?", "Tell Bryce what the yard is doing and he'll say straight.")
    html_str = site.render_shell(
        title="Services | Patios, Walkways, Walls &amp; Fire Pits | Bryce's Patios",
        desc="Stone patios, walkways, retaining walls and fire pits installed across southeastern Massachusetts and Rhode Island. Owner-operated, free estimates.",
        url=f"{site.BASE}/services/", trail=trail, body=body, ld_extra=[],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, "services/index.html", html_str)

def build_town(root: Path, t: str) -> None:
    tslug = site.slug(t)
    trail = [("Home", "/"), ("Service Area", "/areas/"), (f"{t}, MA", f"/areas/{tslug}/")]
    svc_rows = []
    for s in site.SERVICES:
        svc_rows.append(f'<li><a href="/areas/{tslug}/{s["key"]}/">{site.esc(s["name"])} in {site.esc(t)}, MA</a></li>')
    body = [f'<section class="section"><div class="wrap wrap--narrow">']
    body.append(site.crumb_html(trail))
    body.append(f'<header class="section__head"><p class="eyebrow">{site.esc(t)}, Massachusetts</p>'
                f'<h1 class="h2">Stone patios &amp; hardscaping in {site.esc(t)}, MA</h1></header>')
    body.append(site.page_actions())
    body.append(f'<p class="lede">Bryce builds patios, walkways, retaining walls and fire pits in {site.esc(t)} and the towns next to it. One crew, one person quoting the job, and it is the same person who builds it.</p>')
    intro = site.TOWN_INTRO.get(t)
    if intro:
        body.append(f'<p class="prose">{site.esc(intro)}</p>')
    body.append(f'<p class="prose">If you are in {site.esc(t)} and want a number, tell us the size, the grade and how you want to use the space. We look at the yard before we quote it, and the estimate is free.</p>')
    town_img = site.TOWN_IMG.get(t, "project-dining")
    body.append('<figure class="learn__figure">'
                + _img(town_img, site.TOWN_IMG_ALT.get(town_img, site.TOWN_IMG_ALT_DEFAULT),
                       "(max-width:1024px) 100vw, 900px")
                + f'<figcaption><strong>Stone work in {site.esc(t)}, MA.</strong> Base, drainage and edge, done in order.</figcaption></figure>')
    body.append('</div></section>')
    body.append(f'<section class="section"><div class="wrap wrap--narrow">'
                + _sec_head("What we build", f"Patio work in {t}")
                + f'<ul class="guide__list">{"".join(svc_rows)}</ul></div></section>')
    body.append(_cta(trail, f"Getting a quote in {t}", "Free estimates, no hard limits on where we go."))
    html_str = site.render_shell(
        title=f'Stone Patios &amp; Hardscaping in {t}, MA | Bryce\'s Patios',
        desc=f'Owner-operated stone patio, walkway, retaining wall and fire pit installation in {t}, MA. Free estimates from Bryce\'s Patios.',
        url=f"{site.BASE}/areas/{tslug}/", trail=trail, body="".join(body), ld_extra=[],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, f"areas/{tslug}/index.html", html_str)

def build_service_town(root: Path, t: str, s: dict) -> None:
    """Service x town page for the six towns that matter most."""
    tslug = site.slug(t)
    trail = [("Home", "/"), ("Service Area", "/areas/"), (f"{t}, MA", f"/areas/{tslug}/"),
             (s["name"], f"/areas/{tslug}/{s['key']}/")]
    faqs = [(q.format(town=t) if "{town}" in q else q,
             a.format(town=t) if "{town}" in a else a) for q, a in s["faq"]]
    body = [f'<section class="section"><div class="wrap wrap--narrow">']
    body.append(site.crumb_html(trail))
    body.append(f'<header class="section__head"><p class="eyebrow">{site.esc(t)}, MA &middot; {site.esc(s["name"])}</p>'
                f'<h1 class="h2">{site.esc(s["h1"].format(town=t))}</h1></header>')
    body.append(site.page_actions())
    body.append(f'<p class="lede">{site.esc(s["blurb"])}</p>')
    body.append(f'<p class="prose">In {site.esc(t)} that usually means {site.esc(_town_note(t))}</p>')
    body.append('<ul class="checklist">' + "".join(f'<li>{site.esc(b)}</li>' for b in s["bullets"]) + '</ul>')
    body.append('<figure class="learn__figure">' + _img(s["img"], s["img_alt"], "(max-width:1024px) 100vw, 900px")
                + f'<figcaption><strong>{site.esc(s["name"])} in {site.esc(t)}.</strong> Base, drainage and edge, done in order.</figcaption></figure>')
    body.append('</div></section>')
    body.append(f'<section class="section"><div class="wrap wrap--narrow">'
                + _sec_head("Common questions", f"{s['name']} in {t}")
                + _faq_block(faqs) + '</div></section>')
    body.append(_cta(trail, f"{s['name']} in {t}", "Free estimate, straight answer."))
    html_str = site.render_shell(
        title=f'{s["name"]} in {t}, MA | Bryce\'s Patios',
        desc=f'{s["name"]} installed in {t}, MA on a full-depth compacted base. Owner-operated, free estimates from Bryce\'s Patios.',
        url=f"{site.BASE}/areas/{tslug}/{s['key']}/", trail=trail, body="".join(body),
        ld_extra=[_faq_ld(faqs, f"{site.BASE}/areas/{tslug}/{s['key']}/")],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, f"areas/{tslug}/{s['key']}/index.html", html_str)

def _town_note(t: str) -> str:
    notes = {
        "Mansfield": "grade that falls toward the house, and a base dug to the 30-inch frost line so nothing lifts in March.",
        "Foxborough": "flat lots and heavy spring water, so the slope that sends water away is planned before any stone goes down.",
        "Attleboro": "older yards with mixed grades, so we work out where the water leaves before we set the first paver.",
        "North Attleboro": "sloped yards that want steps and a seat wall, built so the transitions read as deliberate.",
        "Norton": "larger lots and drainage that has to cross the yard, so the path and patio drain together.",
        "Franklin": "deeper frost and wet springs, so depth and compaction decide whether it is flat in ten years.",
    }
    return notes.get(t, "the same discipline as everywhere: dig to depth, compact in lifts, and plan the water.")

def build_areas_hub(root: Path) -> None:
    trail = [("Home", "/"), ("Service Area", "/areas/")]
    ma = "".join(f'<li><a href="/areas/{site.slug(t)}/">Stone patios in {site.esc(t)}, MA</a></li>' for t in site.TOWNS_MA)
    ri = "".join(f'<li><span>{site.esc(t)}, RI (call for availability)</span></li>' for t in site.TOWNS_RI)
    body = f'''<section class="section"><div class="wrap">
      {site.crumb_html(trail)}
      <header class="section__head section__head--center">
        <p class="eyebrow">Service area</p>
        <h1 class="h2">Where Bryce builds.</h1>
        <p class="section__sub">Based at 885 West St in Mansfield, MA and working across southeastern Massachusetts and Rhode Island. Pick your town for local detail, or just call.</p>
      </header>
      {site.page_actions(center=True)}
      <div class="area__grid">
        <div class="area__intro">
          <h2 class="h2">Towns we work in</h2>
          <p>Twelve Massachusetts towns we are in most often, all within a short drive of the Mansfield yard. Rhode Island is on the list too, just call first.</p>
        </div>
        <div class="area__lists">
          <div class="area__col"><h3 class="area__state">Massachusetts</h3><ul class="area__towns">{ma}</ul></div>
          <div class="area__col"><h3 class="area__state">Rhode Island</h3><ul class="area__towns">{ri}</ul></div>
        </div>
      </div>
    </div></section>'''
    body += ('<section class="section"><div class="wrap wrap--narrow"><figure class="learn__figure">'
             + _img("big-yard", "A curved stone patio tying a large yard together.",
                    "(max-width:1024px) 100vw, 900px")
             + '<figcaption><strong>Southeastern Massachusetts &amp; Rhode Island.</strong> Most of the work sits within a short drive of the Mansfield yard.</figcaption></figure></div></section>')
    body += _cta(trail, "Somewhere else in the area?", "Bryce has no hard limits. Call and ask.")
    html_str = site.render_shell(
        title="Service Area | Southeastern MA &amp; Rhode Island | Bryce's Patios",
        desc="Bryce's Patios builds stone patios, walkways, walls and fire pits across southeastern Massachusetts and Rhode Island. See the towns we cover.",
        url=f"{site.BASE}/areas/", trail=trail, body=body, ld_extra=[],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, "areas/index.html", html_str)

def build_sitemap(root: Path) -> None:
    urls = [f"{site.BASE}/", f"{site.BASE}/learn/", f"{site.BASE}/services/", f"{site.BASE}/areas/"]
    urls += [f"{site.BASE}/learn/{g['key']}/" for g in site.GUIDES]
    urls += [f"{site.BASE}/services/{s['key']}/" for s in site.SERVICES]
    urls += [f"{site.BASE}/areas/{site.slug(t)}/" for t in site.TOWNS_MA]
    for t in site.TOP_TOWNS:
        urls += [f"{site.BASE}/areas/{site.slug(t)}/{s['key']}/" for s in site.SERVICES]
    today = _dt.date.today().isoformat()

    # page -> hero image filename (for the Google image sitemap extension)
    img_for = {
        f"{site.BASE}/": ("project-firepit", "Stone patio with a fire pit built by Bryce's Patios in Mansfield, MA"),
        f"{site.BASE}/services/": ("project-firepit", "Stone patios, walls, walkways and fire pits by Bryce's Patios"),
        f"{site.BASE}/areas/": ("big-yard", "Stone patio work across southeastern Massachusetts and Rhode Island"),
        f"{site.BASE}/learn/": ("craft-base", "Patio base and craft guides from Bryce's Patios"),
    }
    for t in site.TOWNS_MA:
        nm = site.TOWN_IMG.get(t, "project-dining")
        img_for[f"{site.BASE}/areas/{site.slug(t)}/"] = (
            nm, "Stone patio work in " + t + ", MA by Bryce's Patios")
    for g in site.GUIDES:
        img_for[f"{site.BASE}/learn/{g['key']}/"] = (g["img"], g["img_alt"])
    for s in site.SERVICES:
        img_for[f"{site.BASE}/services/{s['key']}/"] = (s["img"], s["img_alt"])
    for t in site.TOP_TOWNS:
        tsl = site.slug(t)
        for s in site.SERVICES:
            img_for[f"{site.BASE}/areas/{tsl}/{s['key']}/"] = (
                s["img"], f'{s["name"]} in {t}, MA by Bryce\'s Patios')

    rows = []
    for u in urls:
        rel = u.replace(site.BASE + "/", "").rstrip("/")
        f = root / (rel + "/index.html" if rel else "index.html")
        if not f.exists():
            f = root / rel if rel else root / "index.html"
        lm = _dt.date.fromtimestamp(f.stat().st_mtime).isoformat() if f.exists() else today
        pri = "1.0" if u == f"{site.BASE}/" else ("0.8" if rel.count("/") == 0 else "0.6")
        row = f'  <url><loc>{u}</loc><lastmod>{lm}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority>'
        if u in img_for:
            name, title = img_for[u]
            row += (f'<image:image><image:loc>{site.BASE}/assets/img/{name}.jpg</image:loc>'
                    f'<image:title>{site.esc(title)}</image:title></image:image>')
        row += '</url>'
        rows.append(row)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    (root / "sitemap.xml").write_text(xml, encoding="utf-8")
    return len(urls)

def _page_date(root: Path, rel_html: str) -> str:
    f = root / rel_html
    d = _dt.date.fromtimestamp(f.stat().st_mtime) if f.exists() else _dt.date.today()
    return d.isoformat() + "T09:00:00-04:00"

def build_feed(root: Path) -> int:
    """Atom feed of the guides hub plus every guide page, newest first."""
    esc = site.esc
    entries = []
    hub_rel = "learn/index.html"
    ordered = [("learn/index.html", None)] + [(f"learn/{g['key']}/index.html", g) for g in site.GUIDES]
    dated = []
    for rel, g in ordered:
        url = f"{site.BASE}/learn/" if g is None else f"{site.BASE}/learn/{g['key']}/"
        title = "Patio guides and answers" if g is None else g["title"]
        summary = ("Plain-language guides to patio bases, drainage, frost and stone choice." if g is None
                   else g["lede"])
        dated.append((_page_date(root, rel), url, title, summary, rel))
    dated.sort(key=lambda r: r[0], reverse=True)
    updated = dated[0][0] if dated else _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-04:00")
    for iso, url, title, summary, rel in dated:
        entries.append(
            "  <entry>\n"
            f"    <title>{esc(title)}</title>\n"
            f'    <link href="{url}"/>\n'
            f'    <id>{url}</id>\n'
            f"    <updated>{iso}</updated>\n"
            f"    <summary>{esc(summary)}</summary>\n"
            "  </entry>"
        )
    xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<feed xmlns="http://www.w3.org/2005/Atom">\n'
           "  <title>Bryce's Patios: patio guides</title>\n"
           f'  <link href="{site.BASE}/feed.xml" rel="self"/>\n'
           f'  <link href="{site.BASE}/learn/"/>\n'
           f'  <id>{site.BASE}/learn/</id>\n'
           f"  <updated>{updated}</updated>\n"
           "  <author><name>Bryce's Patios</name>"
           f'<uri>{site.BASE}/</uri></author>\n'
           "  <rights>Bryce's Patios</rights>\n"
           + "\n".join(entries) + "\n</feed>\n")
    (root / "feed.xml").write_text(xml, encoding="utf-8")
    return len(dated)

def main() -> None:
    root = Path(__file__).resolve().parents[2]
    n = 0
    build_learn_hub(root); n += 1
    for g in _GUIDE_LIST:
        build_guide_one(root, g); n += 1
    build_services_hub(root); n += 1
    for s in _SVC_LIST:
        build_service(root, s); n += 1
    build_areas_hub(root); n += 1
    for t in _MA:
        build_town(root, t); n += 1
    for t in _TOP:
        for s in _SVC_LIST:
            build_service_town(root, t, s); n += 1
    total = build_sitemap(root)
    nfeed = build_feed(root)
    print(f"wrote {n} pages, sitemap has {total} urls, feed has {nfeed} entries")


if __name__ == "__main__":
    main()
