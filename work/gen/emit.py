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
# Services that get a page in every town. The seasonal/site-work additions are
# single pages: a brush-clearing page for each of twelve towns would be twelve
# pages of the same paragraph, which is the kind of thing a copy gate exists to
# catch and a visitor can smell.
_TOWN_SVC = [s for s in _SVC_LIST if s.get("town_pages", True)]
_MA = site.TOWNS_MA
# SERVICE x TOWN coverage: build the full 12-town MA matrix, not just the
# original 6 top towns. site.TOP_TOWNS is kept for reference/other use.
_TOP = site.TOWNS_MA

# ── shared bits ────────────────────────────────────────────────────────────
# Intrinsic dimensions of each full-size JPG, read from the files themselves.
# A hand-maintained copy of this table drifted from the actual assets (eight
# entries wrong after a recrop), which emitted width/height attributes that did
# not match the image and made every page shift as it loaded.
_ROOT = Path(__file__).resolve().parents[2]


def _jpeg_size(path: Path) -> tuple[int, int]:
    """Width and height from a JPEG's first SOFn marker. No dependencies."""
    with path.open("rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            raise ValueError(f"{path.name} is not a JPEG")
        while True:
            byte = fh.read(1)
            if not byte:
                raise ValueError(f"{path.name} has no frame header")
            if byte != b"\xff":
                continue
            marker = fh.read(1)
            while marker == b"\xff":
                marker = fh.read(1)
            if not marker:
                raise ValueError(f"{path.name} has no frame header")
            code = marker[0]
            if code in (0xD8, 0x01) or 0xD0 <= code <= 0xD7:
                continue
            length_raw = fh.read(2)
            if len(length_raw) < 2:
                raise ValueError(f"{path.name} truncated")
            length = int.from_bytes(length_raw, "big")
            if code in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                fh.seek(1, 1)  # sample precision byte, then height, then width
                h, w = int.from_bytes(fh.read(2), "big"), int.from_bytes(fh.read(2), "big")
                return w, h
            fh.seek(length - 2, 1)


IMG_DIMS = {
    p.stem: _jpeg_size(p)
    for p in sorted((_ROOT / "assets" / "img").glob("*.jpg"))
    if not p.stem.endswith("-900")
}

# Widths a companion file may carry: <stem>-<w>.jpg beside <stem>.jpg. A frame
# that was recomposed on export (see tools/grade-photos.py CROP) lands at its
# native width instead of 1600, so the widest candidate is the file itself and
# every narrower companion that actually exists is offered to the browser. A
# srcset entry that names a file we do not ship is a broken image, not a nicety.
_TIER_WIDTHS = (640, 900, 1200)


def _variants(name: str, w: int) -> list[tuple[int, str]]:
    out = [(w, f"/assets/img/{name}.jpg")]
    for tw in _TIER_WIDTHS:
        p = (_ROOT / "assets" / "img" / f"{name}-{tw}.jpg")
        if p.exists() and tw < w:
            out.append((tw, f"/assets/img/{name}-{tw}.jpg"))
    return sorted(out)


def _img(name: str, alt: str, sizes: str, *, cls: str = "", loading="lazy") -> str:
    esc = site.esc
    w, h = IMG_DIMS[name]
    c = f' class="{cls}"' if cls else ""
    srcset = ", ".join(f"{url} {iw}w" for iw, url in _variants(name, w))
    return (
        f'<img{c} src="/assets/img/{name}.jpg" '
        f'srcset="{srcset}" '
        f'sizes="{sizes}" width="{w}" height="{h}" loading="{loading}" decoding="async" '
        f'alt="{esc(alt)}">'
    )

def _video_block(src: str, poster: str, caption: str, label: str) -> str:
    """A silent, captioned first-party video on a page. No audio, so it autoplays
    muted everywhere and stays readable with the sound off."""
    esc = site.esc
    return (
        f'<figure class="learn__figure learn__figure--video">'
        f'<video class="learn__video" src="/assets/video/{src}" poster="/assets/img/{poster}.jpg" '
        f'controls muted playsinline preload="none" width="1600" height="900" '
        f'aria-label="{esc(label)}"></video>'
        f'<figcaption>{esc(caption)}</figcaption></figure>'
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

def _video_ld(g: dict, url: str) -> dict:
    v = g["video"]
    return {
        "@type": "VideoObject",
        "@id": url + "#video",
        "name": f'{g["title"]}: Bryce\'s Patios',
        "description": v["label"],
        "thumbnailUrl": [f'{site.BASE}/assets/img/{v["poster"]}.jpg'],
        "contentUrl": f'{site.BASE}/assets/video/{v["src"]}',
        "embedUrl": url,
        "duration": "PT23S",
        "inLanguage": "en-US",
        "isFamilyFriendly": True,
        "publisher": {"@id": f'{site.BASE}/#business'},
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
        <a class="btn btn--solid" href="/#estimate">Bryce</a>
        <a class="btn btn--quiet" href="tel:{PHONE_TEL}">Call Bryce</a>
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

def _svc_town_links(s: dict) -> str:
    """Service x town links for a service page, only where those pages exist."""
    if not s.get("town_pages", True):
        return ""
    esc = site.esc
    items = "".join(
        f'<li><a href="/areas/{site.slug(t)}/{s["key"]}/">{esc(s["name"])} in {esc(t)}</a></li>'
        for t in _TOP)
    return ('<nav class="related" aria-label="Where we build this">'
            '<h2 class="related__h">Where we build this</h2>'
            '<ul class="related__list">' + items + '</ul>'
            '<p class="related__svc">Not seeing your town? '
            '<a href="/areas/">See every area we cover</a>.</p></nav>')

def _svc_guide_links(s: dict) -> str:
    """Guides whose subject is this service, as links from a service page."""
    esc = site.esc
    keys = [k for k, v in site.GUIDE_SERVICE.items() if v == s["key"]]
    items = []
    for k in keys:
        g = _guide_by_key(k)
        if not g:
            continue
        items.append(
            f'<li><span class="related__tag">{esc(g["tag"])}</span>'
            f'<a href="/learn/{g["key"]}/">{esc(g["title"])}</a></li>')
    if not items:
        return ""
    return ('<nav class="related" aria-label="Guides about this work">'
            '<h2 class="related__h">Read this first</h2>'
            '<ul class="related__list">' + "".join(items) + "</ul></nav>")

def _sibling_svc_links(s: dict) -> str:
    """Links to the other three services from a service page."""
    esc = site.esc
    items = "".join(
        f'<li><a href="/services/{o["key"]}/">{esc(o["name"])}</a></li>'
        for o in _SVC_LIST if o["key"] != s["key"])
    return ('<nav class="related" aria-label="Other services">'
            '<h2 class="related__h">Other work we do</h2>'
            '<ul class="related__list">' + items + '</ul></nav>')

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
    if g.get("video"):
        v = g["video"]
        body.append(_video_block(v["src"], v["poster"], v["caption"], v["label"]))
    body.append(_related_block(g))
    body.append('</div></section>')
    faqs = site.FAQS_GUIDE[g["key"]]
    body.append('<section class="section"><div class="wrap wrap--narrow">'
                + _sec_head("Common questions", f"{g['title']} questions, answered")
                + _faq_block(faqs) + '</div></section>')
    if g.get("cta"):
        body.append('<section class="section"><div class="wrap wrap--narrow">'
                    '<p><a class="btn btn--solid" href="/#estimate">Ask Bryce a question</a></p>'
                    '</div></section>')
    body.append(_cta(trail, "Ready when you are.", "Free estimates in Mansfield and the towns around it."))
    html_str = site.render_shell(
        title=f'{g["title"]} | Bryce\'s Patios',
        desc=g["meta"], url=f'{site.BASE}/learn/{g["key"]}/', trail=trail,
        body="".join(body), ld_extra=(
            [_faq_ld(faqs, f'{site.BASE}/learn/{g["key"]}/')]
            + ([_video_ld(g, f'{site.BASE}/learn/{g["key"]}/')] if g.get("video") else [])
        ),
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
             'the depth this part of Massachusetts is built to. From there the cost guide breaks down '
             'what actually moves a price, and the quote guide tells you what a good estimate should include.</p>'
             '</div></section>')
    body += ('<section class="section"><div class="wrap wrap--narrow">'
             + _sec_head("Common questions", "Patio questions, answered")
             + _faq_block(site.FAQS_HUB["learn"]) + '</div></section>')
    body += _cta(trail, "Questions about your yard?", "Ask Bryce directly. No pressure, no sales script.")
    html_str = site.render_shell(
        title="Patio Guides and Answers | Bryce's Patios",
        desc="Plain-language guides to patio bases, drainage, frost and stone choice, written for homeowners in Massachusetts.",
        url=f"{site.BASE}/learn/", trail=trail, body=body,
        ld_extra=[_faq_ld(site.FAQS_HUB["learn"], f"{site.BASE}/learn/")],
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
    if s.get("img"):
        cap = s.get("fig_caption") or f'Built on a full-depth compacted base.'
        body.append('<figure class="learn__figure">' + _img(s["img"], s["img_alt"], "(max-width:1024px) 100vw, 900px")
                    + f'<figcaption><strong>{site.esc(s["name"])}.</strong> {site.esc(cap)}</figcaption></figure>')
    if s.get("video"):
        v = s["video"]
        body.append(_video_block(v["src"], v["poster"], v["caption"], v["label"]))
    body.append('</div></section>')
    body.append(f'<section class="section"><div class="wrap wrap--narrow">'
                + _sec_head("Common questions", f"{s['name']} questions, answered")
                + _faq_block(faqs) + '</div></section>')
    body.append(f'<section class="section"><div class="wrap wrap--narrow">'
                + _svc_town_links(s) + _sibling_svc_links(s) + _svc_guide_links(s) + '</div></section>')
    body.append(_cta(trail, f"Planning {s['short']}?", "Tell Bryce about the yard and get a free estimate."))
    html_str = site.render_shell(
        title=s["title"],
        desc=s["meta"].format(town=town), url=f'{site.BASE}/services/{s["key"]}/', trail=trail,
        body="".join(body), ld_extra=(
            [_faq_ld(faqs, f'{site.BASE}/services/{s["key"]}/')]
            + ([_video_ld({"title": s["name"], "video": s["video"]}, f'{site.BASE}/services/{s["key"]}/')]
               if s.get("video") else [])
        ),
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
        <p class="section__sub">Stone patios, walkways, retaining walls and fire pits, plus the grading, clearing and winter work that goes around them. Owner-operated out of Mansfield, serving southeastern Massachusetts.</p>
      </header>
      {site.page_actions(center=True)}
      <div class="learn__grid">{"".join(cards)}</div>
    </div></section>'''
    body += ('<section class="section"><div class="wrap wrap--narrow">'
             '<h2 class="h2">Seven kinds of work, one standard underneath</h2>'
             '<p class="prose">Every job on this page is built the same way underneath. The ground is dug to '
             'depth, the base goes in as crushed stone compacted in lifts, the surface is set to shed water '
             'away from the house, and the edge is restrained so the field cannot spread. The pavers you see '
             'are only the top layer. The work under them is what keeps the surface from shifting through '
             'the freeze and thaw.</p>'
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
             '<p class="prose">The other three kinds of work are the ones that come before and after the '
             'stone. Grading sets the fall so water leaves the house and the low corner, and it happens on '
             'almost every job - it is the least visible part of any of them. Land clearing takes the brush '
             'and saplings out so there is a yard to build in, and gets the roots out before anything goes on '
             'top of them. Snow plowing is the same driveways and walks in the other half of the year, '
             'cleared by the person who built them.</p>'
             '<p class="prose">Prices here are per job, not per square foot, because two patios the same size '
             'can be different work. Grade, access and how much digging the base needs all move the number. '
             'Send a couple of photos with the size and the grade and you will get a straight answer on '
             'whether a visit is worth it.</p>'
             '</div></section>')
    body += '<section class="section"><div class="wrap wrap--narrow"><figure class="learn__figure">'
    body += _img("patio-firepit-build", "A paver patio curving around a circular fire pit, cut field tight to a stone seat wall.",
                 "(max-width:1024px) 100vw, 900px")
    body += '<figcaption><strong>Stone work, and the ground work under it.</strong> One crew, one standard of base work, on every job.</figcaption></figure></div></section>'
    body += ('<section class="section"><div class="wrap wrap--narrow">'
             + _sec_head("Common questions", "Service questions, answered")
             + _faq_block(site.FAQS_HUB["services"]) + '</div></section>')
    body += _cta(trail, "Not sure which you need?", "Tell Bryce what the yard is doing and he'll say straight.")
    html_str = site.render_shell(
        title="Patio, Wall, Walkway, Site Work & Snow Services in Mansfield, MA | Bryce's Patios",
        desc="Stone patios, walkways, retaining walls and fire pits, plus grading, land clearing and snow plowing across southeastern Massachusetts. Owner-operated, free estimates.",
        url=f"{site.BASE}/services/", trail=trail, body=body,
        ld_extra=[_faq_ld(site.FAQS_HUB["services"], f"{site.BASE}/services/")],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, "services/index.html", html_str)

def build_town(root: Path, t: str) -> None:
    tslug = site.slug(t)
    trail = [("Home", "/"), ("Service Area", "/areas/"), (f"{t}, MA", f"/areas/{tslug}/")]
    svc_rows = []
    for s in _TOWN_SVC:
        svc_rows.append(f'<li><a href="/areas/{tslug}/{s["key"]}/">{site.esc(s["name"])} in {site.esc(t)}, MA</a></li>')
    body = [f'<section class="section"><div class="wrap wrap--narrow">']
    body.append(site.crumb_html(trail))
    body.append(f'<header class="section__head"><p class="eyebrow">{site.esc(t)}, Massachusetts</p>'
                f'<h1 class="h2">Stone patios &amp; hardscaping in {site.esc(t)}, MA</h1></header>')
    body.append(site.page_actions())
    body.append(f'<p class="lede">Bryce builds patios, walkways, retaining walls and fire pits in {site.esc(t)} and the towns next to it. One crew, one person quoting the job, and it is the same person who builds it.</p>')
    summary = getattr(site, "TOWN_SUMMARY", {}).get(t)
    if summary:
        body.append(f'<p class="prose">{site.esc(summary)}</p>')
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
    town_faqs = [(q.format(town=t), a.format(town=t)) for q, a in site.FAQS_TOWN]
    body.append('<section class="section"><div class="wrap wrap--narrow">'
                + _sec_head("Common questions", f"Patio questions in {t}, answered")
                + _faq_block(town_faqs) + '</div></section>')
    body.append(_cta(trail, f"Getting a quote in {t}", "Free estimates, no hard limits on where we go."))
    html_str = site.render_shell(
        title=f'Stone Patios in {t}, MA | Patio Builder',
        desc=f'Owner-operated stone patio, walkway, retaining wall and fire pit installation in {t}, MA. Free estimates from Bryce\'s Patios.',
        url=f"{site.BASE}/areas/{tslug}/", trail=trail, body="".join(body),
        ld_extra=[_faq_ld(town_faqs, f"{site.BASE}/areas/{tslug}/")],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, f"areas/{tslug}/index.html", html_str)

# A town-specific opening clause that leads the service x town lede. It turns the
# one shared service description into a page that names the actual ground in this
# town first, which is the difference the outside audit asked for: each town page
# earns its place by reading like it was written for that town, not spun from a
# matrix. Facts stay generic to the town (grade, water, lots), never invented.
TOWN_LEAD = {
    "Mansfield": "Mansfield is the home town, so this is the ground we know best",
    "Foxborough": "Foxborough yards cover the range from flat to wet",
    "Attleboro": "Attleboro sits on ledge and old mill-era lots",
    "North Attleboro": "North Attleboro yards trend toward a fall",
    "Norton": "Norton lots run larger and flatter than most of the neighbors",
    "Franklin": "Franklin sits higher, with wetter springs and a harder freeze",
    "Seekonk": "Seekonk yards sit close to the line and the water table that comes with it",
    "Rehoboth": "Rehoboth is big-lot country with long driveways and open sky",
    "Plainville": "Plainville is winding and tree-heavy, with shade that holds moisture",
    "Taunton": "Taunton yards sit on mixed soil that runs from sand to clay",
    "Easton": "Easton properties are mature and established, with plantings near the house",
    "Sharon": "Sharon lots are hilly and wooded, with grades steep enough to matter",
}

def _town_lead(t: str) -> str:
    return TOWN_LEAD.get(t, "")

# A short, natural closing line for the last FAQ answer on each service x town
# page. Written per town so the FAQ block is not byte-identical across towns.
TOWN_FAQ_TAIL = {
    "Mansfield": "Mansfield is home base, so it is a short run out to look at a yard here.",
    "Foxborough": "Foxborough is a quick run down 495, so a site visit is no trouble.",
    "Attleboro": "Attleboro is close enough to be out there the same week.",
    "North Attleboro": "North Attleboro is minutes away, so it is easy to come look.",
    "Norton": "Norton is a normal job on the run from the Mansfield yard.",
    "Franklin": "Franklin is a short run out, so the visit is straightforward.",
    "Seekonk": "Seekonk is a normal drive from the yard, so a visit is easy to set up.",
    "Rehoboth": "Rehoboth is within the regular run, so a visit is no problem.",
    "Plainville": "Plainville is close by, so it is easy to come take a look.",
    "Taunton": "Taunton is a normal drive from the yard, so a visit is easy to arrange.",
    "Easton": "Easton is a short run out, so the visit is no trouble.",
    "Sharon": "Sharon is a normal drive from the yard, so a visit is easy to set up.",
}

def build_service_town(root: Path, t: str, s: dict) -> None:
    """Service x town page for the six towns that matter most."""
    tslug = site.slug(t)
    trail = [("Home", "/"), ("Service Area", "/areas/"), (f"{t}, MA", f"/areas/{tslug}/"),
             (s["name"], f"/areas/{tslug}/{s['key']}/")]
    faqs = [(q.format(town=t) if "{town}" in q else q,
             a.format(town=t) if "{town}" in a else a) for q, a in s["faq"]]
    # Give the final answer one town-specific closing line so the FAQ block is
    # not byte-identical across the twelve towns. Reads as a plain sentence and
    # never repeats the town name the lead already opens with.
    if faqs and TOWN_FAQ_TAIL.get(t):
        _q, _a = faqs[-1]
        faqs[-1] = (_q, _a + " " + TOWN_FAQ_TAIL[t])
    body = [f'<section class="section"><div class="wrap wrap--narrow">']
    body.append(site.crumb_html(trail))
    body.append(f'<header class="section__head"><p class="eyebrow">{site.esc(t)}, MA &middot; {site.esc(s["name"])}</p>'
                f'<h1 class="h2">{site.esc(s["h1"].format(town=t))}</h1></header>')
    body.append(site.page_actions())
    lead = _town_lead(t)
    if lead:
        body.append(f'<p class="lede">{site.esc(lead + ". " + s["blurb"])}</p>')
    else:
        body.append(f'<p class="lede">{site.esc(s["blurb"])}</p>')
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
        title=f'{s["name"]} in {t}, MA | Free Estimates',
        desc=f'{s["name"]} installed in {t}, MA on a full-depth compacted base. Owner-operated, free estimates from Bryce\'s Patios.',
        url=f"{site.BASE}/areas/{tslug}/{s['key']}/", trail=trail, body="".join(body),
        ld_extra=[_faq_ld(faqs, f"{site.BASE}/areas/{tslug}/{s['key']}/")],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, f"areas/{tslug}/{s['key']}/index.html", html_str)

# Per-service, per-town paragraph for the service x town pages. One paragraph
# per page: the town-specific beat and the service detail are merged here so no
# page says the same thing twice.
SVC_TOWN_DETAIL = {
    "patios": {
        "Mansfield": "Most Mansfield patios get laid out off the back door and run toward the low corner of the lot, which keeps the walkout clear and gives the water a direction. The plans usually start by watching where the shade line lands at five o'clock, so the patio stays locked to the grade and still catches the evening sun.",
        "Foxborough": "On the flat lots here the patio usually wants a slight crown away from the house, and on the wet ones the first week is often drainage before any stone. Soil varies from lot to lot, so the base stone and the edge restraint get picked for the way water moves under the field before the surface is chosen.",
        "Attleboro": "Older Attleboro yards mean we sometimes re-grade before we lay anything, so the patio sits at a height that still meets the door threshold. Pockets of clay hold water here, so the sub-base is checked before the stone goes in and the low point is moved off the patio edge when it needs to be.",
        "North Attleboro": "The slope here usually earns a set of steps and a seat wall keeping the main field level, so the patio reads as one room instead of three. These yards often show their age in the grading, so we reset the line where the lawn meets the patio instead of following an old edge that no longer runs true.",
        "Norton": "With bigger lots, the patio is often set back nearer the tree line and ties into a path or a second sitting area, so the drainage plan covers the whole run rather than just the patio footprint.",
        "Franklin": "Franklin patios get a base dug to the depth the ground and drainage call for, and a start date that waits for the subgrade to be compactable rather than following the first heavy rain.",
        "Seekonk": "Seekonk yards are often tight and near the Rhode Island line, so the patio is laid out to the shape that fits and the runoff is still sent clear of the neighbor line. Small lots here also mean the base is compacted in narrower lifts and the edge is held hard, because there is less room for the field to move without it showing.",
        "Rehoboth": "Rehoboth's open, sandy lots drain fast, which lets the patio sit a little lower and wider, but the base is still dug to depth and compacted in lifts. That sand also means the edge needs a real border, since a loose edge in fast-draining ground spreads out over a few winters.",
        "Plainville": "In Plainville's tree-heavy yards the shade keeps the surface wet longer, so the base is built dry and the slope is set a touch stronger to shed that water. Roots and shade also decide where the equipment can go, so these patios are often dug and compacted in tighter passes than a wide-open lot would need.",
        "Taunton": "Taunton lots run large on mixed soil, so the patio usually follows the existing grade and the drainage is worked out before the shape is drawn. Mixed soil can settle unevenly from one end of the field to the other, so the base is built up in even lifts and checked with a level as it goes.",
        "Easton": "In Easton's older, planted yards the patio is set to protect the root zones and to fit where the equipment can get in without tearing up the lawn. Established yards also hold the grade they were built with, so the patio is set to meet the existing door and walk heights rather than forcing a new level.",
        "Sharon": "Sharon's steep, wooded lots usually earn steps and a retaining edge first, with the patio field laid out on the level that is left. On that kind of fall the retaining edge gets a footing dug past the frost line and a drain path out to the low corner, so the level it holds stays level.",
    },
    "walkways": {
        "Mansfield": "A Mansfield walkway usually runs front door to drive or front door to patio, and the width and the rise are set by the door threshold and the pitch of the drive apron. It gets the same base as the patio underneath, so it does not dip at the joints.",
        "Foxborough": "Walkways on flat Foxborough lots need positive fall or they puddle, so the grade is set on the walk even when the yard looks level.",
        "Attleboro": "In older Attleboro yards the path often steps down with the grade rather than cutting through it, which protects tree roots and looks settled. Those older lots also mean the walk ties into an existing slab or step, so the new pitch is matched to what is already at the door.",
        "North Attleboro": "Sloped North Attleboro entries get stone steps set into the run instead of a ramp, so the walk stays comfortable and drains at each tread. The base under those steps is dug past the frost line, so the joints do not open.",
        "Norton": "Longer Norton runs get a gentle switch and a low point at the drive so the whole path sheds instead of holding water mid-run. On a run that long the base is compacted in lifts the full length, with the low point set partway rather than only at the ends.",
        "Franklin": "Franklin walkways are set on a deeper base where the frost moves hard, and landings are placed to catch drift before the door. The whole run is dug to the same depth the patio gets, because a shallow trench is what the freeze and thaw cycles punish first.",
        "Seekonk": "In tight Seekonk yards the walk is often a narrow run that still gets a full-depth base, so it stays even where it squeezes past a foundation bed. Narrow runs get their fall set carefully, because a walk with no room to spare has no room to puddle either.",
        "Rehoboth": "Sandy Rehoboth ground drains on its own, so the walk there is graded to stay slightly proud and shed, with a low point worked in at the drive. The base under it is still dug and compacted like the patio, so the joints stay tight even where the ground is forgiving.",
        "Plainville": "Shade and roots in Plainville mean the walk is dug by hand around what has to stay, and the base is compacted in short lifts so the joints hold. Shaded ground also stays wet longer, so the run is set to a slightly stronger fall than a sunny yard would need.",
        "Taunton": "Longer Taunton lots get a walk that steps with the grade instead of cutting through it, and a low point set where it meets the drive. The risers are set to one height and the base is checked in sections, so a dip that would show halfway down is caught while the stone is still open.",
        "Easton": "Established Easton plantings decide the route, so the walk curves around beds and trees and still falls away from the house the whole way. Curves also mean the fall has to keep working on the bend, so each turn is graded to shed rather than flatten out.",
        "Sharon": "On Sharon's hills the walk becomes stone steps set into the run, with each landing graded so it sheds instead of holding water. Each tread is set on its own compacted base, so a step on a hill does not work loose a few winters in.",
    },
    "retaining-walls": {
        "Mansfield": "Mansfield walls usually hold back a grade that falls toward the house, so the wall doubles as the edge of the patio above it, and the base course and the cap are set together with the patio, not after it. The frost line sets the footing depth, so the wall is buried to a point the winter cannot lift it and the base course stays where it was set.",
        "Foxborough": "Where a Foxborough lot is flat but wet, the wall is more often a low border that ties the patio together than a structural face holding real grade. Because those lots drain slowly, the gravel backfill and the outlet matter as much as the face.",
        "Attleboro": "Older Attleboro grades shift, so a wall is set on its own footing and drainage behind it is designed before the face goes up. The height also changes along the run, so the footing and the face are stepped together instead of held at one level.",
        "North Attleboro": "North Attleboro walls carry the slope, so they get a compacted gravel backfill, drain stone and a weep path out toward the low corner, designed before the first block is set.",
        "Norton": "Norton's bigger yards often want a low terrace wall to keep the patio level while the lawn steps down toward the tree line, rather than a single tall face taking the whole drop. On a long run like that each section gets its own footing and drain path.",
        "Franklin": "Franklin's deeper frost means wall footings are dug past it, so the face stays plumb after a hard winter. Franklin also has stretches of flat new-build yard where a low seat wall is the better answer than a tall one, because there is no real grade to hold back, only a change of level.",
        "Seekonk": "Tight Seekonk lots usually want a low wall as a clean edge rather than a tall face, with the footing still dug to depth and drainage run out before the face goes up. On a small lot the drain path has to be planned early and the base kept inside the property line, because there is less room to send that water once the wall is standing.",
        "Rehoboth": "On Rehoboth's sandy ground the wall is mostly holding a change of level, so the footing is set past the frost line, dug wider because sand offers less grip, and the backfill still drains rather than trapping water. Even in sand the wall is built on one continuous footing, so the face does not step apart where the grade shifts.",
        "Plainville": "Tree roots and shade in Plainville mean the wall footing is dug around what has to stay, and the drain behind the face is planned before the first course. Shaded ground stays wet, so the backfill is gravel with a weep path set before the face stone, not soil that will hold that water against the wall.",
        "Taunton": "Taunton's mixed soil can settle unevenly, so the wall is built on one continuous compacted footing rather than stepped pads that can move apart, and the face is set to a string line and checked as it rises. Clay pockets also hold water against the face, so the backfill and the outlet are sized for a slower release than sand would need.",
        "Easton": "Older Easton yards often have an existing grade change a wall can finish cleanly, with root protection deciding how close the footing can come. Where roots rule out a deep footing, the wall is kept low and the grade is split between a wall and a planted slope instead, and where a wall failed once already the old footing is dug out and the base started fresh.",
        "Sharon": "Sharon's steep wooded lots usually need the wall to carry real fall, so it gets compacted backfill, drain stone and a weep path out to the low corner, with the height, the footing and the drainage worked out together.",
    },
    "fire-pits": {
        "Mansfield": "A Mansfield fire pit usually sits on its own level pad off the patio, far enough from the house for a real fire and near enough to share the seating, and roomy yards let it sit back so the smoke drifts away from the door.",
        "Foxborough": "On wet Foxborough lots the pit goes on ground that drains, which sometimes decides the corner before the design does, and the pad is raised on compacted base so the ring never sits in standing water.",
        "Attleboro": "Older Attleboro yards often fit the pit into an existing level corner, which takes the least new grade and the least new stone.",
        "North Attleboro": "Sloped North Attleboro yards get the pit on a built terrace, so it sits flat and the seating rings it evenly, with the footing dug past the frost line so the ring stays level across winters.",
        "Norton": "With room to work, Norton pits often get a wider ring of seating and a gravel apron so the area stays off the lawn and usable through the wet months.",
        "Franklin": "Franklin pits use a stone ring set on a compacted base, so frost does not tip the course out of level over winter, and the pad is built when the spring ground can be compacted dry instead of right after the thaw.",
        "Seekonk": "In a tight Seekonk yard the pit goes where it needs the least new grade, usually a level corner off the patio, with the seating kept inside the property line and a clear ring measured from the house first.",
        "Rehoboth": "Rehoboth's fast-draining sand lets the pit sit on a simple compacted base, and the open lots give it room to sit back so the seating rings wide and the smoke drifts clear of the door.",
        "Plainville": "Shade in Plainville means the pit is set where it drains and the stone ring is footed so it does not lift when the ground holds water in spring. The apron around the ring is built firm, so the area stays underfoot instead of turning to mud.",
        "Taunton": "On larger Taunton lots the pit usually gets more room, a wider gravel apron and seating that rings it evenly on one flat pad, set farther from the house and the tree line.",
        "Easton": "In Easton's older yards the pit is fitted into an existing level corner, so it needs the least new stone and leaves the root zones of the big trees alone.",
        "Sharon": "On Sharon's slopes the pit sits on a built terrace, graded and compacted the same way as the patio, so the ring stays level and the seating rings it evenly. The terrace edge is held with a low wall or stone border, so the level does not wash out.",
    },
}

def _svc_town_detail(svc_key: str, t: str) -> str:
    return SVC_TOWN_DETAIL.get(svc_key, {}).get(t, "")


# Per-service closing paragraph: what we watch for, worded for each service and
# lightly varied by town so the copy stays specific instead of template-filler.
_SVC_WATCH = {
    "patios": (
        "The pavers get picked near the end, once the shape, the fall and the edge are settled. In {t} the "
        "layout usually starts from two fixed points - where the house sends its water and where the sun sits "
        "late in the day - and the field is drawn to serve both. Choosing stone first is how a patio ends up "
        "with a handsome surface over a shape that never quite works.",
        "When a patio quote is much lower than the others, ask what it does not include. Depth, compaction, "
        "slope and edge restraint are the four things to compare line by line. "
        "In {t} the grade and the frost line make all four matter, so we walk the yard, set the fall away from "
        "the house, and build the base before a single paver is set. That is also why a patio here gets quoted "
        "by the square foot with the excavation, the gravel and the compaction in it, not as a flat number for "
        "stone laid on whatever is already there.",
    ),
    "walkways": (
        "Where a walk meets a step, a landing or the driveway is where most of the thought goes. In {t} the "
        "joins are set so the run lands flush and the fall keeps moving through the transition instead of "
        "stalling at it. A walk can be dead level across the field and still trip you at the one spot where "
        "two surfaces meet.",
        "Width gets decided by what the walk has to carry, not by the stone on it. In {t} a path that only takes "
        "foot traffic can run narrower than one that has to pass a wheelbarrow or a mower, and the edging is set "
        "to hold that width for good. A run that has to be widened a year later never quite matches the first "
        "stretch, so we settle the width before the trench is opened.",
    ),
    "retaining-walls": (
        "Ties matter as much as the wall. In {t} a wall that ends in mid-air, or meets a set of steps with no "
        "return, is the one that opens a gap as the seasons move it. Burying both ends into the grade costs "
        "almost nothing at the time and is the difference between a wall that reads as finished and one that "
        "always looks like it is missing a piece.",
        "In {t} that means sizing the wall to the grade it is actually holding, not just the height that looks "
        "right from the deck, and letting drainage decide how far the base extends behind the face. The height "
        "you see from the deck and the load the wall actually carries are two different numbers, and the footing "
        "is set from the second one.",
    ),
    "fire-pits": (
        "Where the pit sits decides how much you use it. In {t} we keep it off the main walking line, far "
        "enough from the house wall for the smoke to clear, and close enough to the seating that the fire "
        "still does its job. A pit that crowds the door or the grill is the one that ends up with a cover "
        "on it.",
        "The ring itself is set level before anything is stacked on it, and checked course by course, because a "
        "pit only reads as wrong once the cap is on and the error is already buried. In {t} we screed the bed "
        "for the first course and keep the inside open so ash and rainwater have somewhere to go. A ring laid "
        "to a string line rather than a level shows up the moment the cap goes on.",
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
    body = f'''<section class="section"><div class="wrap">
      {site.crumb_html(trail)}
      <header class="section__head section__head--center">
        <p class="eyebrow">Service area</p>
        <h1 class="h2">Where Bryce builds.</h1>
        <p class="section__sub">Based at 885 West St in Mansfield, MA and working across southeastern Massachusetts. Pick your town for local detail, or just call.</p>
      </header>
      {site.page_actions(center=True)}
      <div class="area__grid">
        <div class="area__intro">
          <h2 class="h2">Towns we work in</h2>
          <p>Twelve Massachusetts towns we are in most often, all within a short drive of the Mansfield yard.</p>
        </div>
        <div class="area__lists">
          <div class="area__col"><h3 class="area__state">Massachusetts</h3><ul class="area__towns">{ma}</ul></div>
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
             '<p class="prose">Everything here is built the same way: a base dug to depth and compacted in '
             'lifts, because a shallow base will heave no matter how good the stone looks. If your project '
             'sits outside this area, call and we will tell you straight whether it makes sense.</p>'
             '</div></section>')
    body += ('<section class="section"><div class="wrap wrap--narrow"><figure class="learn__figure">'
             + _img("big-yard", "A wide curved paver patio across a large back yard.",
                    "(max-width:1024px) 100vw, 900px")
             + '<figcaption><strong>Southeastern Massachusetts.</strong> Most of the work sits within a short drive of the Mansfield yard.</figcaption></figure></div></section>')
    body += ('<section class="section"><div class="wrap wrap--narrow">'
             + _sec_head("Common questions", "Service area questions, answered")
             + _faq_block(site.FAQS_HUB["areas"]) + '</div></section>')
    body += _cta(trail, "Somewhere else in the area?", "Bryce has no hard limits. Call and ask.")
    html_str = site.render_shell(
        title="Service Area | Southeastern MA | Bryce's Patios",
        desc="Bryce's Patios builds stone patios, walkways, walls and fire pits across southeastern Massachusetts. See the towns we cover.",
        url=f"{site.BASE}/areas/", trail=trail, body=body,
        ld_extra=[_faq_ld(site.FAQS_HUB["areas"], f"{site.BASE}/areas/")],
        svc_links=_svc_links(), town_links=_town_links())
    write_page(root, "areas/index.html", html_str)

def build_sitemap(root: Path) -> None:
    urls = [f"{site.BASE}/", f"{site.BASE}/learn/", f"{site.BASE}/services/", f"{site.BASE}/areas/"]
    urls += [f"{site.BASE}/learn/{g['key']}/" for g in site.GUIDES]
    urls += [f"{site.BASE}/services/{s['key']}/" for s in site.SERVICES]
    urls += [f"{site.BASE}/areas/{site.slug(t)}/" for t in site.TOWNS_MA]
    for t in site.TOWNS_MA:
        urls += [f"{site.BASE}/areas/{site.slug(t)}/{s['key']}/" for s in _TOWN_SVC]
    today = _dt.date.today().isoformat()

    # page -> hero image filename (for the Google image sitemap extension)
    img_for = {
        f"{site.BASE}/": ("patio-firepit-build", "A paver patio and circular fire pit under construction"),
        f"{site.BASE}/services/": ("patio-firepit-build", "Paver patios, walls and fire pits built by Bryce's Patios"),
        f"{site.BASE}/areas/": ("big-yard", "Stone patio work across southeastern Massachusetts"),
        f"{site.BASE}/learn/": ("craft-base", "Patio base and craft guides from Bryce's Patios"),
    }
    for t in site.TOWNS_MA:
        nm = site.TOWN_IMG.get(t, "project-dining")
        img_for[f"{site.BASE}/areas/{site.slug(t)}/"] = (
            nm, "Stone patio work in " + t + ", MA by Bryce's Patios")
    for g in site.GUIDES:
        img_for[f"{site.BASE}/learn/{g['key']}/"] = (g["img"], g["img_alt"])
    for s in site.SERVICES:
        if s.get("img"):
            img_for[f"{site.BASE}/services/{s['key']}/"] = (s["img"], s["img_alt"])
    for t in site.TOWNS_MA:
        tsl = site.slug(t)
        for s in _TOWN_SVC:
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
        # Video sitemap extension. One entry per page that carries a video.
        vid = None
        if u == f"{site.BASE}/":
            vid = dict(
                thumb=f'{site.BASE}/assets/img/hero-finished.jpg',
                title='Bryce&#39;s Patios showreel',
                desc=('Eight real jobs, start to finish: base prep, paver patios, '
                      'walkways, steps, walls and fire pits around Mansfield, MA.'),
                content=f'{site.BASE}/assets/video/showreel-1080p-silent-{site.REEL_HASH}.mp4',
                player=f'{site.BASE}/#film',
                dur='29',
            )
        elif u in (f'{site.BASE}/learn/patio-base/', f'{site.BASE}/services/patios/'):
            vid = dict(
                thumb=f'{site.BASE}/assets/img/craft-base.jpg',
                title='How a patio base is built',
                desc=('Silent, captioned walk through a patio build: the dig, the compacted '
                      'aggregate base in lifts, the screeded setting bed, the cut edge and the '
                      'finished pavers, by Bryce\'s Patios in Mansfield, MA.'),
                content=f'{site.BASE}/assets/video/patio-base-explainer-1080p-silent.mp4',
                player=u,
                dur='23',
            )
        if vid:
            row += (
                '<video:video>'
                f'<video:thumbnail_loc>{vid["thumb"]}</video:thumbnail_loc>'
                f'<video:title>{vid["title"]}</video:title>'
                f'<video:description>{vid["desc"]}</video:description>'
                f'<video:content_loc>{vid["content"]}</video:content_loc>'
                f'<video:duration>{vid["dur"]}</video:duration>'
                '<video:publication_date>2026-10-09T09:00:00-04:00</video:publication_date>'
                '<video:family_friendly>yes</video:family_friendly>'
                '<video:live>no</video:live>'
                '</video:video>')
        row += '</url>'
        rows.append(row)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"\n'
           '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n'
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
        for s in _TOWN_SVC:
            build_service_town(root, t, s); n += 1
    total = build_sitemap(root)
    nfeed = build_feed(root)
    print(f"wrote {n+1} pages, sitemap has {total} urls, feed has {nfeed} entries")


if __name__ == "__main__":
    main()
