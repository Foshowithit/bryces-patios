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
    body += ('<section class="section"><div class="wrap wrap--narrow">'
             '<h2 class="h2">Start here if you have never hired patio work</h2>'
             '<p class="prose">Most people find this site with the same question: why is one quote so much lower '
             'than another for the same patio? The answer is almost never the stone. It is how deep the '
             'contractor plans to dig, how the base gets compacted, and where the water goes. The guides below '
             'explain each of those in plain words, with no sales spin, so you can tell a real quote from a '
             'thin one.</p>'
             '<p class="prose">The base guide is the one to read first, because nine-tenths of a patio is '
             'underground. The drainage guide explains why patios sink and walls lean. The frost guide covers '
             'the 30-inch depth this part of Massachusetts is built to. From there the cost guide breaks down '
             'what actually moves a price, and the quote guide tells you what a good estimate should include.</p>'
             '<p class="prose">You do not need to read all of these before calling. If you would rather just '
             'talk it through, call Bryce and describe the yard. He will tell you what he needs to see and '
             'give you a straight answer without a pitch.</p>'
             '</div></section>')
    body += _cta(trail, "Questions about your yard?", "Ask Bryce directly. No pressure, no sales script.")
    html_str = site.render_shell(
        title="Patio Guides and Answers | Bryce's Patios",
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
    for para in s.get("prose", []):
        body.append(f'<p class="prose">{site.esc(para)}</p>')
    body.append('<ul class="checklist">' + "".join(f'<li>{site.esc(b)}</li>' for b in s["bullets"]) + '</ul>')
    body.append('<figure class="learn__figure">' + _img(s["img"], s["img_alt"], "(max-width:1024px) 100vw, 900px")
                + f'<figcaption><strong>{site.esc(s["name"])}.</strong> Built on a full-depth compacted base.</figcaption></figure>')
    body.append('</div></section>')
    body.append(f'<section class="section"><div class="wrap wrap--narrow">'
                + _sec_head("Common questions", f"{s['name']} questions, answered")
                + _faq_block(faqs) + '</div></section>')
    body.append(_cta(trail, f"Planning {s['short']}?", "Tell Bryce about the yard and get a free estimate."))
    html_str = site.render_shell(
        title=f'{s["name"]} in Mansfield, MA | Bryce\'s Patios',
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
    body += ('<section class="section"><div class="wrap wrap--narrow">'
             '<h2 class="h2">Four kinds of work, one standard underneath</h2>'
             '<p class="prose">Every job on this page is built the same way underneath. The ground is dug to '
             'depth, the base goes in as crushed stone compacted in lifts, the surface is set to shed water '
             'away from the house, and the edge is restrained so the field cannot spread. That last inch you '
             'see is the cheap part. The work under it is what keeps the surface flat after five winters of '
             'freeze and thaw.</p>'
             '<p class="prose">A patio is the floor of the yard and takes the most square footage, so the '
             'layout and the drainage get the most thought. A walkway takes more traffic per square foot and '
             'usually sits where water already wants to run, so it gets the same base in a narrower trench. A '
             'retaining wall holds back the weight of wet soil, which makes the base course, the drainage '
             'behind it and the compaction the whole job. A fire pit is built into the patio layout from the '
             'start, because one dropped onto a finished patio almost never sits right.</p>'
             '<p class="prose">The stone you pick is the part that is easiest to change and the part that '
             'moves the price most. Paver is the friendliest budget, bluestone and flagstone climb from '
             'there. We pick the material with you after we have looked at the yard, because the right choice '
             'depends on the slope, the traffic and how you want it to age.</p>'
             '<p class="prose">Prices here are per job, not per square foot, because two patios the same size '
             'can be different work. Grade, access and how much digging the base needs all move the number. '
             'Send a couple of photos with the size and the grade and you will get a straight answer on '
             'whether a visit is worth it.</p>'
             '</div></section>')
    body += '<section class="section"><div class="wrap wrap--narrow"><figure class="learn__figure">'
    body += _img("project-firepit", "A circular stone fire pit set into a stone patio with seating around it.",
                 "(max-width:1024px) 100vw, 900px")
    body += '<figcaption><strong>Patios, walls, walkways and fire pits.</strong> One crew, one standard of base work, on every job.</figcaption></figure></div></section>'
    body += _cta(trail, "Not sure which you need?", "Tell Bryce what the yard is doing and he'll say straight.")
    html_str = site.render_shell(
        title="Services | Patios, Walkways, Walls, Fire Pits | Bryce's Patios",
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
    detail = getattr(site, "TOWN_DETAIL", {}).get(t)
    if detail:
        for para in detail:
            body.append(f'<p class="prose">{site.esc(para)}</p>')
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
        title=f'Stone Patios in {t}, MA | Bryce\'s Patios',
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
    detail = _svc_town_detail(s["key"], t)
    if detail:
        body.append(f'<p class="prose">{site.esc(detail)}</p>')
    watch = _svc_watch(s["key"], t)
    if watch:
        body.append(f'<p class="prose">{site.esc(watch)}</p>')
    checks = list(s["bullets"])
    if detail:
        checks.append(f"Worked to {site.esc(t)}'s grade and drainage, not a cookie-cutter layout")
    body.append('<ul class="checklist">' + "".join(f'<li>{site.esc(b)}</li>' for b in checks) + '</ul>')
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
        "Mansfield": "grade that falls toward the house, and a base dug to the 30-inch frost line so nothing lifts in March. The lots run from flat to a foot of fall in twenty, so the slope is read before any stone is set.",
        "Foxborough": "flat lots and heavy spring water, so the slope that sends water away is planned before any stone goes down. Without that, spring thaw sits on the patio instead of running off it.",
        "Attleboro": "older yards with mixed grades, so we work out where the water leaves before we set the first paver. Many of these lots were built up over time, and the high and low spots move around.",
        "North Attleboro": "sloped yards that want steps and a seat wall, built so the transitions read as deliberate instead of like an afterthought. The fall also decides where a fire pit can sit on its own level.",
        "Norton": "larger lots and drainage that has to cross the yard, so the path and patio drain together instead of fighting each other. Long runs need a low point designed in, not discovered after a storm.",
        "Franklin": "deeper frost and wet springs, so depth and compaction decide whether it is flat in ten years. Wet ground also means the base has to be built dry, which changes the schedule.",
        "Seekonk": "smaller yards close to the Rhode Island line, so the layout gets planned tight and the water still has to leave the property cleanly.",
        "Rehoboth": "open, sandy lots that drain fast on their own, which lets a patio sit a little differently but still needs the base dug to depth and compacted in lifts.",
        "Plainville": "winding, tree-heavy yards where root zones and shade change how the base is prepped and how long a stone surface stays wet.",
        "Taunton": "larger yards on mixed soil, so the layout usually follows the existing grade and the drainage is set before the shape is drawn.",
        "Easton": "mature, established neighborhoods with lots of mature plantings, so access and root protection guide where equipment can go.",
        "Sharon": "hilly, wooded lots where the fall is steep enough that steps and a retaining edge come first and the patio shape second.",
    }
    return notes.get(t, "the same discipline as everywhere: dig to depth, compact in lifts, and plan the water.")

# Per-service, per-town second paragraph for the service x town pages.
SVC_TOWN_DETAIL = {
    "patios": {
        "Mansfield": "Most Mansfield patios get laid out off the back door and run toward the low corner of the lot, which keeps the walkout clear and gives the water a direction.",
        "Foxborough": "On the flat lots here the patio usually wants a slight crown away from the house, and on the wet ones the first week is often drainage before any stone.",
        "Attleboro": "Older Attleboro yards mean we sometimes re-grade before we lay anything, so the patio sits at a height that still meets the door threshold.",
        "North Attleboro": "The slope here usually earns a set of steps and a seat wall keeping the main field level, so the patio reads as one room instead of three.",
        "Norton": "With bigger lots, the patio is often set back nearer the tree line, and the path out to it drains with the same low point.",
        "Franklin": "Franklin patios get a base beyond the frost line and a start date that respects how late the ground stays wet in spring.",
    },
    "walkways": {
        "Mansfield": "A Mansfield walkway usually runs front door to drive or front door to patio, and it gets the same base as the patio underneath so it does not dip at the joints.",
        "Foxborough": "Walkways on flat Foxborough lots need positive fall or they puddle, so the grade is set on the walk even when the yard looks level. On flat Foxborough lots the fall on a walk has to be built in on purpose, so the runs are set to shed even when the yard reads level to the eye.",
        "Attleboro": "In older Attleboro yards the path often steps down with the grade rather than cutting through it, which protects tree roots and looks settled.",
        "North Attleboro": "Sloped North Attleboro entries get stone steps set into the run instead of a ramp, so the walk stays comfortable and drains at each tread.",
        "Norton": "Longer Norton runs get a gentle switch and a low point at the drive so the whole path sheds instead of holding water mid-run.",
        "Franklin": "Franklin walkways are set on a deeper base where the frost moves hard, and landings are placed to catch drift before the door. Franklin walks also get a wider base trench than the frost alone would demand, because the wet spring ground needs to drain as well as hold.",
    },
    "retaining-walls": {
        "Mansfield": "Mansfield walls are usually holding back a grade that falls toward the house, so the wall doubles as the edge of the patio above it. In Mansfield a wall often doubles as the seat wall at the edge of the patio, so the base course and the cap are set together with the patio, not after it.",
        "Foxborough": "Where a Foxborough lot is flat but wet, the wall is often a low seat wall tying the patio together rather than a tall structural one. Where the lot is flat and wet instead of sloped, a Foxborough wall is more often a low border that ties the patio together than a structural face holding real grade.",
        "Attleboro": "Older Attleboro grades shift, so a wall is set on its own footing and drainage behind it is designed before the face goes up.",
        "North Attleboro": "North Attleboro walls carry the slope, so they get a compacted gravel backfill, drain stone and a weep path out toward the low corner. North Attleboro walls carry real slope, so the drain stone behind the face and the weep path out to the low corner get designed before the first block is set.",
        "Norton": "Bigger Norton yards sometimes need a terrace wall to keep the patio level while the lawn steps down toward the tree line. Norton's bigger yards often want a low terrace wall to keep the patio level while the lawn steps down, rather than a single tall face taking the whole drop.",
        "Franklin": "Franklin's deeper frost means wall footings are dug past it, so the face stays plumb after a hard winter. Franklin also has stretches of flat new-build yard where a low seat wall is the better answer than a tall one, because there is no real grade to hold back, only a change of level.",
    },
    "fire-pits": {
        "Mansfield": "A Mansfield fire pit usually sits on its own level pad off the patio, far enough from the house for a real fire and near enough to share the seating. Most Mansfield yards have the room for that pad off the patio edge, so the pit ends up where the seating already wants to be rather than out in the open lawn.",
        "Foxborough": "On wet Foxborough lots the pit goes on ground that drains, which sometimes decides the corner before the design does. On the wetter Foxborough lots we also set the pit on a raised compacted base so spring water drains under it rather than sitting in the ring. If the grade will not let us raise it, we dig a dry well beside the ring and run the base stone out to it so the pit never sits in a puddle.",
        "Attleboro": "Older Attleboro yards often fit the pit into an existing corner so it needs the least new grade and the least new stone. Attleboro's older yards often already have a level corner worn into the lawn, which is usually the cheapest place to set a pit because it needs the least new grade.",
        "North Attleboro": "Sloped North Attleboro yards get the pit on a built terrace, so it sits flat and the seating rings it evenly. On a sloped North Attleboro yard the pit sits on its own built terrace, which means the base under it is graded and compacted the same way as the patio above.",
        "Norton": "With room to work, Norton pits often get a wider ring of seating and a gravel apron so the area stays off the lawn. On a big Norton lot the pit usually gets a wider gravel apron and more seating, since there is room and the area then stays off the lawn through the wet months.",
        "Franklin": "Franklin pits use a stone ring set on a compacted base, so frost does not tip the course out of level over winter. Franklin's deeper frost also decides how the pit ring is footed, since a shallow ring will lift and tip one course at a time over a few hard winters.",
    },
}

def _svc_town_detail(svc_key: str, t: str) -> str:
    return SVC_TOWN_DETAIL.get(svc_key, {}).get(t, "")

# Per-service closing paragraph: what we watch for, worded for each service and
# lightly varied by town so the copy stays specific instead of template-filler.
_SVC_WATCH = {
    "patios": (
        "For a patio in {t} the things that decide the result are boring ones: how deep the base is dug, "
        "whether it is compacted in lifts, where the surface sheds to, and how the edge is held. Get those "
        "right and the pavers you picked at the yard will look the same in ten winters. Get them wrong and "
        "no amount of pretty stone will keep the field flat.",
        "Every patio quote that comes in low usually skipped one of the four: depth, compaction, slope or edge. "
        "In {t} the grade and the frost line make all four matter, so we walk the yard, set the fall away from "
        "the house, and build the base before a single paver is set.",
    ),
    "walkways": (
        "A walkway in {t} fails at the joints before it fails anywhere else, and the joints fail when the base "
        "under them was not dug and compacted the same way the patio was. Laid that way, the path stays even "
        "through the freeze and thaw cycles and does not dip where two runs meet.",
        "The other thing that makes a walk look right is the fall. In {t} we set a positive slope on the run "
        "and a low point at the drive or the lawn so water leaves instead of sitting on the surface after a storm.",
    ),
    "retaining-walls": (
        "A retaining wall in {t} is mostly the part you never see: a footing dug past the frost line, gravel "
        "backfill that drains, and a path for that water to escape at the bottom. The face is the easy part. "
        "A wall that holds water behind it will lean within a few seasons.",
        "In {t} that means sizing the wall to the grade it is actually holding, not just the height that looks "
        "right from the deck, and letting drainage decide how far the base extends behind the face.",
    ),
    "fire-pits": (
        "A fire pit in {t} wants its own level pad and a clear ring around it, so the seating sits flat and "
        "the heat has somewhere to go. Building it into the patio layout from the start is cheaper and looks "
        "better than dropping one onto finished stone later.",
        "The pad under a fire pit in {t} gets the same treatment as the patio: dug, compacted and set on a base "
        "that does not heave, so the stone ring stays level rather than tipping after the first hard winter.",
    ),
}

def _svc_watch(svc_key: str, t: str) -> str:
    opts = _SVC_WATCH.get(svc_key)
    if not opts:
        return ""
    # deterministic pick so rebuilds are stable, town-varied so pages differ
    return opts[sum(map(ord, t)) % len(opts)].format(t=t)


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
    body += ('<section class="section"><div class="wrap wrap--narrow">'
             '<h2 class="h2">How far we go, and what changes town to town</h2>'
             '<p class="prose">Mansfield is home base, so the towns closest to the shop are the ones we are in '
             'most weeks. Foxborough, Norton and Attleboro are a short run down 495 or 140. North Attleboro, '
             'Franklin and Taunton sit a few minutes further out. Nothing on the list is a long drive, and the '
             'same person who quotes the job is the one who shows up to build it.</p>'
             '<p class="prose">What changes from town to town is not the crew, it is the ground. Mansfield and '
             'Norton yards tend flat, so the drainage gets designed into the patio and the yard carries water '
             'around the stone instead of through it. Attleboro and Sharon lots run to ledge and slope, where '
             'the work turns into steps, landings and a wall, and the base has to hold back fill on the high '
             'side. Easton and Franklin yards sit wetter in spring and closer to woods, so drainage and base '
             'depth get worked out before anything is dug.</p>'
             '<p class="prose">Rhode Island is a short drive over the line and Bryce takes those jobs too. We '
             'do not carry a Rhode Island registration, so for work there it is best to call first and sort '
             'out what your town requires before the job is booked. Everything in Massachusetts is built to '
             'the same 30-inch frost depth, because a base that skips it will heave no matter how good the '
             'stone looks.</p>'
             '<p class="prose">If your town is not on the list, that does not mean no. There are no hard '
             'limits on how far out the work goes. Call with the address and Bryce will tell you straight '
             'whether it makes sense for both sides.</p>'
             '</div></section>')
    body += ('<section class="section"><div class="wrap wrap--narrow"><figure class="learn__figure">'
             + _img("big-yard", "A curved stone patio tying a large yard together.",
                    "(max-width:1024px) 100vw, 900px")
             + '<figcaption><strong>Southeastern Massachusetts &amp; Rhode Island.</strong> Most of the work sits within a short drive of the Mansfield yard.</figcaption></figure></div></section>')
    body += _cta(trail, "Somewhere else in the area?", "Bryce has no hard limits. Call and ask.")
    html_str = site.render_shell(
        title="Service Area | Southeastern MA | Bryce's Patios",
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
    print(f"wrote {n+1} pages, sitemap has {total} urls, feed has {nfeed} entries")


if __name__ == "__main__":
    main()
